from django.contrib import admin

from .models import FAQItem


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("question", "topic", "order", "is_published")
    list_editable = ("topic", "order", "is_published")
    list_filter = ("topic", "is_published")
    search_fields = ("question", "answer")