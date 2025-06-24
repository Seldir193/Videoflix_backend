#!/bin/sh
set -e

# ------------------------------------------------------------
# 1) DB-Host & -Port sauber aus DATABASE_URL herauslösen
#    BusyBox-Tools, kein "sed -E"
# ------------------------------------------------------------
if [ -n "$DATABASE_URL" ] && [ -z "$DB_HOST" ]; then
  # Beispiel:  postgres://user:pw@ec2-1-2-3-4.compute.amazonaws.com:6543/dbname
  export DB_HOST="$(echo "$DATABASE_URL" | cut -d@ -f2 | cut -d: -f1)"
  export DB_PORT="$(echo "$DATABASE_URL" | rev | cut -d: -f1 | rev | cut -d/ -f1)"
fi

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

echo "⏳ warte auf PostgreSQL unter $DB_HOST:$DB_PORT …"
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
  sleep 1
done
echo "✅ PostgreSQL ist bereit"

# ------------------------------------------------------------
# 2) Django-Hausarbeiten
# ------------------------------------------------------------
python manage.py collectstatic --noinput --ignore=admin --ignore=debug_toolbar \
                               --ignore=import_export --ignore=modeltranslation \
                               --ignore=rest_framework
python manage.py migrate --noinput

# Superuser anlegen (falls noch nicht vorhanden)
python manage.py shell <<'PY'
import os, django
django.setup()
from django.contrib.auth import get_user_model
U=get_user_model()
u=os.environ.get("DJANGO_SUPERUSER_USERNAME","admin")
if not U.objects.filter(username=u).exists():
    U.objects.create_superuser(
        username=u,
        email=os.environ.get("DJANGO_SUPERUSER_EMAIL","admin@example.com"),
        password=os.environ.get("DJANGO_SUPERUSER_PASSWORD","adminpassword")
    )
PY

# ------------------------------------------------------------
# 3) RQ-Worker & Gunicorn
# ------------------------------------------------------------
python manage.py rqworker default &
exec gunicorn video_backend.wsgi:application \
     --bind 0.0.0.0:${PORT:-8000} \
     --workers 3 --worker-class gevent --timeout 300 --keep-alive 5 --no-sendfile
