from django.db import models


class ContactMessage(models.Model):
    first_name = models.CharField("Votre nom", max_length=100)
    last_name = models.CharField("Nom de famille", max_length=100)
    phone = models.CharField("Numéro de téléphone", max_length=30)
    email = models.EmailField("E-mail")
    message = models.TextField("Message", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.created_at:%d/%m/%Y})"
