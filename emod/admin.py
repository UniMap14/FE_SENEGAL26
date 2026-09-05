from django.contrib import admin

from .models import Guide, GuideCategory


class GuideInline(admin.TabularInline):
    model = Guide
    extra = 1
    prepopulated_fields = {"slug": ("title",)}


@admin.register(GuideCategory)
class GuideCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [GuideInline]


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "order")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("title",)}
