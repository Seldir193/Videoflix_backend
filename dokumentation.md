# Backend Documentation – Videoflix

This document provides a detailed overview of the backend components of the Videoflix project, including setup instructions, configuration details, and troubleshooting tips.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Backend Setup](#backend-setup)
   - [Docker Setup](#docker-setup)
   - [Admin user / super-user](#admin-user--super-user)
   - [Additional Notes](#additional-notes)
4. [Backend Components](#backend-components)
   - [Users](#users)
   - [Videos](#videos)
   - [Tasks](#tasks)
   - [Media & Static Files](#media--static-files)
5. [Environment Variables](#environment-variables)
6. [Creating a SECRET KEY](#creating-a-secret-key)
7. [Testing](#testing)
   - [Test Overview](#test-overview)
   - [Test Files](#test-files)
8. [License](#license)

---

## Project Overview

Videoflix is a full-stack Netflix clone that allows users to watch and stream videos, manage their user accounts, and store video progress. The backend is built with **Django 4** and uses **PostgreSQL 16** as the database. It includes various features such as email activation, password reset, video transcoding, and the handling of user data.

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

### Core Backend Technologies:

- **Django 4** for the web framework
- **Django REST Framework** for API handling
- **PostgreSQL 16** for the database
- **Redis 6** for caching and background tasks via **django-rq**
- **Djoser** for authentication (JWT)
- **SimpleJWT** for JSON Web Token authentication
- **WhiteNoise** for handling static and media files in production

---

## Backend Setup

### Docker Setup

1. **Clone the repository**:

```bash
    git clone https://github.com/Seldir193/Videoflix_backend.git
    cd Videoflix_backend 
```

2. **Create a `.env` file**

```bash
   cp .env.template .env
```

3. **Build & start the stack**

```bash
   docker compose up --build
```

4. **View logs**

```bash
   docker compose logs -f web
```

5. > Need an admin account?  
   > See [Admin user / super-user](#admin-user--super-user).


### Admin user / super-user

The container’s **entrypoint** checks the environment for  
`DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, and  
`DJANGO_SUPERUSER_PASSWORD`.

| Environment variables present? | What happens on first `docker compose up`? | Manual step needed? |
| ------------------------------ | ------------------------------------------- | ------------------- |
| **Yes** (all three)           | Super-user is created automatically.        | **No.** You can log in right away. |
| **No** (one or more missing)  | No super-user is created.                   | **Yes.** Once the stack is running, execute:<br>`docker compose exec web python manage.py createsuperuser` |

If the user already exists in the database, the entrypoint simply skips the
creation step—so you can safely keep the code in place without side-effects.

## Production Stack (essentials)

1. **Expose the app**  
   WhiteNoise already serves static files.  
   Map the container port to the host as needed, e.g.

```bash
   docker compose up --build -d            
   # or
   docker run -p 80:8000 videoflix:latest
```

2. **Critical env overrides**  
```env
   DEBUG=False
   ALLOWED_HOSTS=your-domain
   CSRF_TRUSTED_ORIGINS=https://your-domain
```

3. **Initial admin user**

If no admin exists yet, create one as shown in the Docker Setup section.

### Additional Notes

- **.env** – edit the copied `.env` before the first `docker compose up`; it
  holds DB, SMTP and optional `DJANGO_SUPERUSER_*` values.

- **Local Python workflow** – if you run the backend outside Docker,
  make sure PostgreSQL and Redis are running on their default ports
  (or start them via Docker).


## Backend Components

### Users

The `users` app is responsible for handling all user-related functionality, such as registration, login, and account management.

- **Models**: Custom user model and related fields
- **Serializers**: User registration and authentication serializers
- **Views**: Account creation, login, and profile management

Key features include:

- Email activation (via Djoser)
- Password reset
- JWT authentication (via SimpleJWT)

### Videos

The `videos` app is responsible for managing the video content, including video metadata, uploads, and transcoding.

- **Models**: Video model (title, description, category, etc.)
- **Serializers**: Video-related data serialization
- **Views**: CRUD operations for managing videos
- **Tasks**: Background tasks for transcoding videos using FFmpeg

### Tasks

Video transcoding is handled by background tasks defined in `videos/tasks.py`. These tasks are executed using **django-rq** and **Redis** for queuing.

---

## Media & Static Files

In the backend, media and static files are handled by Django with the help of **WhiteNoise** for serving static files in production and **Django**'s default configuration for media files (e.g., uploaded videos, thumbnails).

### Static Files

Static files include assets such as CSS, JavaScript, and image files that are required for the frontend of the application. During development, Django serves these files directly. In production, **WhiteNoise** is used to serve static files more efficiently.

To collect static files and prepare them for production, use the following command:

```bash
python manage.py collectstatic
```

## Environment Variables

All configuration lives in the `.env` file (copy `.env.template` first).  
Below are the most important keys; the template already contains sensible
defaults or placeholders.

| Category | Key | Notes |
|----------|-----|-------|
| **Core** | `SECRET_KEY` | Always set your own random key (see below). |
| **PostgreSQL** | `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Credentials for the Django DB. |
| | `DB_HOST` | `db` when using Docker (service name), `localhost` for bare-metal. |
| | `DB_PORT` | Usually `5432` |
| **Redis / django-rq** | `REDIS_HOST` (`redis` in Docker, `localhost` otherwise), `REDIS_PORT`, `REDIS_DB` | Queue & cache backend |
| **Frontend URLs** | `FRONTEND_PROTOCOL`, `FRONTEND_DOMAIN` | Used in e-mail activation links |
| **Super-user (optional)** | `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` | If all three are set, the entry-point creates the admin automatically. |

### E-mail settings

```env
   # default (dev): log mails to console
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

   # switch to SMTP for real mails
   #EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   EMAIL_USE_TLS=True
   EMAIL_USE_SSL=False
   DEFAULT_FROM_EMAIL="Videoflix <noreply@example.com>"
```
You can find a sample `.env` file in `.env.template`.

---

**Important**: You must generate a unique `SECRET_KEY` for your project.

## Creating a SECRET KEY

To generate a secure `SECRET_KEY` for your project:

1. **Open a Python shel**:

```bash
   python
```

2. **Run the following Python code to generate the SECRET_KEY**:

```bash
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
```

3. **Copy the generated key and add it to your .env file as follows**:

```bash
   SECRET_KEY=your_generated_secret_key
```

## Testing

```bash
pytest --cov=. --cov-report=term-missing -v
```

## Test Overview

Here are the test files that you can explore and execute:

- **Test User Models**: Tests for user creation, password mismatch validation, and authentication mechanisms.
- **Test Video Models**: Tests for video file uploads, variants creation, and video-related functionality.
- **Test API Views**: Tests for various API views including video listing, progress tracking, and trailer management.
- **Test Signals**: Tests for background tasks related to video processing and file cleanup.

### Test Files

- [**test_users_models.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/tests/test_users_models.py) – Tests for user models, registration, and login.
- [**test_users_serializers.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/tests/test_users_serializers.py) – Tests for user registration and login serializers.
- [**test_users_utils.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/tests/test_users_utils.py) – Tests for utility functions like email validation or token handling.
- [**test_users_activate_views.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/tests/test_users_activate_view.py) – Tests for views handling user activation and account validation.
- [**test_users_admin.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/tests/test_users_admin.py) – Tests for the Django admin interface related to users.
- [**test_videos_admin.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/tests/test_videos_admin.py) – Tests for the Django admin interface related to videos.
- [**test_videos_views.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/tests/test_videos_views.py) – Tests for API views related to videos, progress, etc.
- [**test_videos_signals.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/tests/test_videos_signals.py) – Tests for signals related to video processing.
- [**test_videos_tasks.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/tests/test_videos_tasks.py) – Tests for background tasks like video transcoding.
- [**test_videos_serializers.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/tests/test_videos_serializers.py) – Tests for serializers used in video and user APIs.
- [**test_videos_models.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/tests/test_videos_models.py) – Tests for Django models (e.g., WatchProgress, Video).
- [**conftest.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/conftest.py) – Configuration for fixtures and shared test setups.
- [**pytest.ini**](https://github.com/Seldir193/Videoflix_backend/blob/main/pytest.ini) – Pytest configuration file for test settings.
- [**settings_test.py**](https://github.com/Seldir193/Videoflix_backend/blob/main/video_backend/settings_test.py) – Test-specific settings used during testing.

You can click on the links to scroll directly to each section.

## License

MIT License • © 2025 Selcuk Kocyigit
