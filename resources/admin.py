from django.contrib import admin

from .models import Resource, ResourceCategory


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ResourceInline]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "resource_type", "level", "order")
    list_filter = ("category", "resource_type", "level")