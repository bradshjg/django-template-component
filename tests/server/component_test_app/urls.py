from django.urls import path

from . import views

urlpatterns = [
    path("", views.OKView.as_view(), name="ok"),
]
