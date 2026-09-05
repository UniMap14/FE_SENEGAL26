from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "phone", "email", "message"]
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom de famille",
            "phone": "Numéro de téléphone",
            "email": "E-mail",
            "message": "Message",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Votre prénom", "class": "form-control", "required": "required",
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Votre nom de famille", "class": "form-control", "required": "required",
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "Ex : +221 77 000 00 00", "class": "form-control", "required": "required",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "vous@exemple.com", "class": "form-control", "required": "required",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Écrivez votre message ici...", "class": "form-control", "rows": 6,
            }),
        }
        error_messages = {
            "first_name": {"required": "Merci de renseigner votre prénom."},
            "last_name": {"required": "Merci de renseigner votre nom de famille."},
            "phone": {"required": "Merci de renseigner votre numéro de téléphone."},
            "email": {
                "required": "Merci de renseigner votre e-mail.",
                "invalid": "Merci de saisir une adresse e-mail valide.",
            },
        }