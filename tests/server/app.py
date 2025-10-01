#!/usr/bin/env python
import os

from django.core.management import execute_from_command_line
from django.urls import include, path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

urlpatterns = [
    path("", include("component_test_app.urls")),
]

if __name__ == "__main__":
    execute_from_command_line()
