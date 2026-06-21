#!/usr/bin/env bash
set -e

echo "[catalog] waiting for database at $DB_HOST:$DB_PORT ..."
until python -c "import socket,os; s=socket.socket(); s.settimeout(2); s.connect((os.environ['DB_HOST'], int(os.environ['DB_PORT']))); s.close()" 2>/dev/null; do
  sleep 1
done
echo "[catalog] database is up."

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

if [ "$DJANGO_DEBUG" = "True" ]; then
  exec python manage.py runserver 0.0.0.0:8000
else
  # Catalog uses Channels (WebSockets) → must run an ASGI server (daphne), not WSGI.
  exec daphne -b 0.0.0.0 -p 8000 config.asgi:application
fi
