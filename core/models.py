from django.db import models


class SiteSettings(models.Model):
    """Réglages globaux du site (singleton) : logo, coordonnées, mission."""

    site_name = models.CharField(max_length=200, default="FE_SENEGAL")
    tagline = models.CharField(max_length=200, default="Excellence & Partage", blank=True)
    logo = models.ImageField(
        upload_to="site/", blank=True, null=True,
        help_text="Si vide, le logo par défaut du site (static/img/site-logo.jpg) est utilisé.",
    )

    contact_email = models.EmailField(blank=True, default="fe2024.uidt@univ-thies.sn")
    contact_phone = models.CharField(max_length=100, blank=True, default="+221 77 441 02 11")
    contact_address = models.CharField(
        max_length=255, blank=True, default="Université Iba Der Thiam, Thiès, Sénégal"
    )

    footer_about_text = models.TextField(
        blank=True,
        default=(
            "FE_SENEGAL est engagée dans l'excellence académique et la formation de "
            "professionnels compétents et responsables en modélisation appliquée du paludisme."
        ),
        help_text="Texte affiché dans le pied de page sous 'À propos de nous'.",
    )

    class Meta:
        verbose_name = "Réglages du site"
        verbose_name_plural = "Réglages du site"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter / X"),
        ("youtube", "YouTube"),
        ("wordpress", "WordPress"),
        ("instagram", "Instagram"),
        ("other", "Autre"),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.get_platform_display()}"


class Mission(models.Model):
    """Élément numéroté de la section 'Nos Missions'."""

    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text


class AboutPage(models.Model):
    """Contenu de la page 'À propos de nous' (singleton)."""

    intro = models.TextField(
        blank=True,
        default=(
            "Le fardeau du paludisme demeure élevé en Afrique subsaharienne malgré deux "
            "décennies d'interventions intensives. L'analyse et l'utilisation régulières des "
            "données de santé publique permettront une lutte plus efficace contre cette maladie "
            "grâce à une prise de décision fondée sur des données probantes."
        ),
        help_text="Ex: Le fardeau du paludisme demeure élevé en Afrique subsaharienne...",
    )
    long_term_goal = models.TextField(
        blank=True,
        default="Notre objectif à long terme est de former une masse critique de scientifiques spécialisés en modélisation qui soient :",
        help_text="Ex: Notre objectif à long terme est de former une masse critique...",
    )
    programme_summary = models.TextField(
        blank=True,
        default=(
            "Pour contribuer à la réalisation de cet objectif, l'équipe de FE_SENEGAL propose un "
            "programme de formation intensive en présentiel de 18 semaines sur la modélisation "
            "appliquée du paludisme."
        ),
        help_text="Ex: programme de formation intensive en présentiel de 18 semaines...",
    )
    photo = models.ImageField(upload_to="about/", blank=True, null=True)

    class Meta:
        verbose_name = "Page À propos"
        verbose_name_plural = "Page À propos"

    def __str__(self):
        return "À propos de nous"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HomeSlide(models.Model):
    """Diapositive du carrousel de la page d'accueil."""

    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    button_text = models.CharField(max_length=100, default="EN SAVOIR PLUS")
    button_url = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="home_slides/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Partner(models.Model):
    """Logo de partenaire affiché sur le site (bandeau partenaires)."""

    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="partners/")
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"

    def __str__(self):
        return self.name


class GalleryPhoto(models.Model):
    """Photo affichée dans la galerie du site (ateliers, événements, vie du programme)."""

    CATEGORY_CHOICES = [
        ("atelier", "Ateliers & formations"),
        ("evenement", "Événements"),
        ("equipe", "Vie de l'équipe"),
        ("campus", "Campus & partenaires"),
    ]

    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="atelier")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Photo de la galerie"
        verbose_name_plural = "Galerie photo"

    def __str__(self):
        return self.caption or f"Photo #{self.pk}"


class TeamMember(models.Model):
    """Un membre de l'équipe / du programme, avec sa propre page de profil."""

    CATEGORY_COORDINATION = "coordination"
    CATEGORY_ENSEIGNANT = "enseignant"
    CATEGORY_ETUDIANT = "etudiant"
    CATEGORY_PARTENAIRE = "partenaire"
    CATEGORY_CHOICES = [
        (CATEGORY_COORDINATION, "Coordination"),
        (CATEGORY_ENSEIGNANT, "Enseignants-chercheurs"),
        (CATEGORY_ETUDIANT, "Étudiants & modélisateurs"),
        (CATEGORY_PARTENAIRE, "Partenaires associés"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    role = models.CharField(max_length=255, help_text="Ex: Enseignant-chercheur, Coordinateur du programme...")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_ENSEIGNANT)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    bio = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    email = models.EmailField(blank=True)
    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter / X")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn")
    scholar_url = models.URLField(blank=True, verbose_name="Google Scholar")
    researchgate_url = models.URLField(blank=True, verbose_name="ResearchGate")
    orcid_url = models.URLField(blank=True, verbose_name="ORCID")

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("core:team_detail", kwargs={"slug": self.slug})

    @property
    def initials(self):
        parts = self.name.split()
        return "".join(p[0].upper() for p in parts[:2]) if parts else "?"

    @property
    def social_links(self):
        links = []
        if self.facebook_url:
            links.append(("Facebook", self.facebook_url, "facebook"))
        if self.twitter_url:
            links.append(("Twitter / X", self.twitter_url, "twitter"))
        if self.linkedin_url:
            links.append(("LinkedIn", self.linkedin_url, "linkedin"))
        if self.scholar_url:
            links.append(("Google Scholar", self.scholar_url, "scholar"))
        if self.researchgate_url:
            links.append(("ResearchGate", self.researchgate_url, "researchgate"))
        if self.orcid_url:
            links.append(("ORCID", self.orcid_url, "orcid"))
        return links

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.name)
            slug = base_slug
            i = 1
            while TeamMember.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base_slug}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)
