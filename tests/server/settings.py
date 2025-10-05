ROOT_URLCONF = "app"

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
