"""Erreurs renvoyées par l'API Lexio Rent (format RFC 9457 ``application/problem+json``)."""
from __future__ import annotations

from typing import Any, Mapping


class LexioError(Exception):
    """Erreur de l'API Lexio Rent.

    Attributs utiles : ``status`` (code HTTP), ``code`` (ex. ``VEHICLE_UNAVAILABLE``),
    ``detail`` (explication lisible), ``request_id`` (à transmettre au support),
    ``problem`` (corps complet de la réponse).
    """

    def __init__(self, status: int, problem: Mapping[str, Any] | None, *, request_id: str | None = None) -> None:
        self.status = status
        self.problem: dict[str, Any] = dict(problem or {})
        self.code: str | None = self.problem.get("code")
        self.title: str | None = self.problem.get("title")
        self.detail: str | None = self.problem.get("detail")
        self.request_id: str | None = self.problem.get("requestId") or request_id
        label = self.code or f"HTTP_{status}"
        msg = f"{label} ({status})"
        if self.detail:
            msg += f" : {self.detail}"
        if self.request_id:
            msg += f" [requestId={self.request_id}]"
        super().__init__(msg)


class AuthenticationError(LexioError):
    """401 : clé absente, invalide, expirée, révoquée ou désactivée."""


class PermissionDeniedError(LexioError):
    """403 : scope manquant ou fonctionnalité absente du plan (``FEATURE_NOT_AVAILABLE``)."""


class NotFoundError(LexioError):
    """404 : ressource introuvable dans l'organisation de la clé."""


class ConflictError(LexioError):
    """409 : véhicule indisponible, devis expiré, prix changé, clé d'idempotence déjà utilisée…"""


class ValidationError(LexioError):
    """400 / 422 : requête mal formée ou refusée par les règles métier."""


class RateLimitError(LexioError):
    """429 : quota dépassé ; ``retry_after`` donne l'attente conseillée en secondes."""

    retry_after: float | None = None


class ServerError(LexioError):
    """5xx : erreur côté Lexio Rent ; réessayer plus tard avec la même clé d'idempotence."""


def error_for(status: int, problem: Mapping[str, Any] | None, request_id: str | None) -> LexioError:
    if status == 401:
        cls: type[LexioError] = AuthenticationError
    elif status == 403:
        cls = PermissionDeniedError
    elif status == 404:
        cls = NotFoundError
    elif status == 409:
        cls = ConflictError
    elif status in (400, 413, 415, 422):
        cls = ValidationError
    elif status == 429:
        cls = RateLimitError
    elif status >= 500:
        cls = ServerError
    else:
        cls = LexioError
    return cls(status, problem, request_id=request_id)
