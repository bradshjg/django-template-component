from django.apps import AppConfig

from django_template_component.loader import autodiscover_components


class DjangoTemplateComponentConfig(AppConfig):
    name = "django_template_component"

    def ready(self):
        super().ready()
        autodiscover_components()
