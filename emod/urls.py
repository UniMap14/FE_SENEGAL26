from django.urls import path

from . import views

app_name = "emod"

urlpatterns = [
    path("", views.emod_index_view, name="index"),
    path("<slug:slug>/", views.guide_category_view, name="guide_category"),
    path("<slug:category_slug>/<slug:slug>/", views.guide_detail_view, name="guide_detail"),
]
