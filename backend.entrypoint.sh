#!/bin/sh
set -e

# Extrahiere Host/Port aus DATABASE_URL, falls DB_HOST nicht gesetzt ist
if [ -n "$DATABASE_URL" ] && [ -z "$DB_HOST" ]; then
  export DB_HOST=$(echo "$DATABASE_URL" | awk -F[@:/] '{print $4}')
  export DB_PORT=$(echo "$DATABASE_URL" | awk -F[@:/] '{print $5}')
fi

# Warten, bis Postgres bereit ist
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
  echo "PostgreSQL nicht erreichbar – warte 1 s"
  sleep 1
done

echo "PostgreSQL ist bereit - fahre fort..."

# Deine originalen Befehle (ohne wait_for_db)
#python manage.py collectstatic --noinput

python manage.py collectstatic --noinput --ignore=admin --ignore=debug_toolbar --ignore=import_export --ignore=modeltranslation --ignore=rest_framework
python manage.py makemigrations
python manage.py migrate

# Create a superuser using environment variables
# (Dein Superuser-Erstellungs-Code bleibt gleich)
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser '{username}'...")
    # Korrekter Aufruf: username hier übergeben
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists.")
EOF

# Starte den RQ Worker im Hintergrund
python manage.py rqworker default &

#exec gunicorn video_backend.wsgi:application --bind 0.0.0.0:8000
exec gunicorn video_backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers=3 --worker-class=gevent --timeout=300 --keep-alive=5 --no-sendfile
