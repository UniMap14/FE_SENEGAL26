from django.urls import path

from . import views

app_name = "resources"

urlpatterns = [
    path("", views.resources_index_view, name="index"),
    path("<slug:slug>/", views.category_detail_view, name="category_detail"),
]
