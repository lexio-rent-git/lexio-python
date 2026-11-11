"""Ressources de l'API Lexio Rent — FICHIER GÉNÉRÉ par scripts/generate.py, ne pas éditer."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping

if TYPE_CHECKING:
    from ._client import Lexio

SPEC_VERSION = "1.0.5"


class AvailabilityResource:
    """Opérations sur ``/availability``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, start_at: Any = None, end_at: Any = None, vehicle_id: Any = None, category_id: Any = None, vehicle_type: Any = None, is_available: Any = None) -> Any:
        """Lister les disponibilités et les prix.

        ``GET /availability`` (operationId ``listAvailability``).

        **Accès** : `offers.read` Prix réservable de chaque véhicule sur la période, avec forfait, franchise et caution par défaut (ceux de `POST /quotes`) : un devis sur les mêmes `vehicleId`, `startAt` et `endAt`, sans autre champ, donne le même `totalTTC`. Seul un devis fige le prix. **Périmètre** : véhicules actifs, non archivés, dont la catégorie tarifaire a un prix ; un véhicule sans catégorie tarifaire n’apparaît pas. **Filtres** : `startAt` et `endAt` obligatoires. `isAvailable=true` : réservables ; `false` : les autres, avec `unavailableReasons`. Identifiant inconnu : aucun élément. **Paginat

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``start_at`` → ``startAt``, ``end_at`` → ``endAt``, ``vehicle_id`` → ``vehicleId``, ``category_id`` → ``categoryId``, ``vehicle_type`` → ``vehicleType``, ``is_available`` → ``isAvailable``.
        """
        return self._client.request("GET", "/availability", params={"limit": limit, "cursor": cursor, "startAt": start_at, "endAt": end_at, "vehicleId": vehicle_id, "categoryId": category_id, "vehicleType": vehicle_type, "isAvailable": is_available})


class CategoriesResource:
    """Opérations sur ``/categories``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None) -> Any:
        """Lister les catégories tarifaires.

        ``GET /categories`` (operationId ``listCategories``).

        **Accès** : `catalog.read` Liste les catégories tarifaires de l’organisation, avec leurs prix journaliers par saison et leurs nombres de véhicules. Tri : `name`, puis `id`. Une catégorie fixe le prix journalier HT des véhicules qui s’y rattachent (`categoryId` du véhicule) ; un véhicule sans catégorie n’est pas réservable.

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``.
        """
        return self._client.request("GET", "/categories", params={"limit": limit, "cursor": cursor})

    def create(self, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Créer une catégorie tarifaire.

        ``POST /categories`` (operationId ``createCategory``).

        **Accès** : `catalog.write` · Clé partenaire : non Crée une catégorie tarifaire ; la réponse porte déjà ses prix de saison (`seasonPrices`). **Refus** : nom déjà porté par une autre catégorie, casse ignorée → 409 `ALREADY_EXISTS`.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", "/categories", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def delete(self, category_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer une catégorie tarifaire.

        ``DELETE /categories/{categoryId}`` (operationId ``deleteCategory``).

        **Accès** : `catalog.write` · Clé partenaire : non Supprime une catégorie tarifaire ; 204 sans corps. **Refus** : catégorie encore rattachée à un véhicule (archivé compris), une caution ou une franchise → 409 `RESOURCE_IN_USE`, avec toutes les causes dans `blockers` (`VEHICLES`, `DEPOSITS`, `DEDUCTIBLES`) ; rien n’est supprimé.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("DELETE", f"/categories/{category_id}", idempotency_key=idempotency_key, idempotency_required=False)

    def get(self, category_id: str) -> Any:
        """Lire une catégorie tarifaire.

        ``GET /categories/{categoryId}`` (operationId ``getCategory``).

        **Accès** : `catalog.read` Renvoie une catégorie tarifaire, dans la même représentation que la liste.
        """
        return self._client.request("GET", f"/categories/{category_id}")

    def update(self, category_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier une catégorie tarifaire.

        ``PATCH /categories/{categoryId}`` (operationId ``updateCategory``).

        **Accès** : `catalog.write` · Clé partenaire : non Modifie une catégorie tarifaire : seuls les champs envoyés changent. - Un nouveau `baseDailyPriceHT` met aussitôt à jour `seasonPrices`. - `overageRatePerKmHT: null` supprime le prix de dépassement. **Refus** : nom déjà porté par une autre catégorie, casse ignorée → 409 `ALREADY_EXISTS`.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PATCH", f"/categories/{category_id}", json=body, idempotency_key=idempotency_key, idempotency_required=False)


class CustomersResource:
    """Opérations sur ``/customers``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, email: Any = None, company_registration_number: Any = None) -> Any:
        """Lister les clients.

        ``GET /customers`` (operationId ``listCustomers``).

        **Accès** : `customers.read` · Clé partenaire : non Liste les clients du loueur, fiches anonymisées comprises. Tri : `lastName` (raison sociale d’une société), puis `id`. **Filtres** : `email`, égalité exacte, casse ignorée, plusieurs fiches possibles (sociétés, une fiche particulier par `partnerCode`) ; `companyRegistrationNumber`, égalité exacte.

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``email`` → ``email``, ``company_registration_number`` → ``companyRegistrationNumber``.
        """
        return self._client.request("GET", "/customers", params={"limit": limit, "cursor": cursor, "email": email, "companyRegistrationNumber": company_registration_number})

    def create(self, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Créer un client.

        ``POST /customers`` (operationId ``createCustomer``).

        **Accès** : `customers.write` · Clé partenaire : non Crée un client, particulier (`firstName`, `lastName`) ou société (`isCompany: true`, `companyName`). **Refus** : champ de l’autre type de client → 400 `not_applicable` ; société française sans `companyRegistrationNumber` → 400 `required` ; email déjà pris par un particulier du même `partnerCode` → 409 `ALREADY_EXISTS`.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", "/customers", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def delete(self, customer_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer un client.

        ``DELETE /customers/{customerId}`` (operationId ``deleteCustomer``).

        **Accès** : `customers.delete` · Clé partenaire : non Supprime définitivement un client, avec ses documents, notes et pièces d’identité ; 204 sans corps. **Refus** : client lié à une location (titulaire ou conducteur, tout statut), une facture, un devis commercial ou un incident → 409 `RESOURCE_IN_USE` avec toutes les causes ; rien n’est supprimé. Pour effacer ses données personnelles, demandez son anonymisation au support Lexio (contact@lexio.rent).

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("DELETE", f"/customers/{customer_id}", idempotency_key=idempotency_key, idempotency_required=False)

    def get(self, customer_id: str) -> Any:
        """Lire un client.

        ``GET /customers/{customerId}`` (operationId ``getCustomer``).

        **Accès** : `customers.read` · Clé partenaire : non Renvoie un client visible par la clé, dans la même représentation que la liste, sans historique de locations. Hors du périmètre de la clé : 404.
        """
        return self._client.request("GET", f"/customers/{customer_id}")

    def update(self, customer_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier un client.

        ``PATCH /customers/{customerId}`` (operationId ``updateCustomer``).

        **Accès** : `customers.write` · Clé partenaire : non Modifie un client en Merge Patch : champ omis inchangé, `null` efface ; `address` est fusionnée champ par champ, `address: null` la retire. Pour changer de type (`isCompany`), fournissez dans la même requête les noms du nouveau type. **Refus** : fiche anonymisée → 409 `CUSTOMER_ANONYMIZED` ; email de particulier déjà pris → 409 `ALREADY_EXISTS`. **Effet** : une adresse complétée émet ensuite les factures en attente des locations payées.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PATCH", f"/customers/{customer_id}", json=body, idempotency_key=idempotency_key, idempotency_required=False)


class DeductiblesResource:
    """Opérations sur ``/deductibles``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, is_active: Any = None) -> Any:
        """Lister les franchises.

        ``GET /deductibles`` (operationId ``listDeductibles``).

        **Accès** : `catalog.read` Liste les franchises de l’organisation. Tri : `name`, puis `id`. `isActive` filtre (`true` ou `false`, omis : tous).

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``is_active`` → ``isActive``.
        """
        return self._client.request("GET", "/deductibles", params={"limit": limit, "cursor": cursor, "isActive": is_active})

    def create(self, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Créer une franchise.

        ``POST /deductibles`` (operationId ``createDeductible``).

        **Accès** : `catalog.write` · Clé partenaire : non Crée une franchise, réservée à une catégorie (`categoryId`) ou valable pour toutes. Omis : `isActive` true, `isDefault` false. **Refus** - `isDefault: true` avec `isActive: false` → 400 `mutually_exclusive` (un défaut est toujours actif) ; - `categoryId` ou `linkedDepositId` inconnu → 422 `REFERENCE_NOT_FOUND` ; - caution liée désactivée ou d’une autre catégorie → 422 `REFERENCE_INACTIVE`.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", "/deductibles", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def delete(self, deductible_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer une franchise.

        ``DELETE /deductibles/{deductibleId}`` (operationId ``deleteDeductible``).

        **Accès** : `catalog.write` · Clé partenaire : non Supprime une franchise ; 204 sans corps. **Refus** - franchise par défaut → 409 `DEFAULT_ITEM_REQUIRED` : désignez d’abord un autre défaut, ou retirez-lui ce statut (`isDefault: false`) ; - franchise portée par une location ou un devis saisi dans Lexio → 409 `RESOURCE_IN_USE` (`RENTALS`, `SALES_QUOTES` ; un devis `POST /quotes` ne bloque pas) : désactivez-la plutôt.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("DELETE", f"/deductibles/{deductible_id}", idempotency_key=idempotency_key, idempotency_required=False)

    def get(self, deductible_id: str) -> Any:
        """Lire une franchise.

        ``GET /deductibles/{deductibleId}`` (operationId ``getDeductible``).

        **Accès** : `catalog.read` Renvoie une franchise.
        """
        return self._client.request("GET", f"/deductibles/{deductible_id}")

    def update(self, deductible_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier une franchise.

        ``PATCH /deductibles/{deductibleId}`` (operationId ``updateDeductible``).

        **Accès** : `catalog.write` · Clé partenaire : non Modifie une franchise : seuls les champs envoyés changent ; `null` efface `description`, `categoryId` et `linkedDepositId` ; `price` est remplacé en entier. `isDefault` suit les règles de la [création](https://docs.lexio.rent/api-reference/catalogue/create-deductible). La caution liée n’est contrôlée que si `linkedDepositId` ou `categoryId` change. **Refus** - désactiver la franchise par défaut sans envoyer `isDefault: false` → 409 `DEFAULT_ITEM_REQUIRED` ; - référence inconnue → 422 `REFERENCE_NOT_FOUND` ; - caution liée désactivée ou d’une a

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PATCH", f"/deductibles/{deductible_id}", json=body, idempotency_key=idempotency_key, idempotency_required=False)


class DepositsResource:
    """Opérations sur ``/deposits``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, is_active: Any = None) -> Any:
        """Lister les cautions.

        ``GET /deposits`` (operationId ``listDeposits``).

        **Accès** : `catalog.read` · Fonctionnalité d’abonnement : `pricing.deposits` ([plans](https://docs.lexio.rent/authentification)) Liste les cautions de l’organisation. Tri : `displayOrder`, `name`, puis `id`. `isActive` filtre (`true` ou `false`, omis : tous).

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``is_active`` → ``isActive``.
        """
        return self._client.request("GET", "/deposits", params={"limit": limit, "cursor": cursor, "isActive": is_active})

    def create(self, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Créer une caution.

        ``POST /deposits`` (operationId ``createDeposit``).

        **Accès** : `catalog.write` · Fonctionnalité d’abonnement : `pricing.deposits` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Crée une caution, réservée à une catégorie (`categoryId`) ou valable pour toutes ; `method` est requis. Omis : `isActive` true, `isDefault` false, `displayOrder` 0. **Refus** - `isDefault: true` avec `isActive: false` → 400 `mutually_exclusive` (un défaut est toujours actif) ; - `categoryId` inconnu → 422 `REFERENCE_NOT_FOUND`.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", "/deposits", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def delete(self, deposit_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer une caution.

        ``DELETE /deposits/{depositId}`` (operationId ``deleteDeposit``).

        **Accès** : `catalog.write` · Fonctionnalité d’abonnement : `pricing.deposits` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Supprime une caution ; 204 sans corps. **Refus** - caution par défaut → 409 `DEFAULT_ITEM_REQUIRED` : désignez d’abord un autre défaut, ou retirez-lui ce statut (`isDefault: false`) ; - caution portée par une location ou un devis saisi dans Lexio, ou liée à une franchise → 409 `RESOURCE_IN_USE` (`RENTALS`, `SALES_QUOTES`, `DEDUCTIBLES` ; un devis `POST /quotes` ne bloque pas) : désactivez-la plutôt.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("DELETE", f"/deposits/{deposit_id}", idempotency_key=idempotency_key, idempotency_required=False)

    def get(self, deposit_id: str) -> Any:
        """Lire une caution.

        ``GET /deposits/{depositId}`` (operationId ``getDeposit``).

        **Accès** : `catalog.read` · Fonctionnalité d’abonnement : `pricing.deposits` ([plans](https://docs.lexio.rent/authentification)) Renvoie une caution.
        """
        return self._client.request("GET", f"/deposits/{deposit_id}")

    def update(self, deposit_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier une caution.

        ``PATCH /deposits/{depositId}`` (operationId ``updateDeposit``).

        **Accès** : `catalog.write` · Fonctionnalité d’abonnement : `pricing.deposits` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Modifie une caution : seuls les champs envoyés changent ; `null` efface `description` et `categoryId`. `isDefault` suit les règles de la [création](https://docs.lexio.rent/api-reference/catalogue/create-deposit). **Refus** - désactiver la caution par défaut sans envoyer `isDefault: false` → 409 `DEFAULT_ITEM_REQUIRED` ; - `categoryId` inconnu → 422 `REFERENCE_NOT_FOUND`.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PATCH", f"/deposits/{deposit_id}", json=body, idempotency_key=idempotency_key, idempotency_required=False)


class DurationDiscountsResource:
    """Opérations sur ``/duration-discounts``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self) -> Any:
        """Lister les remises de durée.

        ``GET /duration-discounts`` (operationId ``listDurationDiscounts``).

        **Accès** : `pricing.read` · Fonctionnalité d’abonnement : `pricing.discounts` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Renvoie la grille complète des remises de durée, actives ou non, triée par `minRentalDays` puis `id` ; `nextCursor` vaut toujours `null`. **Application** - Une remise s’applique quand la durée facturée (`period.billedDays`) est dans [`minRentalDays`, `maxRentalDays`], qu’elle est active, et que [`GET /pricing-settings`](https://docs.lexio.rent/api-reference/tarification/get-pricing-settings) donne `durationDiscounts.isEnabled` et `isAvailable
        """
        return self._client.request("GET", "/duration-discounts")

    def create(self, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Créer une remise de durée.

        ``POST /duration-discounts`` (operationId ``createDurationDiscount``).

        **Accès** : `pricing.write` · Fonctionnalité d’abonnement : `pricing.discounts` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Crée une remise de durée ; `maxRentalDays` est requis, `null` pour une plage sans borne haute. **Refus** : `maxRentalDays` < `minRentalDays` → 400 `too_small` ; plage qui chevauche une autre remise, même inactive → 409 `RANGE_OVERLAP` (`conflictingId` et ses bornes).

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", "/duration-discounts", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def delete(self, duration_discount_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer une remise de durée.

        ``DELETE /duration-discounts/{durationDiscountId}`` (operationId ``deleteDurationDiscount``).

        **Accès** : `pricing.write` · Fonctionnalité d’abonnement : `pricing.discounts` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Supprime une remise de durée ; 204 sans corps. Rien ne bloque la suppression : les locations existantes gardent le taux figé à leur création.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("DELETE", f"/duration-discounts/{duration_discount_id}", idempotency_key=idempotency_key, idempotency_required=False)

    def get(self, duration_discount_id: str) -> Any:
        """Lire une remise de durée.

        ``GET /duration-discounts/{durationDiscountId}`` (operationId ``getDurationDiscount``).

        **Accès** : `pricing.read` · Fonctionnalité d’abonnement : `pricing.discounts` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Renvoie une remise de durée.
        """
        return self._client.request("GET", f"/duration-discounts/{duration_discount_id}")

    def update(self, duration_discount_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier une remise de durée.

        ``PATCH /duration-discounts/{durationDiscountId}`` (operationId ``updateDurationDiscount``).

        **Accès** : `pricing.write` · Fonctionnalité d’abonnement : `pricing.discounts` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Modifie une remise de durée : seuls les champs envoyés changent ; `maxRentalDays: null` ouvre la plage. Les bornes sont contrôlées sur la remise obtenue. **Refus** : `maxRentalDays` < `minRentalDays` → 400 `too_small` ; chevauchement avec une autre remise, même inactive → 409 `RANGE_OVERLAP`.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PATCH", f"/duration-discounts/{duration_discount_id}", json=body, idempotency_key=idempotency_key, idempotency_required=False)


class EventsResource:
    """Opérations sur ``/events``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, start: Any = None, types: Any = None) -> Any:
        """Lister les changements des locations.

        ``GET /events`` (operationId ``listEvents``).

        **Accès** : `rentals.read` Flux ordonné des changements de locations : `rental.created`, `rental.updated`, `rental.cancelled` et `rental.deleted`. Les événements sont minces : relisez la location par `GET /rentals/{rentalId}`. Une clé partenaire ne reçoit que ceux de ses locations. **Lecture** : sans `cursor`, le flux part des 29 derniers jours (`start=EARLIEST`) ou du moment présent (`start=LATEST`). Traitez les événements dans l’ordre de la page, puis reprenez au `nextCursor` tel quel : sur ce flux, il n’est jamais nul, même sur une page vide. **Refus** : curseur de plus de 30 jours → 410 `C

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``start`` → ``start``, ``types`` → ``types``.
        """
        return self._client.request("GET", "/events", params={"limit": limit, "cursor": cursor, "start": start, "types": types})


class LeadTimeTiersResource:
    """Opérations sur ``/lead-time-tiers``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self) -> Any:
        """Lister les paliers de délai de réservation.

        ``GET /lead-time-tiers`` (operationId ``listLeadTimeTiers``).

        **Accès** : `pricing.read` · Fonctionnalité d’abonnement : `pricing.leadtime` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Renvoie les paliers de délai de réservation (10 au plus), actifs ou non, triés par `minLeadDays` puis `id` ; `nextCursor` vaut toujours `null`. **Application** - Le délai se compte en jours civils du loueur, de la date du devis (sans devis : de la création de la location) au jour du départ. S’applique le palier actif dont la plage le contient ; les plages ne se chevauchent pas. - Il ne compte que si [`GET /pricing-settings`](https://docs.lexio
        """
        return self._client.request("GET", "/lead-time-tiers")

    def get(self, lead_time_tier_id: str) -> Any:
        """Lire un palier de délai de réservation.

        ``GET /lead-time-tiers/{leadTimeTierId}`` (operationId ``getLeadTimeTier``).

        **Accès** : `pricing.read` · Fonctionnalité d’abonnement : `pricing.leadtime` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Renvoie un palier de délai de réservation, avec un `priceFactor` par saison.
        """
        return self._client.request("GET", f"/lead-time-tiers/{lead_time_tier_id}")

    def update(self, lead_time_tier_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier un palier de délai de réservation.

        ``PATCH /lead-time-tiers/{leadTimeTierId}`` (operationId ``updateLeadTimeTier``).

        **Accès** : `pricing.write` · Fonctionnalité d’abonnement : `pricing.leadtime` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Modifie un palier de délai : seuls les champs envoyés changent ; `maxLeadDays: null` ouvre la plage. La création et la suppression de paliers se font dans Lexio. - `priceFactors` est remplacé en entier et couvre exactement les saisons de l’organisation : saison en double ou manquante → 400, saison inconnue → 422 `REFERENCE_NOT_FOUND`. Chaque `priceFactor` va de 0,1 à 5, 2 décimales au plus. - Bornes contrôlées sur le palier obtenu : `maxLeadD

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PATCH", f"/lead-time-tiers/{lead_time_tier_id}", json=body, idempotency_key=idempotency_key, idempotency_required=False)


class LocationsResource:
    """Opérations sur ``/locations``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, is_active: Any = None, type: Any = None) -> Any:
        """Lister les lieux.

        ``GET /locations`` (operationId ``listLocations``).

        **Accès** : `catalog.read` Liste les lieux de départ et de retour du loueur (agence, aéroport, gare…). Tri : `displayOrder`, `name`, puis `id`. Les lieux se gèrent dans Lexio (lecture seule ici). Pour en utiliser un : `{ "locationId": "…" }` en `pickupLocation` ou `returnLocation` d’une location ; désactivé, il est refusé (422 `REFERENCE_INACTIVE`). Une adresse libre `{ "address": "…" }` reste possible. **Filtres** : `isActive` (`true` ou `false`, omis = tous) ; `type`, plusieurs valeurs séparées par des virgules.

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``is_active`` → ``isActive``, ``type`` → ``type``.
        """
        return self._client.request("GET", "/locations", params={"limit": limit, "cursor": cursor, "isActive": is_active, "type": type})


class MaintenanceOperationsResource:
    """Opérations sur ``/maintenance-operations``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self) -> Any:
        """Lister le catalogue des opérations d’entretien.

        ``GET /maintenance-operations`` (operationId ``listMaintenanceOperations``).

        **Accès** : `maintenance.read` · Clé partenaire : non Liste le catalogue des opérations d’entretien de l’organisation, désactivées comprises. Tri : `displayOrder`, `name`, puis `operationCode`. Un entretien ne peut porter que les codes à `isRecordable: true`.
        """
        return self._client.request("GET", "/maintenance-operations")


class MaintenanceRecordsResource:
    """Opérations sur ``/maintenance-records``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, vehicle_id: Any = None, from_: Any = None, to: Any = None) -> Any:
        """Lister les entretiens.

        ``GET /maintenance-records`` (operationId ``listMaintenanceRecords``).

        **Accès** : `maintenance.read` · Clé partenaire : non Liste les entretiens de l’organisation, contrôles techniques exclus. Tri : `interventionDate` décroissant, puis `id`. - `from` et `to` bornent le jour de l’intervention, inclus ; `to` antérieur à `from` donne une liste vide, un `vehicleId` inconnu aussi. - Une facture impossible à signer fait échouer la requête : 503 `SERVICE_UNAVAILABLE`, à renvoyer.

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``vehicle_id`` → ``vehicleId``, ``from_`` → ``from``, ``to`` → ``to``.
        """
        return self._client.request("GET", "/maintenance-records", params={"limit": limit, "cursor": cursor, "vehicleId": vehicle_id, "from": from_, "to": to})

    def create(self, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Enregistrer un entretien.

        ``POST /maintenance-records`` (operationId ``createMaintenanceRecord``).

        **Accès** : `maintenance.write` · Fonctionnalité d’abonnement : `maintenance.manage` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Enregistre une intervention sur un véhicule. - Le compteur du véhicule est relevé à `odometerKm` s’il est plus élevé, dans la même transaction ; il ne baisse jamais (pour le corriger : [`PATCH /vehicles/{vehicleId}`](https://docs.lexio.rent/api-reference/flotte/update-vehicle)). - Une opération désactivée (`isEnabled: false`) est acceptée, un véhicule archivé aussi. - L’échéance de chaque opération repart de sa dernière intervention : u

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", "/maintenance-records", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def delete(self, maintenance_record_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer un entretien.

        ``DELETE /maintenance-records/{maintenanceRecordId}`` (operationId ``deleteMaintenanceRecord``).

        **Accès** : `maintenance.write` · Fonctionnalité d’abonnement : `maintenance.manage` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Supprime un entretien ; 204 sans corps. Le blocage de planning qui lui est lié est supprimé avec lui : le véhicule redevient disponible sur ces dates. La facture est effacée ; le compteur du véhicule ne change pas. Un contrôle technique répond 404 : il se supprime dans Lexio.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("DELETE", f"/maintenance-records/{maintenance_record_id}", idempotency_key=idempotency_key, idempotency_required=False)

    def get(self, maintenance_record_id: str) -> Any:
        """Lire un entretien.

        ``GET /maintenance-records/{maintenanceRecordId}`` (operationId ``getMaintenanceRecord``).

        **Accès** : `maintenance.read` · Clé partenaire : non Renvoie un entretien, dans la même représentation que la liste. Une facture impossible à signer (stockage indisponible) répond 503 `SERVICE_UNAVAILABLE`, à renvoyer.
        """
        return self._client.request("GET", f"/maintenance-records/{maintenance_record_id}")

    def update(self, maintenance_record_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier un entretien.

        ``PATCH /maintenance-records/{maintenanceRecordId}`` (operationId ``updateMaintenanceRecord``).

        **Accès** : `maintenance.write` · Fonctionnalité d’abonnement : `maintenance.manage` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Corrige un entretien : seuls les champs envoyés changent et l’identifiant reste le même. Mêmes règles qu’à la [création](https://docs.lexio.rent/api-reference/entretien/create-maintenance-record) ; le véhicule ne change pas (`vehicleId` → 400 `unknown_field`), `{}` → 400 `empty_patch`. Un nouvel `odometerKm` relève le compteur du véhicule s’il est plus élevé, jamais à la baisse.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PATCH", f"/maintenance-records/{maintenance_record_id}", json=body, idempotency_key=idempotency_key, idempotency_required=False)


class MileagePackagesResource:
    """Opérations sur ``/mileage-packages``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, is_active: Any = None) -> Any:
        """Lister les forfaits kilométriques.

        ``GET /mileage-packages`` (operationId ``listMileagePackages``).

        **Accès** : `catalog.read` · Fonctionnalité d’abonnement : `mileage.basic` ([plans](https://docs.lexio.rent/authentification)) Liste les forfaits kilométriques de l’organisation. Tri : `displayOrder`, `name`, puis `id`. `isActive` filtre (`true` ou `false`, omis : tous).

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``is_active`` → ``isActive``.
        """
        return self._client.request("GET", "/mileage-packages", params={"limit": limit, "cursor": cursor, "isActive": is_active})

    def create(self, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Créer un forfait kilométrique.

        ``POST /mileage-packages`` (operationId ``createMileagePackage``).

        **Accès** : `catalog.write` · Fonctionnalité d’abonnement : `mileage.basic` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Crée un forfait kilométrique. Omis : `isActive` true, `isDefault` false, `displayOrder` 0. **Refus** : `isDefault: true` avec `isActive: false` → 400 `mutually_exclusive` (un défaut est toujours actif).

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", "/mileage-packages", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def delete(self, mileage_package_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer un forfait kilométrique.

        ``DELETE /mileage-packages/{mileagePackageId}`` (operationId ``deleteMileagePackage``).

        **Accès** : `catalog.write` · Fonctionnalité d’abonnement : `mileage.basic` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Supprime un forfait kilométrique ; 204 sans corps. **Refus** - forfait par défaut → 409 `DEFAULT_ITEM_REQUIRED` : désignez d’abord un autre défaut, ou retirez-lui ce statut (`isDefault: false`) ; - forfait porté par une location ou un devis saisi dans Lexio → 409 `RESOURCE_IN_USE` (`RENTALS`, `SALES_QUOTES` ; un devis `POST /quotes` ne bloque pas) : désactivez-le plutôt.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("DELETE", f"/mileage-packages/{mileage_package_id}", idempotency_key=idempotency_key, idempotency_required=False)

    def get(self, mileage_package_id: str) -> Any:
        """Lire un forfait kilométrique.

        ``GET /mileage-packages/{mileagePackageId}`` (operationId ``getMileagePackage``).

        **Accès** : `catalog.read` · Fonctionnalité d’abonnement : `mileage.basic` ([plans](https://docs.lexio.rent/authentification)) Renvoie un forfait kilométrique.
        """
        return self._client.request("GET", f"/mileage-packages/{mileage_package_id}")

    def update(self, mileage_package_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier un forfait kilométrique.

        ``PATCH /mileage-packages/{mileagePackageId}`` (operationId ``updateMileagePackage``).

        **Accès** : `catalog.write` · Fonctionnalité d’abonnement : `mileage.basic` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Modifie un forfait kilométrique : seuls les champs envoyés changent ; `price` et `tiers` sont remplacés en entier. `isDefault` suit les règles de la [création](https://docs.lexio.rent/api-reference/catalogue/create-mileage-package). **Refus** : désactiver le forfait par défaut sans envoyer `isDefault: false` → 409 `DEFAULT_ITEM_REQUIRED`.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PATCH", f"/mileage-packages/{mileage_package_id}", json=body, idempotency_key=idempotency_key, idempotency_required=False)


class OptionsResource:
    """Opérations sur ``/options``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, is_active: Any = None) -> Any:
        """Lister les options.

        ``GET /options`` (operationId ``listOptions``).

        **Accès** : `catalog.read` · Fonctionnalité d’abonnement : `pricing.options` ([plans](https://docs.lexio.rent/authentification)) Liste les options de l’organisation (siège bébé, conducteur additionnel…). Tri : `displayOrder`, `name`, puis `id`. `isActive` filtre (`true` ou `false`, omis : tous).

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``is_active`` → ``isActive``.
        """
        return self._client.request("GET", "/options", params={"limit": limit, "cursor": cursor, "isActive": is_active})

    def create(self, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Créer une option.

        ``POST /options`` (operationId ``createOption``).

        **Accès** : `catalog.write` · Fonctionnalité d’abonnement : `pricing.options` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Crée une option. **Règles** - `price.maxAmountHT` plafonne le prix par exemplaire sur la location : interdit avec `unit: RENTAL`, jamais inférieur à `amountHT`, `null` (pas 0) pour ne pas plafonner. - `maxQuantity` ne se fixe que sur une option `STANDARD` (sinon 400 `not_applicable`). - `youngDriverAgeThreshold` est requis pour une option `YOUNG_DRIVER`, refusé pour les autres. - Omis : `maxQuantity` et `stockCount` valent 1, `availableMonths`

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", "/options", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def delete(self, option_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer une option.

        ``DELETE /options/{optionId}`` (operationId ``deleteOption``).

        **Accès** : `catalog.write` · Fonctionnalité d’abonnement : `pricing.options` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Supprime une option jamais vendue ; 204 sans corps. **Refus** : option vendue au moins une fois → 409 `RESOURCE_IN_USE` (`RENTALS`) : désactivez-la plutôt (`isActive: false`).

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("DELETE", f"/options/{option_id}", idempotency_key=idempotency_key, idempotency_required=False)

    def get(self, option_id: str) -> Any:
        """Lire une option.

        ``GET /options/{optionId}`` (operationId ``getOption``).

        **Accès** : `catalog.read` · Fonctionnalité d’abonnement : `pricing.options` ([plans](https://docs.lexio.rent/authentification)) Renvoie une option. `imageUrls` porte une URL signée valable une heure.
        """
        return self._client.request("GET", f"/options/{option_id}")

    def update(self, option_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier une option.

        ``PATCH /options/{optionId}`` (operationId ``updateOption``).

        **Accès** : `catalog.write` · Fonctionnalité d’abonnement : `pricing.options` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Modifie une option : seuls les champs envoyés changent ; `price` est fusionné champ par champ et ses règles portent sur le prix obtenu (voir la [création](https://docs.lexio.rent/api-reference/catalogue/create-option)). Repasser une option en `STANDARD` sans envoyer `maxQuantity` la remet à 1. **Refus** : passer à `ADDITIONAL_DRIVER` ou `YOUNG_DRIVER` alors qu’une telle option existe → 409 `ALREADY_EXISTS` ; quitter `ADDITIONAL_DRIVER` ou `YOU

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PATCH", f"/options/{option_id}", json=body, idempotency_key=idempotency_key, idempotency_required=False)


class OrganizationResource:
    """Opérations sur ``/organization``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def get(self) -> Any:
        """Lire l’organisation et la clé.

        ``GET /organization`` (operationId ``getOrganization``).

        **Accès** : toute clé valide Renvoie les réglages du loueur qui gouvernent les dates et les prix, et la clé qui appelle. À lire une fois au démarrage : devise et nombre de décimales des montants ([Montants et TVA](https://docs.lexio.rent/montants-et-tva)), fuseau des heures de location, TVA, horaires et règles de réservation imposés aux clés partenaires.
        """
        return self._client.request("GET", "/organization")


class PricingSettingsResource:
    """Opérations sur ``/pricing-settings``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def get(self) -> Any:
        """Lire les réglages tarifaires.

        ``GET /pricing-settings`` (operationId ``getPricingSettings``).

        **Accès** : `pricing.read` · Clé partenaire : non Renvoie l’activation de chaque règle de prix et ses valeurs, défauts compris. Lecture seule : ces réglages se modifient dans Lexio. **Application** - Une règle ne s’applique que si `isEnabled` et `isAvailable` valent `true`. `isAvailable` suit le plan, ou une ouverture hors plan par Lexio : `pricing.seasons` pour `seasonalPricing` et `weekendSurcharge`, `pricing.discounts` pour `durationDiscounts` et `shortDurationSurcharge`, `pricing.leadtime` pour `leadTimePricing`. - Week-end : s’applique si le jour du départ, ou un jour atteint de 24 h en 2
        """
        return self._client.request("GET", "/pricing-settings")


class QuotesResource:
    """Opérations sur ``/quotes``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def create(self, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Créer un devis.

        ``POST /quotes`` (operationId ``createQuote``).

        **Accès** : `quotes.write` Fige 24 h (`expiresAt`) le prix d’un véhicule sur une période, sans le réserver : la disponibilité est revérifiée à la création de la location. Avec `vehicleId`, `startAt` et `endAt` seuls, `totalTTC` est celui de `GET /availability`. Options : quantité de 1 à `choices.options[].maxBookableQuantity`. **Refus** - `VEHICLE_UNAVAILABLE` : véhicule non réservable. - `OPTION_UNAVAILABLE` : stock d’option insuffisant. - `BOOKING_RULE_VIOLATION` : règles de réservation (clé partenaire). - `DISCOUNT_CAP_EXCEEDED` : remise au-delà du plafond de la clé ou sous un total nul. - 

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", "/quotes", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def get(self, quote_id: str) -> Any:
        """Lire un devis.

        ``GET /quotes/{quoteId}`` (operationId ``getQuote``).

        **Accès** : `offers.read` Le devis tel que créé, expiré compris : lisez `expiresAt`, `consumedAt` et `rentalId` (location créée avec lui). `choices` reste celui du calcul. Devis inconnu, d’une autre organisation ou d’un autre code partenaire, ou effacé (24 h après `expiresAt`) : `404`. La lecture ne renvoie jamais `QUOTE_EXPIRED`.
        """
        return self._client.request("GET", f"/quotes/{quote_id}")


class RentalsResource:
    """Opérations sur ``/rentals``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, status: Any = None, vehicle_id: Any = None, customer_id: Any = None, category_id: Any = None, partner_reference: Any = None, partner_code: Any = None, number: Any = None, from_: Any = None, to: Any = None) -> Any:
        """Lister les locations.

        ``GET /rentals`` (operationId ``listRentals``).

        **Accès** : `rentals.read` Les locations, chacune dans la représentation de `GET /rentals/{rentalId}`, triées par `period.startAt` décroissant puis `id`. **Filtres**, combinables, en égalité exacte : `status` (valeurs séparées par des virgules), `vehicleId`, `customerId`, `categoryId`, `partnerReference`, `number`. Un identifiant inconnu donne une liste vide. `from` et `to` (`YYYY-MM-DD`, inclus) sont des jours (fuseau du loueur) : une location est retenue si sa période contractuelle ou réelle les chevauche ; une location `IN_PROGRESS` non rendue court jusqu’à son retour. `from` postérieur à `

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``status`` → ``status``, ``vehicle_id`` → ``vehicleId``, ``customer_id`` → ``customerId``, ``category_id`` → ``categoryId``, ``partner_reference`` → ``partnerReference``, ``partner_code`` → ``partnerCode``, ``number`` → ``number``, ``from_`` → ``from``, ``to`` → ``to``.
        """
        return self._client.request("GET", "/rentals", params={"limit": limit, "cursor": cursor, "status": status, "vehicleId": vehicle_id, "customerId": customer_id, "categoryId": category_id, "partnerReference": partner_reference, "partnerCode": partner_code, "number": number, "from": from_, "to": to})

    def create(self, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Créer une location.

        ``POST /rentals`` (operationId ``createRental``).

        **Accès** : `rentals.write` Crée une location `RESERVED` (tout ou rien), au prix d’un devis (`quoteId`) ou au prix du moment. **Obligatoire** : `customerId` (clé interne) ou `customer`, jamais les deux ; puis `quoteId` seul, ou `vehicleId`, `startAt`, `endAt` avec les règles et défauts de `POST /quotes`. Un `customer` déjà connu n’est complété que sur ses champs vides. Sans devis, aucune majoration jeune conducteur n’est appliquée : pour un conducteur concerné, passez par `POST /quotes` avec `driverBirthDate`, puis `quoteId`. **Refus** (sans devis, s’ajoutent ceux de `POST /quotes`) - `REFEREN

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("POST", "/rentals", json=body, idempotency_key=idempotency_key, idempotency_required=True)

    def delete(self, rental_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer une location.

        ``DELETE /rentals/{rentalId}`` (operationId ``deleteRental``).

        **Accès** : `rentals.delete` · Clé partenaire : non Supprime définitivement une location `RESERVED` ou `CANCELLED` (204). Préférez [cancel](https://docs.lexio.rent/api-reference/locations/cancel-rental), qui garde l’historique. **Refus** - `RENTAL_STATUS_NOT_ALLOWED` (`action: DELETE`) : autre statut, revérifié à l’écriture. Une demande `PENDING_APPROVAL` se refuse par annulation. - `RESOURCE_IN_USE` : rien n’est supprimé ; `blockers` liste toutes les causes : `INVOICES` (facture émise, même remboursée), `PAYMENTS_HELD` (net encaissé hors caution ; `count` = paiements et remboursements validés

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("DELETE", f"/rentals/{rental_id}", idempotency_key=idempotency_key, idempotency_required=True)

    def get(self, rental_id: str) -> Any:
        """Lire une location.

        ``GET /rentals/{rentalId}`` (operationId ``getRental``).

        **Accès** : `rentals.read` La location dans sa représentation unique, la même que celle des écritures. **Montants** dans `currency`, la devise figée à la création. `totalHT`, `vatAmount` et `totalTTC` font foi, avec `totalTTC − totalHT = vatAmount` ; la somme des `lines` leur est égale, sauf écart possible sur une location ancienne. `totalTTC` est le montant de la pièce, inchangé par une annulation ; `balance.totalTTC` est l’exigible, 0 sur une location `CANCELLED`. Caution et franchise ne sont jamais dans ces totaux. **Solde** : `balance.paidAmount` = paiements validés − remboursements validé
        """
        return self._client.request("GET", f"/rentals/{rental_id}")

    def update(self, rental_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier les notes et les lieux.

        ``PATCH /rentals/{rentalId}`` (operationId ``updateRental``).

        **Accès** : `rentals.write` Modifie `notes`, `pickupLocation` et `returnLocation` en Merge Patch (`application/json` ou `application/merge-patch+json`) : omis = inchangé, `null` efface, un lieu se remplace entier. Réponse : la location relue ; ni le prix, ni le statut, ni le titulaire ne changent. **Statuts** : `notes` toujours modifiable ; lieux en `PENDING_APPROVAL` et `RESERVED`, lieu de retour seul en `IN_PROGRESS` ; ailleurs → 409 `RENTAL_STATUS_NOT_ALLOWED` (`action: EDIT_LOCATIONS`, champ pointé). **Refus** : `{}` → 400 `empty_patch` ; `""` → 400 `empty_string` ; lieu inconnu → 422 `REF

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("PATCH", f"/rentals/{rental_id}", json=body, idempotency_key=idempotency_key, idempotency_required=True)

    def list_amendments(self, rental_id: str, *, limit: Any = None, cursor: Any = None) -> Any:
        """Lister les avenants d’une location.

        ``GET /rentals/{rentalId}/amendments`` (operationId ``listRentalAmendments``).

        **Accès** : `rentals.read` Liste les avenants d’une location, quel que soit leur statut, du plus récent au plus ancien (`createdAt` décroissant, puis `id`). - Les montants sont les totaux de la location avant et après l’avenant. Tant que la signature est en attente (`PENDING`, `SENT`, `VIEWED`), `newTotalHT` et `newTotalTTC` suivent le total à jour de la location, ou le total d’avant l’avenant suivant s’il en existe un en attente ou signé ; ensuite ils sont figés (pour `SIGNED`, ceux signés par le client). - `document` est une URL signée valable une heure. Les données de signature ne sont jama

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``.
        """
        return self._client.request("GET", f"/rentals/{rental_id}/amendments", params={"limit": limit, "cursor": cursor})

    def cancel(self, rental_id: str, body: Mapping[str, Any], *, dry_run: Any = None, idempotency_key: str | None = None) -> Any:
        """Annuler une location ou refuser une demande.

        ``POST /rentals/{rentalId}/cancel`` (operationId ``cancelRental``).

        **Accès** : `rentals.write` Annule une location `RESERVED` ou refuse une demande `PENDING_APPROVAL` (tout ou rien). **Effets** - `CANCELLED`, code promo rendu, factures brouillon supprimées, un avoir du restant de chaque facture émise (`effects.cancellation.creditNotes`). - `PENDING_APPROVAL` : email de refus au client, avec le motif, notification au loueur, puis libération de l’autorisation Stripe une fois l’annulation enregistrée (`effects.paymentAuthorizationRelease`). - Aucun frais : `effects.cancellation.refundDueAmount` est le remboursement à enregistrer par [POST …/payments](https://doc

        Paramètres de requête : ``dry_run`` → ``dryRun``.

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("POST", f"/rentals/{rental_id}/cancel", params={"dryRun": dry_run}, json=body, idempotency_key=idempotency_key, idempotency_required=True)

    def change_coverage(self, rental_id: str, body: Mapping[str, Any], *, dry_run: Any = None, idempotency_key: str | None = None) -> Any:
        """Changer la couverture d’une location.

        ``POST /rentals/{rentalId}/change-coverage`` (operationId ``changeRentalCoverage``).

        **Accès** : `rentals.write` Change le forfait kilométrique, la franchise ou la caution d’une location `RESERVED` ou `IN_PROGRESS` : au moins un des trois champs. **Règles** - Franchise changée sans `depositId` : caution recalculée (`effects.depositResolution`). - Élément changé : tarif du jour ; inchangé : prix gardé. Un élément offert dans Lexio et remplacé perd la gratuité. - Mêmes identifiants : 200 sans effet. Sur `IN_PROGRESS`, avenant si le changement est significatif (`effects.amendment`). **Refus** - `REFERENCE_NOT_FOUND` : identifiant inconnu. - `REFERENCE_INACTIVE` : nouvel élément d

        Paramètres de requête : ``dry_run`` → ``dryRun``.

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("POST", f"/rentals/{rental_id}/change-coverage", params={"dryRun": dry_run}, json=body, idempotency_key=idempotency_key, idempotency_required=True)

    def change_customer(self, rental_id: str, body: Mapping[str, Any], *, dry_run: Any = None, idempotency_key: str | None = None) -> Any:
        """Changer le titulaire d’une location.

        ``POST /rentals/{rentalId}/change-customer`` (operationId ``changeRentalCustomer``).

        **Accès** : `rentals.write` Change le titulaire d’une location `RESERVED` (en cours : dans Lexio), par `customerId` (clé interne) ou `customer` (`effects.customerResolution`), jamais les deux. Aucun email envoyé. **Conducteurs** : un titulaire particulier devient conducteur principal ; s’il remplace une société, le conducteur principal de celle-ci devient conducteur additionnel facturé. Une société qui remplace un particulier le garde en conducteur principal. Options conducteur recalculées (`priceChange` possible). **Refus** - `REFERENCE_NOT_FOUND`, `REFERENCE_INACTIVE` : `customerId` inconnu,

        Paramètres de requête : ``dry_run`` → ``dryRun``.

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("POST", f"/rentals/{rental_id}/change-customer", params={"dryRun": dry_run}, json=body, idempotency_key=idempotency_key, idempotency_required=True)

    def change_vehicle(self, rental_id: str, body: Mapping[str, Any], *, dry_run: Any = None, idempotency_key: str | None = None) -> Any:
        """Changer le véhicule d’une location.

        ``POST /rentals/{rentalId}/change-vehicle`` (operationId ``changeRentalVehicle``).

        **Accès** : `rentals.write` Remplace le véhicule d’une location `RESERVED` ou `IN_PROGRESS`. Sur `IN_PROGRESS`, `odometers` est requis (compteur du véhicule rendu, puis du remis). **Choix tarifaires** : `KEEP_ORIGINAL_PRICE` toujours ; `BREAKDOWN` et `UNAVAILABLE` ajoutent `APPLY_LOWER_PRICE` si le véhicule est moins cher ; `CUSTOMER_REQUEST` ajoute `APPLY_NEW_PRICE` si les prix diffèrent, et `APPLY_PRORATA` en cours de location. `effects.availablePricingChoices` fait foi, total compris ; sans `pricingChoice`, le choix recommandé s’applique. **Refus** - `RENTAL_STATUS_NOT_ALLOWED` : `odometers

        Paramètres de requête : ``dry_run`` → ``dryRun``.

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("POST", f"/rentals/{rental_id}/change-vehicle", params={"dryRun": dry_run}, json=body, idempotency_key=idempotency_key, idempotency_required=True)

    def get_contract(self, rental_id: str) -> Any:
        """Lire le contrat d’une location.

        ``GET /rentals/{rentalId}/contract`` (operationId ``getRentalContract``).

        **Accès** : `rentals.read` Renvoie le contrat de location en vigueur : l’exemplaire signé au départ, sinon celui du retour. Lecture seule : l’appel ne génère ni ne remplace aucun document. - `NOT_ISSUED` tant qu’aucun contrat n’est disponible (location pas encore partie, ou contrat de départ en cours de génération) : `document` et `issuedAt` valent `null`. - `AVAILABLE` : `document` est une URL signée valable une heure, à ne pas stocker.
        """
        return self._client.request("GET", f"/rentals/{rental_id}/contract")

    def list_inspections(self, rental_id: str) -> Any:
        """Lister les états des lieux d’une location.

        ``GET /rentals/{rentalId}/inspections`` (operationId ``listRentalInspections``).

        **Accès** : `rentals.read` Renvoie les états des lieux d’une location : au plus deux éléments, `DEPARTURE` puis `RETURN`. Un état des lieux pas encore fait est absent : liste vide sur une location `RESERVED`, départ seul sur `IN_PROGRESS`. Même forme que l’`inspection` envoyée au [départ](https://docs.lexio.rent/api-reference/depart-et-retour/pick-up-rental) et au [retour](https://docs.lexio.rent/api-reference/depart-et-retour/return-rental). Les dommages du départ portent un `id` à citer dans `confirmedDepartureDamageIds` au retour ; un dommage historique saisi en texte libre a un `id` `null`
        """
        return self._client.request("GET", f"/rentals/{rental_id}/inspections")

    def list_invoices(self, rental_id: str, *, limit: Any = None, cursor: Any = None, type: Any = None) -> Any:
        """Lister les factures et avoirs d’une location.

        ``GET /rentals/{rentalId}/invoices`` (operationId ``listRentalInvoices``).

        **Accès** : `rentals.read` Liste les factures et avoirs émis pour une location, du plus récent au plus ancien (`createdAt` décroissant, puis `id`) ; `type` filtre. - Un brouillon n’est jamais listé : une liste vide veut dire qu’aucune pièce n’est émise. - Montants dans `currency`, la devise de la pièce ; ceux d’un avoir sont négatifs et `creditedInvoiceId` désigne la facture créditée. Voir [Montants et TVA](https://docs.lexio.rent/montants-et-tva). - `document` est une URL signée valable une heure : rappelez la liste pour en obtenir une neuve.

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``type`` → ``type``.
        """
        return self._client.request("GET", f"/rentals/{rental_id}/invoices", params={"limit": limit, "cursor": cursor, "type": type})

    def remove_option(self, rental_id: str, option_id: str, *, dry_run: Any = None, expected_total_ttc: Any = None, overpayment_resolution: Any = None, idempotency_key: str | None = None) -> Any:
        """Retirer une option d’une location.

        ``DELETE /rentals/{rentalId}/options/{optionId}`` (operationId ``removeRentalOption``).

        **Accès** : `rentals.write` · Fonctionnalité d’abonnement : `pricing.options` ([plans](https://docs.lexio.rent/authentification)) Retire toute la ligne d’une option standard d’une location `RESERVED` ou `IN_PROGRESS` (204). Sans corps : les paramètres passent en query (inconnu → 400 `unknown_field`). **Prix** : le montant retiré est le prix vendu. Sur `IN_PROGRESS`, avenant si le changement est significatif (`effects.amendment`). **Refus** - 404 `resource: OPTION` : option inconnue ; `resource: RENTAL_OPTION` : absente de la location. - 400 `not_applicable` : option conducteur. - `INVOICE_FINA

        Paramètres de requête : ``dry_run`` → ``dryRun``, ``expected_total_ttc`` → ``expectedTotalTTC``, ``overpayment_resolution`` → ``overpaymentResolution``.

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("DELETE", f"/rentals/{rental_id}/options/{option_id}", params={"dryRun": dry_run, "expectedTotalTTC": expected_total_ttc, "overpaymentResolution": overpayment_resolution}, idempotency_key=idempotency_key, idempotency_required=True)

    def set_option_quantity(self, rental_id: str, option_id: str, body: Mapping[str, Any], *, dry_run: Any = None, idempotency_key: str | None = None) -> Any:
        """Fixer la quantité d’une option.

        ``PUT /rentals/{rentalId}/options/{optionId}`` (operationId ``setRentalOptionQuantity``).

        **Accès** : `rentals.write` · Fonctionnalité d’abonnement : `pricing.options` ([plans](https://docs.lexio.rent/authentification)) Fixe la quantité finale (1 à 100) d’une option standard sur une location `RESERVED` ou `IN_PROGRESS` : ligne créée si besoin, même quantité sans effet. Pour retirer la ligne : `DELETE`. **Prix** : unités gardées à leur prix, ajoutées au tarif du jour, retirées au dernier prix vendu. Sur `IN_PROGRESS`, avenant si le changement est significatif (`effects.amendment`). **Refus** - 404 `resource: OPTION` : option inconnue ; 400 `not_applicable` : option conducteur (gérée

        Paramètres de requête : ``dry_run`` → ``dryRun``.

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("PUT", f"/rentals/{rental_id}/options/{option_id}", params={"dryRun": dry_run}, json=body, idempotency_key=idempotency_key, idempotency_required=True)

    def list_payments(self, rental_id: str, *, limit: Any = None, cursor: Any = None) -> Any:
        """Lister les paiements d’une location.

        ``GET /rentals/{rentalId}/payments`` (operationId ``listRentalPayments``).

        **Accès** : `rentals.read` Encaissements, cautions et remboursements de la location, du plus récent au plus ancien (`paidAt` décroissant, puis `id`). Montants dans `currency`, la devise de la location ; `amount` est positif, le sens est porté par `type`, sauf un mouvement de caution au retour (`DEPOSIT` négatif : restitution ou retenue décidée dans Lexio). Seules les lignes `VALIDATED` hors `DEPOSIT` comptent dans le solde (`balance` de `GET /rentals/{rentalId}`) : `PAYMENT` en plus, `REFUND` en moins.

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``.
        """
        return self._client.request("GET", f"/rentals/{rental_id}/payments", params={"limit": limit, "cursor": cursor})

    def create_payment(self, rental_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Enregistrer un paiement.

        ``POST /rentals/{rentalId}/payments`` (operationId ``createRentalPayment``).

        **Accès** : `payments.write` ou `payments.refund` Enregistre, validé, un encaissement (`PAYMENT`) ou une caution (`DEPOSIT`), scope `payments.write`, ou un remboursement (`REFUND`), scope `payments.refund`. Clé partenaire : `PAYMENT` `STRIPE` seulement (sinon 400 `not_applicable`). **Stripe** : PaymentIntent `succeeded` du compte Stripe du loueur, dans la devise de la location, pour exactement `amount` ; sa metadata ne vise ni une autre location (`rentalId`) ni une autre organisation (`orgId`, `organizationId`) et, pour une clé partenaire, porte ce `rentalId` ou votre `partnerCode`. **Refus** 

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("POST", f"/rentals/{rental_id}/payments", json=body, idempotency_key=idempotency_key, idempotency_required=True)

    def delete_payment(self, rental_id: str, payment_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer un paiement saisi par erreur.

        ``DELETE /rentals/{rentalId}/payments/{paymentId}`` (operationId ``deleteRentalPayment``).

        **Accès** : `payments.refund` · Clé partenaire : non Corrige une saisie erronée : la transaction est supprimée, rien n’est émis. Admis sur une location `RESERVED`, `IN_PROGRESS` ou `COMPLETED`, sinon 409 `RENTAL_STATUS_NOT_ALLOWED`. **Refus** - Paiement inconnu ou d’une autre location → 404 (`resource: PAYMENT`). - Paiement validé encaissé par Stripe (`stripePaymentIntentId`) → 409 `PAYMENT_PROVIDER_MANAGED` : il se rembourse chez Stripe ; Lexio l’enregistre à réception de l’événement Stripe, sauf si l’équipe du loueur l’a déjà saisi à la main. - Mouvement d’une caution sécurisée en ligne (`me

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("DELETE", f"/rentals/{rental_id}/payments/{payment_id}", idempotency_key=idempotency_key, idempotency_required=True)

    def get_payment(self, rental_id: str, payment_id: str) -> Any:
        """Lire un paiement.

        ``GET /rentals/{rentalId}/payments/{paymentId}`` (operationId ``getRentalPayment``).

        **Accès** : `rentals.read` Même représentation que la liste. Un `paymentId` qui n’appartient pas à `rentalId` répond 404 (`resource: PAYMENT`), même s’il appartient à une autre de vos locations ; une location hors du périmètre de la clé répond 404 (`resource: RENTAL`).
        """
        return self._client.request("GET", f"/rentals/{rental_id}/payments/{payment_id}")

    def create_photo_uploads(self, rental_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Préparer le téléversement de photos.

        ``POST /rentals/{rentalId}/photo-uploads`` (operationId ``createRentalPhotoUploads``).

        **Accès** : `rentals.operate` · Clé partenaire : non Étape 1 sur 3 du dépôt de photos d’état des lieux, photo du compteur comprise (vue `DASHBOARD`). Pour chaque élément (phase, vue, format, taille exacte), la réponse donne, dans l’ordre de `items`, un `uploadId` et une URL signée. **Suite** 1. Envoyez chaque fichier par `PUT` sur `url`, avec exactement les `headers` fournis, avant `expiresAt` (15 minutes). 2. Enregistrez-les par [`POST /rentals/{rentalId}/photos`](https://docs.lexio.rent/api-reference/depart-et-retour/register-rental-photos) avant `registrationExpiresAt` (24 h). **Statuts adm

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", f"/rentals/{rental_id}/photo-uploads", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def list_photos(self, rental_id: str, *, limit: Any = None, cursor: Any = None, phase: Any = None) -> Any:
        """Lister les photos d’état des lieux d’une location.

        ``GET /rentals/{rentalId}/photos`` (operationId ``listRentalPhotos``).

        **Accès** : `rentals.read` Liste les photos de départ, de retour et de sinistre d’une location, de la plus récente à la plus ancienne (`takenAt` décroissant, puis `id`) ; `phase` filtre. Les pièces jointes ajoutées dans Lexio ne sont jamais listées. - `original` et `annotated` sont des URL signées valables une heure : rappelez la liste ou [`GET …/photos/{photoId}`](https://docs.lexio.rent/api-reference/depart-et-retour/get-rental-photo) pour en obtenir de neuves. - Tant que `processingStatus` vaut `PENDING`, `original` peut encore changer et `annotated` vaut `null`. - Une URL impossible à sign

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``phase`` → ``phase``.
        """
        return self._client.request("GET", f"/rentals/{rental_id}/photos", params={"limit": limit, "cursor": cursor, "phase": phase})

    def register_photos(self, rental_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Enregistrer des photos téléversées.

        ``POST /rentals/{rentalId}/photos`` (operationId ``registerRentalPhotos``).

        **Accès** : `rentals.operate` · Clé partenaire : non Étape 3 sur 3 : enregistre, tout ou rien, les fichiers envoyés par `PUT`, désignés par `uploadId` ; `data` suit l’ordre de `items`. **Contrôles** : chaque fichier est vérifié avant toute écriture (reçu, taille, format réel). Un élément refusé fait refuser le lot en 422 `UPLOAD_INVALID`, un `errors[]` par élément : `upload_incomplete` (refaites le `PUT`), `upload_expired` (préparez un nouveau téléversement), `too_small`, `too_big`, `invalid_format`, `upload_conflict` (déjà enregistré autrement), `duplicate`. `uploadId` inconnu ou retiré depui

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", f"/rentals/{rental_id}/photos", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def delete_photo(self, rental_id: str, photo_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer une photo d’état des lieux.

        ``DELETE /rentals/{rentalId}/photos/{photoId}`` (operationId ``deleteRentalPhoto``).

        **Accès** : `rentals.operate` · Clé partenaire : non Supprime une photo d’état des lieux ; 204 sans corps. La suppression est tracée au journal d’audit ; les fichiers sont purgés ensuite s’ils ne servent à aucune autre photo. **Statuts admis** : `IN_PROGRESS` et `COMPLETED` ; `RESERVED` pour une photo `DEPARTURE`. Sinon 409 `RENTAL_STATUS_NOT_ALLOWED`. **404** (`resource: PHOTO`) : photo inconnue, d’une autre location, pièce jointe ajoutée dans Lexio, ou suppression renvoyée sans `Idempotency-Key` : traitez ce 404 comme un succès s’il s’agit d’un renvoi. Le contrat de départ est figé au départ

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("DELETE", f"/rentals/{rental_id}/photos/{photo_id}", idempotency_key=idempotency_key, idempotency_required=False)

    def get_photo(self, rental_id: str, photo_id: str) -> Any:
        """Lire une photo d’état des lieux.

        ``GET /rentals/{rentalId}/photos/{photoId}`` (operationId ``getRentalPhoto``).

        **Accès** : `rentals.read` Renvoie une photo, dans la même représentation que la liste : pour attendre `processingStatus` `READY` ou obtenir de nouvelles URL signées. Interrogez avec un délai croissant (1 s, 2 s, 4 s…) et un plafond de quelques minutes : une photo dont l’image annotée n’a pas pu être produite peut rester `PENDING`, `original` restant lisible. **Refus** : photo inconnue, d’une autre location ou pièce jointe ajoutée dans Lexio → 404 (`resource: PHOTO`) ; location hors du périmètre de la clé → 404 (`resource: RENTAL`) ; URL signée impossible à produire (stockage indisponible) → 5
        """
        return self._client.request("GET", f"/rentals/{rental_id}/photos/{photo_id}")

    def pick_up(self, rental_id: str, body: Mapping[str, Any], *, dry_run: Any = None, idempotency_key: str | None = None) -> Any:
        """Enregistrer le départ.

        ``POST /rentals/{rentalId}/pickup`` (operationId ``pickUpRental``).

        **Accès** : `rentals.operate` · Clé partenaire : non Remet le véhicule au client : la location `RESERVED` passe `IN_PROGRESS` avec état des lieux de départ, compteur, signature, consentement aux CGL et paiements du comptoir (tout ou rien). Des `payments` exigent aussi le scope `payments.write`. **Refus** - `PAYMENT_EXCEEDS_DUE` : encaissements au-delà du reste dû (caution non comprise). - `PAYMENT_PROVIDER_MANAGED` : caution alors qu’une caution est sécurisée en ligne, ou caution `SWIKLY` quand ce moyen est connecté chez le loueur. - 400 `not_applicable` : empreinte (`isPreAuthorization`) sans

        Paramètres de requête : ``dry_run`` → ``dryRun``.

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("POST", f"/rentals/{rental_id}/pickup", params={"dryRun": dry_run}, json=body, idempotency_key=idempotency_key, idempotency_required=True)

    def reschedule(self, rental_id: str, body: Mapping[str, Any], *, dry_run: Any = None, idempotency_key: str | None = None) -> Any:
        """Changer les dates d’une location.

        ``POST /rentals/{rentalId}/reschedule`` (operationId ``rescheduleRental``).

        **Accès** : `rentals.write` Déplace le départ, le retour ou les deux, aux prix figés à la création de la location (tarif, prix des saisons, coefficients et taux), les options à leur prix de vente ; la saison de chaque jour suit le calendrier actuel. L’heure envoyée est retenue telle quelle. **Règles** - `RESERVED` : départ dans le passé → 400 `date_in_past`. - `IN_PROGRESS` : seule la fin bouge, après maintenant et le départ réel ; avenant si le changement est significatif (`effects.amendment`). **Refus** - `RENTAL_STATUS_NOT_ALLOWED` : `startAt` sur `IN_PROGRESS`. - `BOOKING_RULE_VIOLATION` (

        Paramètres de requête : ``dry_run`` → ``dryRun``.

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("POST", f"/rentals/{rental_id}/reschedule", params={"dryRun": dry_run}, json=body, idempotency_key=idempotency_key, idempotency_required=True)

    def return_(self, rental_id: str, body: Mapping[str, Any], *, dry_run: Any = None, idempotency_key: str | None = None) -> Any:
        """Enregistrer le retour.

        ``POST /rentals/{rentalId}/return`` (operationId ``returnRental``).

        **Accès** : `rentals.operate` · Clé partenaire : non Clôt une location `IN_PROGRESS` : elle passe `COMPLETED` avec état des lieux de retour, compteur, signature, frais, dépassement kilométrique, paiements et, si le loueur facture au retour, facture (tout ou rien). Facture refusée faute de données : brouillon dans Lexio (`effects.invoice` null). **Calculs** : Lexio applique le dépassement kilométrique, km cumulés sur les véhicules successifs (`effects.mileageOverage`) ; énergie manquante et retard sont seulement proposés (`effects.suggestedCharges`), à renvoyer dans `charges`. **Ordre** : frais

        Paramètres de requête : ``dry_run`` → ``dryRun``.

        ``Idempotency-Key`` : obligatoire côté API, générée automatiquement si absente.
        """
        return self._client.request("POST", f"/rentals/{rental_id}/return", params={"dryRun": dry_run}, json=body, idempotency_key=idempotency_key, idempotency_required=True)


class SeasonCalendarResource:
    """Opérations sur ``/season-calendar``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list_months(self) -> Any:
        """Lister les mois du calendrier.

        ``GET /season-calendar`` (operationId ``listSeasonCalendarMonths``).

        **Accès** : `pricing.read` · Fonctionnalité d’abonnement : `pricing.seasons` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Renvoie les 12 mois du calendrier des saisons, de 1 à 12 : un gabarit annuel, sans année, qui vaut chaque année.
        """
        return self._client.request("GET", "/season-calendar")

    def get_month(self, month: str) -> Any:
        """Lire un mois du calendrier des saisons.

        ``GET /season-calendar/{month}`` (operationId ``getSeasonCalendarMonth``).

        **Accès** : `pricing.read` · Fonctionnalité d’abonnement : `pricing.seasons` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Renvoie l’affectation jour par jour d’un mois (1 à 12) du calendrier des saisons.
        """
        return self._client.request("GET", f"/season-calendar/{month}")

    def replace_month(self, month: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Remplacer un mois du calendrier des saisons.

        ``PUT /season-calendar/{month}`` (operationId ``replaceSeasonCalendarMonth``).

        **Accès** : `pricing.write` · Fonctionnalité d’abonnement : `pricing.seasons` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Remplace en bloc les affectations jour → saison d’un mois. Le changement vaut aussitôt pour les devis futurs de tous les canaux de vente du loueur : ne modifiez pas ce gabarit sans année pour un cas ponctuel (hausse d’un jour, fête mobile comme Pâques) ; avec une clé interne, ajoutez plutôt un frais libre (`charges`, type `SURCHARGE`) au devis ou à la location. **Refus** (rien n’est écrit) : jour manquant, en double ou hors du mois → 400 ; `se

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PUT", f"/season-calendar/{month}", json=body, idempotency_key=idempotency_key, idempotency_required=False)


class SeasonsResource:
    """Opérations sur ``/seasons``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self) -> Any:
        """Lister les saisons.

        ``GET /seasons`` (operationId ``listSeasons``).

        **Accès** : `pricing.read` · Fonctionnalité d’abonnement : `pricing.seasons` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Liste les saisons tarifaires de l’organisation (10 au plus). Tri : `displayOrder`, `name`, puis `slug`. Le prix journalier HT d’une catégorie en saison se lit dans `seasonPrices` de [`GET /categories`](https://docs.lexio.rent/api-reference/catalogue/list-categories) (`baseDailyPriceHT` × `priceFactor`, arrondi) ; le [calendrier des saisons](https://docs.lexio.rent/api-reference/tarification/list-season-calendar-months) dit quelle saison s’appli
        """
        return self._client.request("GET", "/seasons")

    def get(self, slug: str) -> Any:
        """Lire une saison.

        ``GET /seasons/{slug}`` (operationId ``getSeason``).

        **Accès** : `pricing.read` · Fonctionnalité d’abonnement : `pricing.seasons` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Renvoie une saison tarifaire, identifiée par son `slug`.
        """
        return self._client.request("GET", f"/seasons/{slug}")

    def update(self, slug: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier une saison.

        ``PATCH /seasons/{slug}`` (operationId ``updateSeason``).

        **Accès** : `pricing.write` · Fonctionnalité d’abonnement : `pricing.seasons` ([plans](https://docs.lexio.rent/authentification)) · Clé partenaire : non Modifie le nom, la description, le rang ou le `priceFactor` d’une saison ; le `slug` est immuable, et les saisons se créent dans Lexio. Un nouveau `priceFactor` met aussitôt à jour `seasonPrices` de toutes les catégories. Seuls les devis futurs suivent le changement.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PATCH", f"/seasons/{slug}", json=body, idempotency_key=idempotency_key, idempotency_required=False)


class VehicleBlocksResource:
    """Opérations sur ``/vehicle-blocks``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, from_: Any = None, to: Any = None, vehicle_id: Any = None, type: Any = None) -> Any:
        """Lister les blocages de planning.

        ``GET /vehicle-blocks`` (operationId ``listVehicleBlocks``).

        **Accès** : `vehicles.read` · Clé partenaire : non Liste les indisponibilités posées sur les véhicules (réparation, nettoyage, usage personnel…), qui les rendent non réservables (`BLOCKED` dans [`GET /availability`](https://docs.lexio.rent/api-reference/offre/list-availability)). Lecture seule : les blocages se posent, se modifient et se lèvent dans Lexio. - `from` et `to` (requis) sont des jours du loueur (son fuseau), inclus : un blocage est renvoyé s’il chevauche cette fenêtre. 92 jours au plus et `from` ≤ `to`, sinon 400 sur `/to`. - `vehicleId` et `type` acceptent plusieurs valeurs séparé

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``from_`` → ``from``, ``to`` → ``to``, ``vehicle_id`` → ``vehicleId``, ``type`` → ``type``.
        """
        return self._client.request("GET", "/vehicle-blocks", params={"limit": limit, "cursor": cursor, "from": from_, "to": to, "vehicleId": vehicle_id, "type": type})


class VehiclesResource:
    """Opérations sur ``/vehicles``."""

    def __init__(self, client: "Lexio") -> None:
        self._client = client

    def list(self, *, limit: Any = None, cursor: Any = None, is_active: Any = None, is_archived: Any = None, status: Any = None, vehicle_type: Any = None, category_id: Any = None) -> Any:
        """Lister les véhicules.

        ``GET /vehicles`` (operationId ``listVehicles``).

        **Accès** : `vehicles.read` · Clé partenaire : non Liste la flotte de l’organisation, véhicules archivés compris sauf avec `isArchived=false` (`true` : archivés seulement). Tri : `displayOrder`, puis `id`. `isBookable` dit si le véhicule peut être réservé en général ; sa disponibilité sur une période se lit dans [`GET /availability`](https://docs.lexio.rent/api-reference/offre/list-availability).

        Paramètres de requête : ``limit`` → ``limit``, ``cursor`` → ``cursor``, ``is_active`` → ``isActive``, ``is_archived`` → ``isArchived``, ``status`` → ``status``, ``vehicle_type`` → ``vehicleType``, ``category_id`` → ``categoryId``.
        """
        return self._client.request("GET", "/vehicles", params={"limit": limit, "cursor": cursor, "isActive": is_active, "isArchived": is_archived, "status": status, "vehicleType": vehicle_type, "categoryId": category_id})

    def create(self, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Créer un véhicule.

        ``POST /vehicles`` (operationId ``createVehicle``).

        **Accès** : `vehicles.write` · Clé partenaire : non Ajoute un véhicule à la flotte ; aucune valeur n’est inventée. **Champs requis par le profil** (sinon 400 `required`) - voiture : `doors`, `transmission`, `registrationDate`, et `fuelCapacityLiters` hors électrique ; - deux-roues : `transmission` en thermique, `batteryCapacityKwh` en électrique. Une plaque ou un numéro de série est requis ; un champ non applicable au profil, ou un équipement hors famille ou énergie → 400 `not_applicable`. **Refus** - plaque déjà prise (casse, espaces et tirets ignorés) ou numéro de série déjà pris (casse igno

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", "/vehicles", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def delete(self, vehicle_id: str, *, idempotency_key: str | None = None) -> Any:
        """Supprimer un véhicule.

        ``DELETE /vehicles/{vehicleId}`` (operationId ``deleteVehicle``).

        **Accès** : `vehicles.delete` · Clé partenaire : non Supprime définitivement un véhicule sans historique, avec ses documents, images et positions GPS ; 204 sans corps. **Refus** : véhicule lié à une location (tout statut), un incident, une contravention, un entretien, une vérification planifiée dans Lexio ou un blocage de planning → 409 `RESOURCE_IN_USE`, chaque cause et son nombre dans `blockers` (`RENTALS`, `INCIDENTS`, `CONTRAVENTIONS`, `MAINTENANCE_RECORDS`, `VEHICLE_CHECKS`, `VEHICLE_BLOCKS`). Rien n’est supprimé : archivez-le plutôt ([`POST /vehicles/{vehicleId}/archive`](https://docs.le

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("DELETE", f"/vehicles/{vehicle_id}", idempotency_key=idempotency_key, idempotency_required=False)

    def get(self, vehicle_id: str) -> Any:
        """Lire un véhicule.

        ``GET /vehicles/{vehicleId}`` (operationId ``getVehicle``).

        **Accès** : `vehicles.read` · Clé partenaire : non Renvoie un véhicule, dans la même représentation que la liste. Un véhicule archivé reste lisible.
        """
        return self._client.request("GET", f"/vehicles/{vehicle_id}")

    def update(self, vehicle_id: str, body: Mapping[str, Any], *, idempotency_key: str | None = None) -> Any:
        """Modifier un véhicule.

        ``PATCH /vehicles/{vehicleId}`` (operationId ``updateVehicle``).

        **Accès** : `vehicles.write` · Clé partenaire : non Modifie un véhicule en Merge Patch : champ omis inchangé, `null` efface un champ facultatif. Panne : `status: BREAKDOWN`. Retrait temporaire : `isActive: false` (sort aussi du décompte d’abonnement). Sortie définitive : [archiver](https://docs.lexio.rent/api-reference/flotte/archive-vehicle). - `null` sur un champ exigé par le profil (ex. `doors` d’une voiture) → 400 `required` ; sur `brand`, `model`, `vehicleType`, `fuelType`, `seats`, `odometerKm`, `isActive`, `status` ou `equipment` → 400 `null_not_allowed`. - Changer `vehicleType` ou `fue

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("PATCH", f"/vehicles/{vehicle_id}", json=body, idempotency_key=idempotency_key, idempotency_required=False)

    def archive(self, vehicle_id: str, *, idempotency_key: str | None = None) -> Any:
        """Archiver un véhicule.

        ``POST /vehicles/{vehicleId}/archive`` (operationId ``archiveVehicle``).

        **Accès** : `vehicles.write` · Clé partenaire : non Retire le véhicule de la flotte active sans perdre son historique : il n’est plus réservable (`ARCHIVED` dans `notBookableReasons`) ni modifiable. Sans corps ; idempotente : un véhicule déjà archivé répond 200 sans changement. **Refus** : location en attente de validation, réservée ou en cours → 409 `RESOURCE_IN_USE` (`blockers` : `ACTIVE_RENTALS`). **Effet** : le nombre de véhicules actifs non archivés fixe le palier d’abonnement Lexio du loueur ; cette opération peut le faire changer.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", f"/vehicles/{vehicle_id}/archive", idempotency_key=idempotency_key, idempotency_required=False)

    def list_maintenance_alerts(self, vehicle_id: str, *, status: Any = None) -> Any:
        """Lister les échéances d’entretien d’un véhicule.

        ``GET /vehicles/{vehicleId}/maintenance-alerts`` (operationId ``listVehicleMaintenanceAlerts``).

        **Accès** : `maintenance.read` · Clé partenaire : non Liste les échéances d’entretien d’un véhicule : une ligne par opération activée et applicable (famille, énergie), contrôle technique compris. - `status` : `OVERDUE` si `remainingKm` ou `remainingDays` est négatif, `UPCOMING` sous 1000 km ou 30 jours restants, `OK` sinon. Le paramètre `status` filtre (valeurs séparées par des virgules). - Tri : `OVERDUE`, `UPCOMING`, `OK`, puis km restants, jours restants et `operationCode`. Liste complète, sans pagination. - `isBlockingRentals` : l’opération en retard rend le véhicule non réservable (`MAINT

        Paramètres de requête : ``status`` → ``status``.
        """
        return self._client.request("GET", f"/vehicles/{vehicle_id}/maintenance-alerts", params={"status": status})

    def unarchive(self, vehicle_id: str, *, idempotency_key: str | None = None) -> Any:
        """Désarchiver un véhicule.

        ``POST /vehicles/{vehicleId}/unarchive`` (operationId ``unarchiveVehicle``).

        **Accès** : `vehicles.write` · Clé partenaire : non Remet le véhicule dans la flotte : il redevient modifiable et `ARCHIVED` quitte `notBookableReasons`. Sans corps ; idempotente : un véhicule non archivé répond 200 sans changement. **Effet** : le nombre de véhicules actifs non archivés fixe le palier d’abonnement Lexio du loueur ; cette opération peut le faire changer.

        ``Idempotency-Key`` : facultative.
        """
        return self._client.request("POST", f"/vehicles/{vehicle_id}/unarchive", idempotency_key=idempotency_key, idempotency_required=False)


RESOURCES = {
    "availability": AvailabilityResource,
    "categories": CategoriesResource,
    "customers": CustomersResource,
    "deductibles": DeductiblesResource,
    "deposits": DepositsResource,
    "duration_discounts": DurationDiscountsResource,
    "events": EventsResource,
    "lead_time_tiers": LeadTimeTiersResource,
    "locations": LocationsResource,
    "maintenance_operations": MaintenanceOperationsResource,
    "maintenance_records": MaintenanceRecordsResource,
    "mileage_packages": MileagePackagesResource,
    "options": OptionsResource,
    "organization": OrganizationResource,
    "pricing_settings": PricingSettingsResource,
    "quotes": QuotesResource,
    "rentals": RentalsResource,
    "season_calendar": SeasonCalendarResource,
    "seasons": SeasonsResource,
    "vehicle_blocks": VehicleBlocksResource,
    "vehicles": VehiclesResource,
}
