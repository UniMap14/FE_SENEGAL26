from django.db import models


class ProgrammeYear(models.Model):
    """Une édition annuelle du programme (ex: 'Programme 2025')."""

    year_label = models.CharField(max_length=50, help_text="Ex: Programme 2025")
    is_current = models.BooleanField(default=True)

    intro_title = models.CharField(max_length=255, default="Manuel du programme")
    intro_subtitle = models.CharField(
        max_length=255, default="Un guide complet du programme, des devoirs et des objectifs d'apprentissage de cette année"
    )
    handbook_file = models.FileField(upload_to="programme/handbooks/", blank=True, null=True)

    objectives_and_expectations = models.TextField(blank=True)
    journal_club_expectations = models.TextField(blank=True)
    presentation_expectations = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.year_label


class ProgrammeSection(models.Model):
    """Liens de la barre latérale : Liste de vérification, Manuel, Meilleures pratiques..."""

    programme_year = models.ForeignKey(ProgrammeYear, related_name="sections", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Milestone(models.Model):
    """Ligne du tableau 'Étapes clés du programme'."""

    programme_year = models.ForeignKey(ProgrammeYear, related_name="milestones", on_delete=models.CASCADE)
    week = models.CharField(max_length=10, help_text="Ex: 0, 2, 3... (numéro de semaine)")
    task = models.CharField(max_length=255, help_text="Ex: Plan des objectifs spécifiques n° 1")
    due_date = models.DateField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "due_date"]

    def __str__(self):
        return f"Semaine {self.week} — {self.task}"
