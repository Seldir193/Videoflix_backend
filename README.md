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

1. [Quick Start](#quick-start)
2. [Backend Setup](#backend-setup)
   - [Docker Setup](#docker-setup)
   - [E-mail settings](#e-mail-settings)
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

### E-mail settings

* **SMTP is the default.**  
  In `.env.template` the line  
  `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` is already active.

* **Fill in your provider credentials** (`EMAIL_HOST`, `EMAIL_HOST_USER`, …).

* **Local dev shortcut:**  
  Uncomment the console-backend line to log mails locally instead of sending them.

* **More details:** see [docs → Environment variables](dokumentation.md#environment-variables).

### Admin user / super-user

How the first admin account is created is described in  
[the docs → Admin user / super-user](dokumentation.md#admin-user--super-user).

---

## Production

For TLS, reverse-proxy tips or a manual **`createsuperuser`**, check the  
[Production guide](dokumentation.md#production-stack).


## Project Structure

A full folder-and-file breakdown is now available here:  
[docs/project-structure.md](dokumentation.md#project-structure)

```

## Port Hints

- **Development / Production** – container **web**  
  - API   → <http://localhost:8000>  
  - Admin → <http://localhost:8000/admin>

## License

MIT License • © 2025 Selcuk Kocyigit
