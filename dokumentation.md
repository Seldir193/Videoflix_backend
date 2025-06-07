# Backend Documentation – Videoflix

This document provides a detailed overview of the backend components of the Videoflix project, including setup instructions, configuration details, and troubleshooting tips.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Backend Setup](#backend-setup)
    1. [Local Setup](#local-setup)
    2. [Docker Setup](#docker-setup)
3. [Backend Components](#backend-components)
    1. [Users](#users)
    2. [Videos](#videos)
    3. [Tasks](#tasks)
    4. [Media & Static Files](#media--static-files)
4. [Environment Variables](#environment-variables)
5. [Database Setup](#database-setup)
6. [Running Migrations](#running-migrations)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)
9. [License](#license)

---

## Project Overview

Videoflix is a full-stack Netflix clone that allows users to watch and stream videos, manage their user accounts, and store video progress. The backend is built with **Django 4** and uses **PostgreSQL 16** as the database. It includes various features such as email activation, password reset, video transcoding, and the handling of user data.

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

### Local Setup

If you want to set up the backend locally without using Docker, follow the steps below:

1. Clone the repository:

    ```bash
    git clone https://github.com/Seldir193/Videoflix_backend.git
    cd Videoflix-backend
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate   # On Windows
    ```

3. Install the required dependencies:

    ```bash
    pip install --no-cache-dir -r requirements.txt
    ```

4. Run migrations to set up the database schema:

    ```bash
    python manage.py migrate
    ```

5. Start the development server:

    ```bash
    python manage.py runserver 8000
    ```

Your backend API will now be available at **http://localhost:8000**.

---

### Docker Setup

To set up the backend with Docker, follow these steps:

1. Build and start the Docker containers:

    ```bash
    docker compose up --build
    ```

2. After starting the containers, run the database migrations:

    ```bash
    docker compose exec web python manage.py migrate
    ```

3. Create a superuser to access the Django admin panel:

    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

4. View logs to ensure everything is running correctly:

    ```bash
    docker compose logs -f web
    ```

---

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

## Environment Variables

The backend relies on several environment variables for configuration. These variables can be found in the `.env` file. Some of the key environment variables include:

- `SECRET_KEY`: Django's secret key for cryptographic signing
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL database user
- `DB_PASSWORD`: PostgreSQL database password
- `REDIS_URL`: URL for Redis instance

You can find a sample `.env` file in `.env.template`.

---

## Database Setup

The backend uses **PostgreSQL 16**. Ensure that PostgreSQL is running either locally or in a Docker container.

1. If using Docker, PostgreSQL should be automatically set up via Docker Compose.
2. If running PostgreSQL locally, make sure it is configured to listen on `localhost:5432`.

Run migrations to apply the database schema:

```bash
python manage.py migrate

```

## Running Migrations

Before starting the application, you need to apply the database migrations to set up the necessary tables. Run the following command to apply all migrations:

```bash
python manage.py migrate
```

## Testing

```bash
python manage.py test
```

## Troubleshooting

```bash
python manage.py collectstatic
```

Django Admin Access Issues:
```bash
python manage.py createsuperuser
```
Redis Queue Not Running:

```bash
docker compose logs redis
```

## License
MIT License • © 2025 Selcuk Kocyigit

