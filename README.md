# 📺 Videoflix – Full-Stack

**Full-stack Netflix clone** powered by **Angular 17.3** (frontend) and  
**Django 4 + PostgreSQL** (API).  
Streams adaptive MP4 variants, remembers the last playback position, sends
activation and reset-password emails, and stores progress every 5 seconds.

| Layer / Purpose    | Tech & Libraries                                               |
| ------------------ | -------------------------------------------------------------- |
| **Frontend**       | Angular 17 · SCSS · RxJS · ngx-translate · Plyr                |
| **Backend API**    | Django 4 · Django REST Framework · djoser · SimpleJWT          |
| **Database**       | PostgreSQL 16                                                  |
| **Queue / Cache**  | Redis 6 · django-rq · django-redis                             |
| **Extras**         | django-modeltranslation · django-import-export · debug-toolbar |
| **Static / Media** | WhiteNoise (dev + prod)                                        |

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Backend – local setup (Windows CMD)](#backend--local-setup-windows-cmd)
3. [Docker Stacks](#docker-stacks)
4. [Production stack](#production-stack)
5. [Port Hints](#port-hints)
6. [Deployment Tips](#deployment-tips)
7. [License](#license)

---

## Project Structure

```text
videoflix-backend/
├── accounts/
│   ├── email.py
│   ├── __init__.py
│   └── …                    # models, signals …
├── tests/
├── users/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── apps.py
├── videos/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py               # FFmpeg transcoding
│   ├── translation.py
│   └── views.py
├── media/                     # uploaded originals & renditions
│   ├── thumbs/
│   └── videos/                # preview images
├── static/                    # created by collectstatic (WhiteNoise / Nginx)
├── staticfiles/
├── templates/
│   └── djoser/email/
│       ├── activation.html
│       ├── activation.txt
│       ├── password_reset.html
│       └── password_reset.txt
├── video_backend/                 # Django project root
│   ├── settings.py
│   ├── settings_test.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── env/                       # (optional) local virtual-env
├── Dockerfile.backend
├── backend.entrypoint.sh
├── conftest.py
├── .dockerignore
├── .env              (prod variables)
├── .env.template     (sample)
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── pytest.ini
└── README.md

```

## Backend – Local Setup (Windows CMD)

This setup is only needed if you **don’t** want to use Docker right now.  
It's useful for quick inspections, unit-test runs, or debugging in Visual Studio Code (VS Code).

### Steps:

1. **(Optional) Clean an old checkout**:
   If you've already cloned the repo previously, clean it before proceeding.

```cmd
 cd %USERPROFILE%
 rmdir /S /Q Videoflix-backend  2>NUL
```

2. **Clone the repository**:
   Clone the project to your local machine.

```cmd
git clone https://github.com/Seldir193/Videoflix_backend.git  Videoflix-backend
cd Videoflix-backend
```

3. **Create and activate a virtual environment**:

```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

4. **install dependencies**

```cmd
pip install --no-cache-dir -r requirements.txt
```

5. **Copy the .env.template file and rename it to .env**:

```cmd
copy .env.template .env   # On Windows
```

6. **dev server (expects PostgreSQL at localhost:5432 or via Docker)**

```cmd
python manage.py migrate
python manage.py runserver 8000
```

## Docker-Stacks

```bash

docker compose up --build

```

## Production Stack

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose logs -f web

```

## Port Hints

- **Development stack** – `web` with `.env`  
  API available at **http://localhost:8000**

## Deployment Tips

_Example: obtain a free Let’s Encrypt TLS certificate for an Nginx-based VPS
running Ubuntu/Debian._

```bash
# install Certbot
sudo apt update && sudo apt install certbot python3-certbot-nginx

# issue/renew a cert for your domain
sudo certbot --nginx -d videoflix.example.com
```

## License

MIT License • © 2025 Selcuk Kocyigit
