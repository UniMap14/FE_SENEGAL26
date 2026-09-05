from django.db import models
from django.urls import reverse


class GuideCategory(models.Model):
    """Catégorie de la barre latérale 'Guides pratiques EMOD'
    (Guide d'installation, Guides de simulation, Guides démographiques, ...)."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)
    intro_text = models.TextField(
        blank=True,
        help_text="Ex: Cliquez sur les liens du menu latéral gauche pour naviguer entre les différents guides EMOD.",
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Catégorie de guide EMOD"
        verbose_name_plural = "Catégories de guides EMOD"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("emod:guide_category", kwargs={"slug": self.slug})


class Guide(models.Model):
    """Un guide individuel au sein d'une catégorie."""

    category = models.ForeignKey(GuideCategory, related_name="guides", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    content = models.TextField(blank=True)
    file = models.FileField(upload_to="emod/guides/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = ("category", "slug")

    def __str__(self):
        return f"{self.category.title} — {self.title}"

    def get_absolute_url(self):
        return reverse("emod:guide_detail", kwargs={"category_slug": self.category.slug, "slug": self.slug})

    @property
    def reading_time_minutes(self):
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))
