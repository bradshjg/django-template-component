from pathlib import Path

ROOT_URLCONF = "app"

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = "not-so-secret"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]

USE_TZ = True

INSTALLED_APPS = ("component_test_app", "django_template_component")
