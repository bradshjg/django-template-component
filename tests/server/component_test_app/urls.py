from django.urls import path

from . import views

urlpatterns = [
    path("template/", views.template_user_details, name="tempate"),
    path("component/", views.component_user_details, name="component"),
]
