#!/bin/sh
# ---------------------------------------------------------------------------
# Self-healing Postgres password.
#
# Postgres only applies POSTGRES_PASSWORD on the FIRST init (empty volume).
# If the data volume already exists with a different password — which happens
# whenever the env password changes between deploys — the app can no longer
# authenticate ("password authentication failed for user ...").
#
# This wrapper makes the env the single source of truth: on EVERY start it
# waits for the server to come up, then forces the role's password to match
# POSTGRES_PASSWORD. Local-socket connections inside the container use `trust`
# auth, so no password is needed to perform the reset. Deploys self-heal.
# ---------------------------------------------------------------------------
set -e

# Background: once the server accepts connections, sync the role password.
(
  until pg_isready -U "$POSTGRES_USER" -q 2>/dev/null; do
    sleep 1
  done
  # A second wait covers the brief temp-server phase during first-init.
  sleep 2
  psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
    -c "ALTER USER \"$POSTGRES_USER\" WITH PASSWORD '$POSTGRES_PASSWORD';" \
    >/dev/null 2>&1 || true
  echo "[db] password for role '$POSTGRES_USER' synced with environment."
) &

# Foreground: the real Postgres entrypoint (keeps proper signal handling).
exec docker-entrypoint.sh postgres
