from django.db import models


class FAQItem(models.Model):
    """Une question fréquente et sa réponse, optionnellement groupée par thème."""

    topic = models.CharField(
        max_length=150, blank=True,
        help_text="Ex : Programme, EMOD, Inscription. Laisser vide pour 'Général'.",
    )
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["topic", "order"]
        verbose_name = "Question fréquente"
        verbose_name_plural = "Questions fréquentes"

    def __str__(self):
        return self.question