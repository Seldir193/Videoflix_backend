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

1. [Quick Start](#quick-start-docker--recommended)
2. [Backend Setup](#backend-setup)
   - [Docker Setup](#docker-setup)
   - [Admin user / super-user](dokumentation.md#admin-user--super-user)
3. [Production](#production)
4. [Project Structure](#project-structure)
5. [Port Hints](#port-hints)
6. [License](#license)

---

## Quick Start
*Docker — recommended*

```bash
git clone https://github.com/Seldir193/Videoflix_backend.git
cd Videoflix_backend
cp .env.template .env
docker compose up --build -d
```

## Backend Setup

### Docker Setup

Full procedure & troubleshooting: see the  
[Docker Setup guide](dokumentation.md#docker-setup).

### Admin user / super-user

How the first admin account is created is described in  
[the docs → Admin user / super-user](dokumentation.md#admin-user--super-user).

---

## Production

For TLS, reverse-proxy tips or a manual **`createsuperuser`**, check the  
[Production guide](dokumentation.md#production-stack).


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

## Port Hints

- **Development / Production** – container **web**  
  - API   → <http://localhost:8000>  
  - Admin → <http://localhost:8000/admin>

## License

MIT License • © 2025 Selcuk Kocyigit
