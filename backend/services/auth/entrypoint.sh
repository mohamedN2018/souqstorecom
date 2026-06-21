#!/usr/bin/env bash
set -e

echo "[auth] waiting for database at $DB_HOST:$DB_PORT ..."
until python -c "import socket,os,sys; s=socket.socket(); s.settimeout(2); s.connect((os.environ['DB_HOST'], int(os.environ['DB_PORT']))); s.close()" 2>/dev/null; do
  sleep 1
done
echo "[auth] database is up."

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

if [ "$DJANGO_DEBUG" = "True" ]; then
  echo "[auth] starting dev server..."
  exec python manage.py runserver 0.0.0.0:8000
else
  echo "[auth] starting gunicorn..."
  exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi
