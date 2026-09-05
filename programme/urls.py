from django.urls import path

from . import views

app_name = "programme"

urlpatterns = [
    path("", views.handbook_view, name="handbook"),
]
