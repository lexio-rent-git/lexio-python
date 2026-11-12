"""Client HTTP de l'API Lexio Rent."""
from __future__ import annotations

import os
import time
import uuid
from typing import Any, Callable, Iterator, Mapping

import httpx

from ._errors import LexioError, RateLimitError, error_for
from ._resources import RESOURCES, SPEC_VERSION

DEFAULT_BASE_URL = "https://api.lexio.rent/api/external/v1"
__version__ = "0.1.1"
USER_AGENT = f"lexio-rent-python/{__version__} (+https://github.com/lexio-rent-git/lexio-python)"
RETRYABLE = {429, 500, 502, 503, 504}


class Lexio:
    """Client de l'API Lexio Rent.

    >>> from lexio_rent import Lexio
    >>> lexio = Lexio()                     # lit LEXIO_API_KEY dans l'environnement
    >>> for v in lexio.paginate(lexio.vehicles.list, is_archived="false"):
    ...     print(v["registrationNumber"])

    L'authentification se fait uniquement par ``Authorization: Bearer lck_…``.
    Les écritures qui exigent ``Idempotency-Key`` en reçoivent une automatiquement
    (UUID v4), réutilisée telle quelle lors des nouvelles tentatives.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 2,
        http_client: httpx.Client | None = None,
    ) -> None:
        key = api_key or os.environ.get("LEXIO_API_KEY")
        if not key:
            raise ValueError(
                "Clé API manquante : passez api_key=… ou définissez LEXIO_API_KEY "
                "(Lexio → Paramètres → Développeur → Tokens API)."
            )
        self.api_key = key
        self.base_url = (base_url or os.environ.get("LEXIO_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.max_retries = max_retries
        self._http = http_client or httpx.Client(timeout=timeout)
        self._owns_http = http_client is None
        for attr, cls in RESOURCES.items():
            setattr(self, attr, cls(self))

    # -- cycle de vie -------------------------------------------------------
    def close(self) -> None:
        if self._owns_http:
            self._http.close()

    def __enter__(self) -> "Lexio":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- requêtes -----------------------------------------------------------
    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        idempotency_key: str | None = None,
        idempotency_required: bool = False,
    ) -> Any:
        """Envoie une requête et renvoie le JSON décodé (``None`` pour un 204)."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        if idempotency_key is None and idempotency_required:
            idempotency_key = str(uuid.uuid4())
        if idempotency_key is not None:
            headers["Idempotency-Key"] = idempotency_key
        query = {k: _fmt(v) for k, v in (params or {}).items() if v is not None}

        attempt = 0
        while True:
            resp = self._http.request(
                method, self.base_url + path, params=query or None, json=json, headers=headers
            )
            if resp.status_code < 400:
                if resp.status_code == 204 or not resp.content:
                    return None
                return resp.json()

            can_retry = resp.status_code in RETRYABLE and (
                method == "GET" or idempotency_key is not None
            )
            if can_retry and attempt < self.max_retries:
                time.sleep(_retry_delay(resp, attempt))
                attempt += 1
                continue
            raise _to_error(resp)

    def paginate(self, list_method: Callable[..., Any], **kwargs: Any) -> Iterator[Any]:
        """Parcourt toutes les pages d'une méthode ``list`` (curseur ``nextCursor``)."""
        cursor = kwargs.pop("cursor", None)
        while True:
            page = list_method(cursor=cursor, **kwargs)
            yield from page.get("data") or []
            cursor = page.get("nextCursor")
            if not cursor:
                return

    def __repr__(self) -> str:
        return f"Lexio(base_url={self.base_url!r}, spec={SPEC_VERSION})"


def _fmt(value: Any) -> Any:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple)):
        return ",".join(str(v) for v in value)
    return value


def _retry_delay(resp: httpx.Response, attempt: int) -> float:
    ra = resp.headers.get("Retry-After")
    if ra:
        try:
            return min(float(ra), 60.0)
        except ValueError:
            pass
    return min(0.5 * (2**attempt), 8.0)


def _to_error(resp: httpx.Response) -> LexioError:
    try:
        problem = resp.json()
        if not isinstance(problem, dict):
            problem = {"detail": str(problem)}
    except ValueError:
        problem = {"detail": resp.text[:500]} if resp.text else {}
    err = error_for(resp.status_code, problem, resp.headers.get("X-Request-Id"))
    if isinstance(err, RateLimitError):
        try:
            err.retry_after = float(resp.headers.get("Retry-After", ""))
        except ValueError:
            err.retry_after = None
    return err
