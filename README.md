# lexio-rent : client Python de l'API Lexio Rent

[![PyPI](https://img.shields.io/pypi/v/lexio-rent.svg)](https://pypi.org/project/lexio-rent/)
[![Licence MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE)

Client Python de l'[API publique de Lexio Rent](https://docs.lexio.rent). Il couvre les **93 opérations** de la version 1 : flotte, catalogue, tarification, devis, locations, départ et retour, paiements, entretien et flux d'événements.

<a href="https://lexio.rent/logiciel-location-voiture">Lexio Rent</a> est un logiciel de gestion de location de voitures, utilitaires et deux-roues pour les loueurs professionnels. Il gère le planning, les contrats, les états des lieux, les cautions et la flotte. L'API sert à brancher Lexio Rent sur votre site de réservation, votre comptabilité, un entrepôt de données ou un agent IA.

## Installation

```bash
pip install lexio-rent
```

Python 3.9 ou plus récent. Seule dépendance : `httpx`.

## Clé API

Dans Lexio : **Paramètres → Développeur → Tokens API → Nouveau token**. La clé commence par `lck_`. L'API est disponible avec le plan Business et n'a pas de bac à sable : testez sur une organisation dédiée.

```bash
export LEXIO_API_KEY="lck_..."
```

## Démarrage

```python
from lexio_rent import Lexio

lexio = Lexio()  # lit LEXIO_API_KEY ; ou Lexio(api_key="lck_...")

# Organisation liée à la clé
print(lexio.organization.get()["data"]["name"])

# Toute la flotte active, page après page
for vehicle in lexio.paginate(lexio.vehicles.list, is_archived=False):
    print(vehicle["registrationNumber"], vehicle["status"])

# Un devis, puis une location au prix du devis
quote = lexio.quotes.create({
    "vehicleId": vehicle["id"],
    "startAt": "2026-12-14T09:00:00",   # heure locale du loueur, sans décalage
    "endAt": "2026-12-16T18:00:00",
})["data"]

rental = lexio.rentals.create({
    "quoteId": quote["id"],
    "customer": {"firstName": "Camille", "lastName": "Martin", "email": "camille@example.com"},
})["data"]
```

## Ce que le client fait pour vous

| Sujet | Comportement |
|---|---|
| Authentification | `Authorization: Bearer lck_…` sur chaque requête (seule méthode acceptée par la v1). |
| Idempotence | Une `Idempotency-Key` (UUID v4) est générée pour les écritures qui l'exigent. Elle est réutilisée à l'identique lors d'une nouvelle tentative, donc la location n'est jamais créée deux fois. Vous pouvez passer la vôtre : `idempotency_key="..."`. |
| Nouvelles tentatives | En cas de 429 ou 5xx : jusqu'à 2 nouvelles tentatives (`max_retries`), en respectant `Retry-After`. Uniquement pour les GET et les écritures idempotentes. |
| Pagination | `lexio.paginate(méthode_list, **filtres)` suit `nextCursor` jusqu'au bout. |
| Erreurs | Les réponses `application/problem+json` deviennent des exceptions typées, avec `code`, `detail` et `request_id`. |
| Paramètres | Les filtres s'écrivent en snake_case (`is_archived=False` → `isArchived=false`). Les corps JSON gardent les noms de l'API (`startAt`, `vehicleId`…). |

### Gestion des erreurs

```python
from lexio_rent import ConflictError, RateLimitError, LexioError

try:
    lexio.rentals.create({"quoteId": quote_id})
except ConflictError as e:          # 409
    if e.code == "VEHICLE_UNAVAILABLE":
        ...
except RateLimitError as e:         # 429 après les nouvelles tentatives
    print("réessayer dans", e.retry_after, "s")
except LexioError as e:             # toute autre erreur de l'API
    print(e.status, e.code, e.detail, e.request_id)
```

Hiérarchie des exceptions : `LexioError` → `AuthenticationError` (401), `PermissionDeniedError` (403), `NotFoundError` (404), `ConflictError` (409), `ValidationError` (400, 413, 415, 422), `RateLimitError` (429), `ServerError` (5xx).

## Ressources disponibles

| Attribut | Méthodes |
|---|---|
| `organization` | `get` |
| `vehicles` | `list`, `get`, `create`, `update`, `delete`, `archive`, `unarchive`, `list_maintenance_alerts` |
| `vehicle_blocks` | `list` |
| `categories`, `options`, `deductibles`, `deposits`, `mileage_packages` | `list`, `get`, `create`, `update`, `delete` |
| `locations` | `list` |
| `customers` | `list`, `get`, `create`, `update`, `delete` |
| `availability` | `list` |
| `quotes` | `create`, `get` |
| `rentals` | `list`, `get`, `create`, `update`, `delete`, `cancel`, `reschedule`, `change_vehicle`, `change_customer`, `change_coverage`, `set_option_quantity`, `remove_option`, `list_amendments`, `pick_up`, `return_`, `list_inspections`, `create_photo_uploads`, `register_photos`, `list_photos`, `get_photo`, `delete_photo`, `list_payments`, `create_payment`, `get_payment`, `delete_payment`, `list_invoices`, `get_contract` |
| `pricing_settings` | `get` |
| `seasons` | `list`, `get`, `update` |
| `season_calendar` | `list_months`, `get_month`, `replace_month` |
| `duration_discounts` | `list`, `get`, `create`, `update`, `delete` |
| `lead_time_tiers` | `list`, `get`, `update` |
| `maintenance_operations` | `list` |
| `maintenance_records` | `list`, `get`, `create`, `update`, `delete` |
| `events` | `list` |

Chaque méthode porte en docstring le résumé et la description de l'opération OpenAPI correspondante (`help(lexio.rentals.create)`). Une opération pas encore couverte reste accessible avec `lexio.request("GET", "/chemin", params=...)`.

## Suivre les changements (polling d'événements)

L'API n'a pas de webhooks. On lit le flux `/events` avec un curseur que l'on conserve :

```python
cursor = load_cursor()  # None la première fois
page = lexio.events.list(cursor=cursor) if cursor else lexio.events.list(start="EARLIEST")
for event in page["data"]:
    handle(event)
save_cursor(page["nextCursor"])
```

Exemple complet : [`examples/sync_events.py`](examples/sync_events.py).

## Développement

```bash
python scripts/generate.py      # régénère src/lexio_rent/_resources.py depuis spec/openapi.json
pip install -e ".[test]" && pytest
```

`spec/openapi.json` est une copie de la spécification publiée sur <https://docs.lexio.rent/openapi.json> (version 1.0.5).

## À propos

Ce client est maintenu par l'équipe de <a href="https://lexio.rent/logiciel-location-voiture">Lexio Rent, logiciel de location de voitures</a>. Si vous gérez encore votre parc dans un tableur, notre <a href="https://lexio.rent/outils/gestion-parc-automobile-excel">modèle gratuit de gestion de parc automobile sous Excel</a> reprend les mêmes champs que l'API (immatriculation, kilométrage, échéances d'entretien), ce qui facilite l'import le jour où vous passez à l'API.

- Documentation de l'API : <https://docs.lexio.rent>
- Spécification OpenAPI : <https://docs.lexio.rent/openapi.json>
- Confidentialité : <https://lexio.rent/politique-de-confidentialite>
- Contact : contact@lexio.rent

Licence MIT.
