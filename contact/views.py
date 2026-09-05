from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from core.models import SiteSettings

from .forms import ContactForm


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            _send_contact_notifications(contact_message)
            messages.success(request, "Votre message a bien été envoyé. Nous vous répondrons rapidement.")
            return redirect("contact:contact")
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})


def _send_contact_notifications(contact_message):
    """Envoie une notification à l'équipe FE_SENEGAL + un accusé de réception au visiteur."""
    site_settings = SiteSettings.load()
    admin_recipient = site_settings.contact_email

    full_name = f"{contact_message.first_name} {contact_message.last_name}".strip()

    if admin_recipient:
        send_mail(
            subject=f"[{site_settings.site_name}] Nouveau message de {full_name}",
            message=(
                f"Nouveau message reçu via le formulaire de contact du site.\n\n"
                f"Nom : {full_name}\n"
                f"Téléphone : {contact_message.phone}\n"
                f"E-mail : {contact_message.email}\n\n"
                f"Message :\n{contact_message.message or '(aucun message)'}"
            ),
            from_email=None,
            recipient_list=[admin_recipient],
            fail_silently=True,
        )

    if contact_message.email:
        send_mail(
            subject=f"{site_settings.site_name} — Nous avons bien reçu votre message",
            message=(
                f"Bonjour {contact_message.first_name},\n\n"
                f"Merci de nous avoir contactés. Votre message a bien été reçu, "
                f"notre équipe vous répondra dans les meilleurs délais.\n\n"
                f"Récapitulatif de votre message :\n{contact_message.message or '(aucun message)'}\n\n"
                f"— L'équipe {site_settings.site_name}"
            ),
            from_email=None,
            recipient_list=[contact_message.email],
            fail_silently=True,
        )