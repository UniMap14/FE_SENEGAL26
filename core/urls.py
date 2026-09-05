from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("a-propos/", views.about_view, name="about"),
    path("galerie/", views.gallery_view, name="gallery"),
    path("equipe/", views.team_list_view, name="team_list"),
    path("equipe/<slug:slug>/", views.team_detail_view, name="team_detail"),
]
