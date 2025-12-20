# Deployment (Raspberry Pi 5) — Videoflix

This document describes how to deploy **Videoflix** on a Raspberry Pi 5 (Debian / Raspberry Pi OS) in a production-like setup.

- **Domain (single subdomain):** https://videoflix.selcuk-kocyigit.de
- **Frontend:** Angular build served as static files via Nginx
- **Backend:** Django (Gunicorn) behind Nginx reverse proxy
- **Database:** PostgreSQL (local on the Pi)
- **Queue:** Redis + django-rq (RQ worker as systemd service)
- **Video processing:** ffmpeg (variants + thumbnails)
- **SSL:** Certbot (Let’s Encrypt)

---

## Table of Contents

- [Architecture](#architecture)
- [DNS and Router](#dns-and-router)
- [Server Requirements](#server-requirements)
- [Folder Layout](#folder-layout)
- [Clone Repositories](#clone-repositories)
- [Frontend Build and Deploy](#frontend-build-and-deploy)
- [Backend Setup](#backend-setup)
- [PostgreSQL Setup](#postgresql-setup)
- [Redis Setup](#redis-setup)
- [Environment Variables](#environment-variables)
- [Django Migrations and Static Files](#django-migrations-and-static-files)
- [Systemd Services](#systemd-services)
  - [Gunicorn Service](#gunicorn-service)
  - [RQ Worker Service](#rq-worker-service)
- [Nginx Configuration](#nginx-configuration)
- [SSL with Certbot](#ssl-with-certbot)
- [Quick Checks](#quick-checks)
- [Troubleshooting](#troubleshooting)
  - [Frontend shows 403 Forbidden](#frontend-shows-403-forbidden)
  - [Angular build output is inside browser folder](#angular-build-output-is-inside-browser-folder)
  - [RQ worker fails: ffmpeg not found](#rq-worker-fails-ffmpeg-not-found)
  - [SMTP host not resolvable](#smtp-host-not-resolvable)
- [Suggested Git Commit](#suggested-git-commit)

---

## Architecture

- **Public entry:** `videoflix.selcuk-kocyigit.de` (Nginx)
- **Frontend:** static files in `/var/www/videoflix_frontend`
- **Backend:** Gunicorn on `127.0.0.1:8001`

**Nginx routing**

- `/` → SPA (index.html fallback)
- `/api/` → Gunicorn
- `/admin/` → Gunicorn
- `/static/` → alias to `staticfiles`
- `/media/` → alias to `media`

[↑ Back to Table of Contents](#table-of-contents)

---

## DNS and Router

1. **DNS (All-Inkl)**

   - Create an **A record**: `videoflix` → your **public WAN IP**

2. **Router Port Forwarding**

   - Forward **80 → Pi LAN IP**
   - Forward **443 → Pi LAN IP**

3. **Verify DNS from the Pi**
   - Check current resolution:
     ```bash
     dig +short videoflix.selcuk-kocyigit.de
     ```
   - Optional (use a public resolver to bypass local caching):
     ```bash
     dig @1.1.1.1 +short videoflix.selcuk-kocyigit.de
     ```

[↑ Back to Table of Contents](#table-of-contents)

---

## Server Requirements

- Raspberry Pi 5 (recommended 8GB+ RAM)
- Debian / Raspberry Pi OS
- Nginx
- Python 3 + venv
- PostgreSQL
- Redis
- ffmpeg
- Node.js (for Angular build)
- Certbot (Let’s Encrypt)

[↑ Back to Table of Contents](#table-of-contents)

---

## Folder Layout

Create the directories:

```bash
sudo mkdir -p /var/www/videoflix_frontend
mkdir -p /home/pi/videoflix_backend
mkdir -p /home/pi/videoflix_frontend
```

[↑ Back to Table of Contents](#table-of-contents)

## Clone Repositories

### Clone via Git (recommended):

```bash
cd /home/pi
git clone https://github.com/Seldir193/Videoflix_backend.git videoflix_backend
git clone https://github.com/Seldir193/Videoflix_frontend.git videoflix_frontend
```

### Verify:

```bash
cd /home/pi/videoflix_backend && git status
cd /home/pi/videoflix_frontend && git status
```

## Frontend Build and Deploy

### Install Node.js on the Pi (one-time):

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node -v
npm -v
```

### Build Angular frontend

```bash
cd /home/pi/videoflix_frontend
npm ci
npm run build --configuration production
```

### The build output is created inside dist/.... Check:

```bash
ls -la dist
```

### Most Angular SSR / modern builds output a browser/ folder. If your output is:

```bash
dist/videoflix-ui/browser/
```

[↑ Back to Table of Contents](#table-of-contents)

## Deploy to Nginx web root

### Deploy like this:

```bash
sudo mkdir -p /var/www/videoflix_frontend
rsync -av --delete /home/pi/videoflix_frontend/dist/videoflix-ui/browser/ /var/www/videoflix_frontend/
```

### Verify:

```bash
ls -la /var/www/videoflix_frontend | head -n 20
ls -la /var/www/videoflix_frontend/index.html
```

### Permissions (recommended):

```bash
sudo chown -R www-data:www-data /var/www/videoflix_frontend
sudo find /var/www/videoflix_frontend -type d -exec chmod 755 {} \;
sudo find /var/www/videoflix_frontend -type f -exec chmod 644 {} \;
```

### Reload Nginx (optional)

```bash
sudo nginx -t
sudo systemctl reload nginx
```

[↑ Back to Table of Contents](#table-of-contents)

## Backend Setup

### Create a virtual environment and install requirements:

```bash
cd /home/pi/videoflix_backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Example:

```bash
find . -maxdepth 3 -name settings.py
```

### If you see ./video_backend/settings.py, then:

Django project module: video_backend
Gunicorn target: video_backend.wsgi:application

[↑ Back to Table of Contents](#table-of-contents)

## PostgreSQL Setup

### Install PostgreSQL

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable --now postgresql
```

### Create user + database:

```bash
sudo -u postgres psql
```

### Inside psql:

```sql
CREATE USER videoflix_user WITH PASSWORD 'YOUR_STRONG_PASSWORD';
CREATE DATABASE videoflix_db OWNER videoflix_user;
GRANT ALL PRIVILEGES ON DATABASE videoflix_db TO videoflix_user;
\q
```

Set DB_HOST=127.0.0.1 in .env.

[↑ Back to Table of Contents](#table-of-contents)

## Redis Setup

### Install and enable Redis:

```bash
sudo apt install -y redis-server
sudo systemctl enable --now redis-server
sudo systemctl status redis-server --no-pager
```

### Use local Redis:

Configure Redis in `.env`:

```env
REDIS_LOCATION=redis://127.0.0.1:6379/1
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
```

[↑ Back to Table of Contents](#table-of-contents)

## Environment Variables

Create /home/pi/videoflix_backend/.env:

```bash
nano /home/pi/videoflix_backend/.env
```

### Minimum production keys (example — replace placeholders, do NOT commit secrets):

```env
DEBUG=False
SECRET_KEY=YOUR_RANDOM_SECRET_KEY

ALLOWED_HOSTS=videoflix.selcuk-kocyigit.de,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://videoflix.selcuk-kocyigit.de

DB_NAME=videoflix_db
DB_USER=videoflix_user
DB_PASSWORD=YOUR_DB_PASSWORD
DB_HOST=127.0.0.1
DB_PORT=5432

REDIS_LOCATION=redis://127.0.0.1:6379/1
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0

FRONTEND_PROTOCOL=https
FRONTEND_DOMAIN=videoflix.selcuk-kocyigit.de

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=YOUR_SMTP_HOST
EMAIL_PORT=587
EMAIL_HOST_USER=YOUR_SMTP_USER
EMAIL_HOST_PASSWORD=YOUR_SMTP_PASSWORD
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL="Videoflix <noreply@videoflix.selcuk-kocyigit.de>"
```

### Generate a SECRET_KEY:

```bash
source /home/pi/videoflix_backend/.venv/bin/activate
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Secure the .env:

```bash
sudo chmod 600 /home/pi/videoflix_backend/.env
```

[↑ Back to Table of Contents](#table-of-contents)

## Django Migrations and Static Files

### Run:

```bash
cd /home/pi/videoflix_backend
source .venv/bin/activate

mkdir -p media

python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
```

### Install ffmpeg (if not installed):

```bash
sudo apt install -y ffmpeg
which ffmpeg
```

[↑ Back to Table of Contents](#table-of-contents)

## Systemd Services

### Gunicorn Service

```bash
sudo nano /etc/systemd/system/videoflix.service
```

### Content:

```ini
[Unit]
Description=Videoflix Gunicorn Service
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/videoflix_backend
Environment="PATH=/home/pi/videoflix_backend/.venv/bin"
EnvironmentFile=/home/pi/videoflix_backend/.env
ExecStart=/home/pi/videoflix_backend/.venv/bin/gunicorn video_backend.wsgi:application \
  --bind 127.0.0.1:8001 \
  --workers 3 \
  --timeout 120

[Install]
WantedBy=multi-user.target
```

### Enable + start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now videoflix
sudo systemctl status videoflix --no-pager
```

### Local check:

```bash
curl -I http://127.0.0.1:8001/
```

A 404 on / can be OK if your API routes do not define a root view.
[↑ Back to Table of Contents](#table-of-contents)

## RQ Worker Service

### Create:

```bash
sudo nano /etc/systemd/system/videoflix-rqworker.service
```

### Content (note the PATH includes /usr/bin so ffmpeg is found):

```ini
[Unit]
Description=Videoflix RQ Worker
After=network.target redis-server.service
Wants=redis-server.service

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/videoflix_backend
Environment="PATH=/home/pi/videoflix_backend/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
EnvironmentFile=/home/pi/videoflix_backend/.env
ExecStart=/home/pi/videoflix_backend/.venv/bin/python manage.py rqworker default
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Enable + start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now videoflix-rqworker
sudo systemctl status videoflix-rqworker --no-pager
```

### Logs:

```bash
sudo journalctl -u videoflix-rqworker -f
```

[↑ Back to Table of Contents](#table-of-contents)

## Nginx Configuration

### Create Nginx site:

```bash
sudo nano /etc/nginx/sites-available/videoflix
```

```nginx
server {
    listen 80;
    server_name videoflix.selcuk-kocyigit.de;

    client_max_body_size 120M;

    root /var/www/videoflix_frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/pi/videoflix_backend/staticfiles/;
    }

    location /media/ {
        alias /home/pi/videoflix_backend/media/;
    }
}
```

### Enable:

```bash
sudo ln -sfn /etc/nginx/sites-available/videoflix /etc/nginx/sites-enabled/videoflix
sudo nginx -t
sudo systemctl reload nginx
```

[↑ Back to Table of Contents](#table-of-contents)

## SSL with Certbot

### Install Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Issue certificate:

```bash
sudo certbot --nginx -d videoflix.selcuk-kocyigit.de
```

[↑ Back to Table of Contents](#table-of-contents)

## Quick Checks

```bash
curl -I http://videoflix.selcuk-kocyigit.de
curl -I https://videoflix.selcuk-kocyigit.de
curl -I https://videoflix.selcuk-kocyigit.de/api/
curl -I https://videoflix.selcuk-kocyigit.de/admin/

# optional: static + media checks
curl -I https://videoflix.selcuk-kocyigit.de/static/
curl -I https://videoflix.selcuk-kocyigit.de/media/

sudo systemctl status videoflix --no-pager
sudo systemctl status videoflix-rqworker --no-pager

sudo journalctl -u videoflix -n 80 --no-pager
sudo journalctl -u videoflix-rqworker -n 120 --no-pager
```

[↑ Back to Table of Contents](#table-of-contents)

## Troubleshooting

### Frontend shows 403 Forbidden

Cause: Missing `index.html` in the Nginx web root or wrong file permissions.

Fix:

- Make sure `index.html` exists in `/var/www/videoflix_frontend/`.
- Ensure files are readable by Nginx (`www-data`).

```bash
ls -la /var/www/videoflix_frontend | head -n 20
ls -la /var/www/videoflix_frontend/index.html

sudo chown -R www-data:www-data /var/www/videoflix_frontend
sudo find /var/www/videoflix_frontend -type d -exec chmod 755 {} \;
sudo find /var/www/videoflix_frontend -type f -exec chmod 644 {} \;

sudo nginx -t
sudo systemctl reload nginx
```

[↑ Back to Table of Contents](#table-of-contents)

### Angular build output is inside browser folder

If build output is dist/<app>/browser/, you must deploy that folder to the web root:

```bash
rsync -av --delete dist/<app>/browser/ /var/www/videoflix_frontend/
ls -la /var/www/videoflix_frontend/index.html
```

[↑ Back to Table of Contents](#table-of-contents)

### RQ worker fails: ffmpeg not found

If logs show:

```text
FileNotFoundError: No such file or directory: 'ffmpeg'
```

Fix: Ensure systemd PATH includes /usr/bin in videoflix-rqworker.service (or use /usr/bin/ffmpeg in the task).

```bash
which ffmpeg
ffmpeg -version
sudo systemctl cat videoflix-rqworker | sed -n '1,140p'
```

[↑ Back to Table of Contents](#table-of-contents)

### SMTP host not resolvable

If Django SMTP fails with:

```text
socket.gaierror: Name or service not known
```

Fix: Verify DNS resolution for your SMTP host and ensure the hostname is correct (avoid typos).

```bash
dig +short YOUR_SMTP_HOST A
getent hosts YOUR_SMTP_HOST
```

[↑ Back to Table of Contents](#table-of-contents)

## Suggested Git Commit

If you add this file to your backend repository:

**Summary**
docs: add raspberry pi deployment guide

**Description**
Add production-like Raspberry Pi 5 deployment guide for Videoflix (Nginx + Gunicorn + PostgreSQL + Redis + RQ worker + Certbot).

### Git commands:

```bash
cd /home/pi/videoflix_backend
git status
git add DEPLOYMENT.md
git commit -m "docs: add raspberry pi deployment guide"
git push
```

[↑ Back to Table of Contents](#table-of-contents)
