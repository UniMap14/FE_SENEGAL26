from django.db import models
from django.urls import reverse
from django.utils import timezone


class NewsArticle(models.Model):
    """Un article d'actualité publié sur le site."""

    CATEGORY_ANNONCE = "annonce"
    CATEGORY_EVENEMENT = "evenement"
    CATEGORY_PARTENARIAT = "partenariat"
    CATEGORY_RECHERCHE = "recherche"
    CATEGORY_CHOICES = [
        (CATEGORY_ANNONCE, "Annonce"),
        (CATEGORY_EVENEMENT, "Compte-rendu d'événement"),
        (CATEGORY_PARTENARIAT, "Partenariat"),
        (CATEGORY_RECHERCHE, "Recherche"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_ANNONCE)
    excerpt = models.TextField(
        max_length=400, blank=True,
        help_text="Court résumé affiché dans la liste des actualités. Généré à partir du contenu si laissé vide.",
    )
    content = models.TextField()
    cover_image = models.ImageField(upload_to="news/", blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Mettre en avant en haut de la liste des actualités.")

    class Meta:
        ordering = ["-published_date"]
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:detail", kwargs={"slug": self.slug})

    @property
    def display_excerpt(self):
        if self.excerpt:
            return self.excerpt
        text = self.content.strip()
        return text[:220] + "…" if len(text) > 220 else text

    @property
    def reading_time_minutes(self):
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))