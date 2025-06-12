# Backend Documentation – Videoflix

This document provides a detailed overview of the backend components of the Videoflix project, including setup instructions, configuration details, and troubleshooting tips.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Backend Setup](#backend-setup)
   1. [Local Setup](#local-setup)
   2. [Docker Setup](#docker-setup)
   3. [Additional Notes](#additional-notes)
3. [Backend Components](#backend-components)
   1. [Users](#users)
   2. [Videos](#videos)
   3. [Tasks](#tasks)
   4. [Media & Static Files](#media--static-files)
4. [Environment Variables](#environment-variables)
5. [Database Setup](#database-setup)
6. [Running Migrations](#running-migrations)
7. [Testing](#testing)
   - [Test Overview](#test-overview)
   - [Test Files](#test-files)
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

1. **Clone the repository**:
   Clone the project to your local machine.

```bash
   git clone https://github.com/Seldir193/Videoflix_backend.git
   cd Videoflix-backend
```

2. **Create and activate a virtual environment**:
   Create and activate a virtual environment to isolate dependencies.

```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # On Windows
```

3. **Install the required dependencies**:
   Install all required dependencies listed in requirements.txt.

```bash
   pip install --no-cache-dir -r requirements.txt
```

4. **Copy the .env.template file and rename it to .env**:
   The .env file contains environment variables for database configuration, SMTP settings, and more.
   Make sure to adjust the values in the .env file to match your local setup (e.g., database, SMTP).

```bash
   copy .env.template .env   # On Windows
```

Note: After renaming, open the .env file and make sure to set the correct values for your environment, such as the database connection and SMTP settings.

5. **Run migrations to set up the database schema**:
   Apply database migrations.

```bash
   python manage.py migrate
```

6. **Start the development server**:
   Start the Django development server to run the API locally.

```bash
   python manage.py runserver 8000
```

Your backend API will now be available at **http://localhost:8000**.

---

### Docker Setup

To set up the backend with Docker, follow these steps:

1. **Copy the .env.template file and rename it to .env**:
   Before starting Docker, make sure to copy and rename the .env.template file to .env. This file contains important environment variables for configuring the database, SMTP, and superuser credentials. Make sure all the values are set correctly before proceeding.

```bash
   copy .env.template .env   # On Windows
```

2. **Build and start the Docker containers**:  
   To build the containers and start the services defined in your `docker-compose.yml` file (including any changes to Dockerfiles or dependencies), run:

```bash
   docker compose up --build
```

If the containers have already been built and you just want to start them, use:

```bash
   docker compose up
```

3. **After starting the containers, run the database migrations**:
   Apply database migrations to set up the database schema.

```bash
   docker compose exec web python manage.py migrate
```

4. **Create a superuser to access the Django admin panel**:
   You'll be prompted to provide a username, email, and password for the superuser.

```bash
   docker compose exec web python manage.py createsuperuser
```

5. **View logs to ensure everything is running correctly**:
   Use the following command to view logs for the web container and ensure everything is working as expected.

```bash
   docker compose logs -f web
```

### Additional Notes:

1. **.env File**:
   Be sure to correctly configure the .env file after copying it from .env.template. This file contains essential environment variables like database credentials, SMTP settings, and superuser credentials.

2. **Docker**:
   Docker will automatically build and start all necessary containers. Ensure that all the environment variables are set correctly in the .env file before running the docker compose up --build command.

3. **Database and Redis**:
   If you're running the application locally without Docker, make sure that PostgreSQL and Redis are running on the expected ports, or use Docker to start them up.

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
python manage.py test
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

- [**test_users_models.py**](#test-users) – Tests for user models, registration, and login.
- [**test_users_serializers.py**](#test-users-serializers) – Tests for user registration and login serializers.
- [**test_users_utils.py**](#test-users-utils) – Tests for utility functions like email validation or token handling.
- [**test_users_activate_views.py**](#test-users-activate-views) – Tests for views handling user activation and account validation.
- [**test_users_admin.py**](#test-users-admin) – Tests for the Django admin interface related to users.
- [**test_videos_admin.py**](#test-videos-admin) – Tests for the Django admin interface related to videos.
- [**test_videos_views.py**](#test-videos-views) – Tests for API views related to videos, progress, etc.
- [**test_videos_signals.py**](#test-videos-signals) – Tests for signals related to video processing.
- [**test_videos_tasks.py**](#test-videos-tasks) – Tests for background tasks like video transcoding.
- [**test_videos_serializers.py**](#test-videos-serializers) – Tests for serializers used in video and user APIs.
- [**test_videos_models.py**](#test-videos-models) – Tests for Django models (e.g., WatchProgress, Video).
- [**conftest.py**](#conftest) – Configuration for fixtures and shared test setups.
- [**pytest.ini**](#pytest-ini) – Pytest configuration file for test settings.
- [**settings_test.py**](#settings-test) – Test-specific settings used during testing.

You can click on the links to scroll directly to each section.

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
