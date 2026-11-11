# Changelog

## 0.1.0 — 2026-11-11

- Première version : 93 opérations de l'API Lexio Rent v1 (spec OpenAPI 1.0.5), générées depuis `spec/openapi.json`.
- Authentification Bearer, `Idempotency-Key` automatique, nouvelles tentatives sur 429/5xx avec `Retry-After`, pagination par curseur, exceptions typées (problem+json).
