"""
Deterministic cross-service identifiers.

In a microservices setup there are NO foreign keys across service databases.
To keep demo/seed data consistent (a product in the Catalog service must point
at a vendor that actually exists in the Vendor service), both services derive
vendor UUIDs from the same namespace + index. Same input → same UUID, offline,
with zero coordination between services.

This exact constant + helper is duplicated in the Catalog service on purpose.
"""
import uuid

VENDOR_NAMESPACE = uuid.UUID("11111111-1111-1111-1111-111111111111")


def vendor_id(index: int) -> uuid.UUID:
    return uuid.uuid5(VENDOR_NAMESPACE, f"vendor:{index}")
