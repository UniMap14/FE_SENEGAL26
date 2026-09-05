from django.contrib import admin

from .models import Event, EventPhoto


class EventPhotoInline(admin.TabularInline):
    model = EventPhoto
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_datetime", "location")
    list_filter = ("start_datetime",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [EventPhotoInline]