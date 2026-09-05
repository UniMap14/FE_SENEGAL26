from django.db import models
from django.urls import reverse


class ResourceCategory(models.Model):
    """Ex: Documents EMOD, Ressources de codage, Sources de données, Communication scientifique."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Catégorie de ressource"
        verbose_name_plural = "Catégories de ressources"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("resources:category_detail", kwargs={"slug": self.slug})


class Resource(models.Model):
    """Un lien ou fichier de ressource au sein d'une catégorie."""

    TYPE_DOCUMENT = "document"
    TYPE_GUIDE = "guide"
    TYPE_MODULE = "module"
    TYPE_LIEN = "lien"
    TYPE_CHOICES = [
        (TYPE_DOCUMENT, "Document"),
        (TYPE_GUIDE, "Guide"),
        (TYPE_MODULE, "Module"),
        (TYPE_LIEN, "Lien externe"),
    ]

    LEVEL_DEBUTANT = "debutant"
    LEVEL_INTERMEDIAIRE = "intermediaire"
    LEVEL_AVANCE = "avance"
    LEVEL_CHOICES = [
        (LEVEL_DEBUTANT, "Débutant"),
        (LEVEL_INTERMEDIAIRE, "Intermédiaire"),
        (LEVEL_AVANCE, "Avancé"),
    ]

    category = models.ForeignKey(ResourceCategory, related_name="resources", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_DOCUMENT)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default=LEVEL_DEBUTANT)
    external_url = models.URLField(blank=True)
    file = models.FileField(upload_to="resources/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title