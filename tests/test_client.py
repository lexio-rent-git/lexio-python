import json

import httpx
import pytest

from lexio_rent import (
    AuthenticationError,
    ConflictError,
    Lexio,
    NotFoundError,
    RateLimitError,
)


def make(handler, **kw):
    return Lexio("lck_test", http_client=httpx.Client(transport=httpx.MockTransport(handler)), **kw)


def test_bearer_auth_and_user_agent():
    seen = {}

    def handler(req):
        seen.update(req.headers)
        return httpx.Response(200, json={"data": {"name": "Démo"}})

    assert make(handler).organization.get() == {"data": {"name": "Démo"}}
    assert seen["authorization"] == "Bearer lck_test"
    assert "x-api-key" not in seen
    assert seen["user-agent"].startswith("lexio-rent-python/")


def test_missing_key(monkeypatch):
    monkeypatch.delenv("LEXIO_API_KEY", raising=False)
    with pytest.raises(ValueError):
        Lexio()


def test_env_key(monkeypatch):
    monkeypatch.setenv("LEXIO_API_KEY", "lck_env")
    assert Lexio().api_key == "lck_env"


def test_path_and_query_params():
    seen = {}

    def handler(req):
        seen["url"] = str(req.url)
        return httpx.Response(200, json={"data": [], "nextCursor": None})

    make(handler).vehicles.list(is_archived=False, category_id="abc", limit=10)
    assert seen["url"].startswith("https://api.lexio.rent/api/external/v1/vehicles?")
    assert "isArchived=false" in seen["url"]
    assert "categoryId=abc" in seen["url"]
    assert "limit=10" in seen["url"]
    assert "cursor" not in seen["url"]


def test_path_parameter_substitution():
    seen = {}

    def handler(req):
        seen["path"] = req.url.path
        return httpx.Response(200, json={"data": {}})

    make(handler).rentals.get_payment("r1", "p2")
    assert seen["path"] == "/api/external/v1/rentals/r1/payments/p2"


def test_idempotency_key_generated_and_reused_on_retry():
    keys = []

    def handler(req):
        keys.append(req.headers.get("idempotency-key"))
        if len(keys) == 1:
            return httpx.Response(503, json={"code": "INTERNAL", "detail": "boom"}, headers={"Retry-After": "0"})
        return httpx.Response(201, json={"data": {"id": "r1"}})

    out = make(handler).rentals.create({"quoteId": "q1"})
    assert out == {"data": {"id": "r1"}}
    assert keys[0] and keys[0] == keys[1]


def test_explicit_idempotency_key():
    seen = {}

    def handler(req):
        seen["key"] = req.headers.get("idempotency-key")
        seen["body"] = json.loads(req.content)
        return httpx.Response(201, json={"data": {}})

    make(handler).rentals.create({"quoteId": "q1"}, idempotency_key="my-key")
    assert seen == {"key": "my-key", "body": {"quoteId": "q1"}}


def test_no_retry_on_non_idempotent_write():
    calls = []

    def handler(req):
        calls.append(1)
        return httpx.Response(503, json={"code": "INTERNAL"})

    client = make(handler)
    with pytest.raises(Exception):
        client.request("POST", "/whatever", json={})
    assert len(calls) == 1


def test_204_returns_none():
    assert make(lambda req: httpx.Response(204)).vehicles.delete("v1") is None


def test_problem_json_errors():
    def handler(req):
        if req.url.path.endswith("/missing"):
            return httpx.Response(404, json={"code": "NOT_FOUND", "detail": "x", "requestId": "rq1"})
        if req.url.path.endswith("/rentals"):
            return httpx.Response(409, json={"code": "VEHICLE_UNAVAILABLE", "detail": "déjà loué"})
        return httpx.Response(401, json={"code": "API_KEY_INVALID", "detail": "clé inconnue"})

    c = make(handler)
    with pytest.raises(NotFoundError) as e:
        c.vehicles.get("missing")
    assert e.value.code == "NOT_FOUND" and e.value.request_id == "rq1"
    with pytest.raises(ConflictError) as e:
        c.rentals.create({"vehicleId": "v"}, idempotency_key="k")
    assert e.value.code == "VEHICLE_UNAVAILABLE"
    with pytest.raises(AuthenticationError):
        c.organization.get()


def test_rate_limit_exhausted():
    def handler(req):
        return httpx.Response(429, json={"code": "RATE_LIMITED"}, headers={"Retry-After": "0"})

    with pytest.raises(RateLimitError) as e:
        make(handler, max_retries=1).vehicles.list()
    assert e.value.retry_after == 0


def test_paginate_follows_cursor():
    pages = {None: {"data": [1, 2], "nextCursor": "c2"}, "c2": {"data": [3], "nextCursor": None}}

    def handler(req):
        return httpx.Response(200, json=pages[req.url.params.get("cursor")])

    c = make(handler)
    assert list(c.paginate(c.vehicles.list, limit=2)) == [1, 2, 3]


def test_every_operation_is_exposed():
    from lexio_rent._resources import RESOURCES

    n = sum(
        1 for cls in RESOURCES.values() for name in vars(cls) if not name.startswith("_")
    )
    assert n == 93
