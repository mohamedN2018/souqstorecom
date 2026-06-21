#!/usr/bin/env bash
# ------------------------------------------------------------
# One-shot initializer for the SouqStore production stack.
# Database migrations run automatically when each container starts;
# this script seeds the demo data + creates the super-admin.
#
# Run AFTER the stack is up:
#   bash dokploy/init.sh
#
# Override sizes:  PRODUCTS=8000 VENDORS=100 bash dokploy/init.sh
# ------------------------------------------------------------
set -e

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.dokploy.yml}"
# If Dokploy gives the project a name, pass it:  PROJECT=myproj bash dokploy/init.sh
PROJECT_FLAG=""
[ -n "$PROJECT" ] && PROJECT_FLAG="-p $PROJECT"

DC="docker compose $PROJECT_FLAG -f $COMPOSE_FILE"

VENDORS="${VENDORS:-60}"
CUSTOMERS="${CUSTOMERS:-200}"
PRODUCTS="${PRODUCTS:-4000}"

echo "==> waiting for services to be ready ..."
sleep 8

echo "==> seeding accounts (admin + vendors + staff + customers) ..."
$DC exec -T auth    python manage.py seed --customers "$CUSTOMERS" --vendors "$VENDORS"

echo "==> seeding stores + site settings ..."
$DC exec -T vendor  python manage.py seed --vendors "$VENDORS"

echo "==> seeding catalog ($PRODUCTS products, local images) ..."
$DC exec -T catalog python manage.py seed --products "$PRODUCTS" --vendors "$VENDORS"

echo ""
echo "✅ Done. Super-admin: admin@souq.test / Admin12345"
echo "   Demo password for everyone else: Password123"
