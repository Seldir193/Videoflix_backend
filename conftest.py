import pytest
from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }


@pytest.fixture(scope="session", autouse=True)
def _prepare_test_db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("migrate", verbosity=0, run_syncdb=True)
