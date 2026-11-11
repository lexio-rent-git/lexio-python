"""Client Python officiel de l'API Lexio Rent (logiciel de gestion de location de véhicules).

Documentation de l'API : https://docs.lexio.rent
"""
from ._client import DEFAULT_BASE_URL, Lexio, __version__
from ._errors import (
    AuthenticationError,
    ConflictError,
    LexioError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from ._resources import SPEC_VERSION

__all__ = [
    "Lexio",
    "DEFAULT_BASE_URL",
    "SPEC_VERSION",
    "__version__",
    "LexioError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
]
