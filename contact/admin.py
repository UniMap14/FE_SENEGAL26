from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)
    readonly_fields = ("first_name", "last_name", "email", "phone", "message", "created_at")
    search_fields = ("first_name", "last_name", "email")
