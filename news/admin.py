from django.contrib import admin

from .models import NewsArticle


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_date", "is_published", "is_featured")
    list_editable = ("is_published", "is_featured")
    list_filter = ("is_published", "category")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_date"