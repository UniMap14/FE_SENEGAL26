from django.db import models
from django.urls import reverse
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    registration_url = models.URLField(blank=True)

    class Meta:
        ordering = ["start_datetime"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("events:event_detail", kwargs={"slug": self.slug})

    @property
    def is_past(self):
        return self.start_datetime < timezone.now()


class EventPhoto(models.Model):
    """Une photo de la galerie d'un événement (typiquement un événement passé)."""

    event = models.ForeignKey(Event, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="events/gallery/")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Photo d'événement"
        verbose_name_plural = "Photos d'événement"

    def __str__(self):
        return self.caption or f"Photo de {self.event.title}"