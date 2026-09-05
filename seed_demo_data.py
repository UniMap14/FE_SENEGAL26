"""Peuple la base avec des données de démonstration complètes pour FE_SENEGAL.
Usage : python3 manage.py shell < seed_demo_data.py
"""
import datetime
import os

from django.conf import settings
from django.core.files import File
from django.utils import timezone
from django.utils.text import slugify
from news.models import NewsArticle
from core.models import AboutPage, GalleryPhoto, HomeSlide, Mission, Partner, SiteSettings, SocialLink, TeamMember
from emod.models import Guide, GuideCategory
from events.models import Event
from programme.models import Milestone, ProgrammeSection, ProgrammeYear
from resources.models import Resource, ResourceCategory
from faq.models import FAQItem
from events.models import Event, EventPhoto
BASE_DIR = str(settings.BASE_DIR)
STATIC_IMG = os.path.join(BASE_DIR, "static", "img")

# --- Site settings ---
s = SiteSettings.load()
s.site_name = "FE_SENEGAL"
s.tagline = "Excellence & Partage"
s.contact_email = "fe2024.uidt@univ-thies.sn"
s.contact_phone = "+221 77 441 02 11"
s.contact_address = "Université Iba Der Thiam, Thiès, Sénégal"
s.footer_about_text = (
    "FE_SENEGAL est engagée dans l'excellence académique et la formation de "
    "professionnels compétents et responsables en modélisation appliquée du paludisme."
)
if not s.logo:
    logo_path = os.path.join(STATIC_IMG, "site-logo.jpg")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            s.logo.save("site-logo.jpg", File(f), save=False)
s.save()

for platform, url in [("facebook", "https://facebook.com"), ("twitter", "https://x.com"),
                       ("youtube", "https://youtube.com"), ("wordpress", "https://wordpress.com")]:
    SocialLink.objects.get_or_create(platform=platform, url=url)

# --- Partenaires ---
partner_files = [
    ("Northwestern University Malaria Modeling", "partners/northwestern.jpg", "https://malaria.northwestern.edu/"),
    ("Ahadi", "partners/ahadi.jpg", ""),
    ("WAMCAD — West Africa Mathematical Modelling Capacity Development", "partners/wamcad.jpg", ""),
]
for i, (name, rel_path, url) in enumerate(partner_files, start=1):
    if Partner.objects.filter(name=name).exists():
        continue
    full_path = os.path.join(STATIC_IMG, rel_path)
    if os.path.exists(full_path):
        partner = Partner(name=name, url=url, order=i)
        with open(full_path, "rb") as f:
            partner.logo.save(os.path.basename(full_path), File(f), save=False)
        partner.save()

# --- Home slide ---
HomeSlide.objects.get_or_create(
    title="Former l'excellence en modélisation appliquée du paludisme",
    defaults=dict(
        body=(
            "Malgré deux décennies d'interventions intensives, le paludisme demeure très "
            "répandu en Afrique subsaharienne. L'analyse et l'utilisation régulières des "
            "données de santé publique permettront une lutte plus efficace grâce à une "
            "prise de décision fondée sur des données probantes."
        ),
        button_text="EN SAVOIR PLUS",
        button_url="/a-propos/",
        order=1,
    ),
)

# --- About page + missions ---
about = AboutPage.load()
about.intro = (
    "Le fardeau du paludisme demeure élevé en Afrique subsaharienne malgré deux décennies "
    "d'interventions intensives. L'analyse et l'utilisation régulières des données de santé "
    "publique permettront une lutte plus efficace contre cette maladie grâce à une prise de "
    "décision fondée sur des données probantes."
)
about.long_term_goal = (
    "Notre objectif à long terme est de former une masse critique de scientifiques "
    "spécialisés en modélisation qui soient :"
)
about.programme_summary = (
    "Pour contribuer à la réalisation de cet objectif, l'équipe FE_SENEGAL propose un "
    "programme de formation intensive en présentiel de 18 semaines sur la modélisation "
    "appliquée du paludisme."
)
about.save()

for i, text in enumerate([
    "Maintenue en Afrique subsaharienne",
    "Former la prochaine génération de modélisateurs",
    "Travailler en étroite collaboration avec les programmes locaux de lutte contre le paludisme pour fournir un soutien opérationnel",
    "Compétitif pour l'obtention de subventions auprès d'organismes de financement internationaux",
    "Étroitement liés entre eux à travers l'Afrique et avec des partenaires internationaux",
], start=1):
    Mission.objects.get_or_create(text=text, defaults={"order": i})

# --- Programme year + sections + milestones ---
py, _ = ProgrammeYear.objects.get_or_create(
    year_label="Programme 2025",
    defaults=dict(
        is_current=True,
        intro_title="Manuel du programme",
        intro_subtitle="Un guide complet du programme, des devoirs et des objectifs d'apprentissage de cette année",
        objectives_and_expectations=(
            "Chaque participant du programme FE_SENEGAL est tenu de consacrer un minimum de 30 heures "
            "par semaine aux activités du programme : cours magistraux, travaux pratiques sur EMOD, "
            "lecture critique d'articles scientifiques et travail personnel de modélisation. "
            "L'assiduité aux séances est obligatoire et les absences doivent être justifiées auprès "
            "du comité pédagogique au moins 48 heures à l'avance. Chaque stagiaire doit produire, "
            "à l'issue du programme, un rapport de modélisation appliqué à une problématique réelle "
            "de lutte antipaludique au Sénégal ou dans la sous-région."
        ),
        journal_club_expectations=(
            "Le journal club se tient chaque vendredi et permet aux participants de présenter et "
            "discuter collectivement un article scientifique récent portant sur la modélisation du "
            "paludisme. Chaque participant anime la séance au moins deux fois durant le programme : "
            "résumé de la problématique, méthodologie, résultats clés et limites de l'étude, suivis "
            "d'une discussion ouverte avec les encadrants et les pairs."
        ),
        presentation_expectations=(
            "À la fin de chaque module, les stagiaires présentent l'avancement de leur projet de "
            "modélisation devant l'ensemble de la promotion et de l'équipe encadrante. Les présentations "
            "doivent durer entre 10 et 15 minutes, suivies de 5 minutes de questions, et couvrir : "
            "le contexte épidémiologique, les hypothèses de modélisation retenues, les résultats "
            "préliminaires et les prochaines étapes envisagées."
        ),
    ),
)
for i, title in enumerate([
    "Liste de vérification pré-programme", "Manuel du programme", "Meilleures pratiques",
    "Exemples d'exercices", "Club de lecture", "Enregistrements de session",
], start=1):
    ProgrammeSection.objects.get_or_create(programme_year=py, title=title, defaults={"order": i})

milestones = [
    ("0", "Exercice de programmation préalable au programme", "2025-04-11"),
    ("2", "Présentation introductive à la recherche", "2025-04-17"),
    ("2", "Idées d'objectifs spécifiques", "2025-04-25"),
    ("3", "Plan des objectifs spécifiques n° 1", "2025-05-02"),
    ("4", "Plan d'objectifs spécifiques n° 2", "2025-05-09"),
    ("6", "Objectifs spécifiques - Version complète n° 1", "2025-05-23"),
    ("6", "Présentation des objectifs spécifiques", "2025-05-28"),
    ("8", "Objectifs spécifiques - Version complète n° 2", "2025-06-06"),
    ("10", "Objectifs spécifiques - Version complète n° 3", "2025-06-20"),
    ("11", "Présentation en cours de réalisation", "2025-07-02"),
    ("12", "Objectifs spécifiques Heure de révision par les pairs", "2025-07-04"),
    ("12", "Biographie préliminaire n° 1", "2025-07-04"),
    ("13", "Objectifs spécifiques - Version complète n° 4", "2025-07-11"),
    ("14", "Biographie provisoire n° 2", "2025-07-18"),
    ("15", "Objectifs spécifiques Version finale", "2025-07-25"),
    ("16", "Heure de révision par les pairs des notices biographiques", "2025-07-28"),
    ("18", "Présentation du projet final", "2025-08-14"),
]
for i, (week, task, due) in enumerate(milestones, start=1):
    Milestone.objects.get_or_create(
        programme_year=py, task=task,
        defaults=dict(week=week, due_date=datetime.date.fromisoformat(due), order=i),
    )

# --- EMOD guide categories + guides ---
emod_categories = [
    "Guide d'installation", "Guides de simulation", "Guides démographiques", "Guides climatiques",
    "Guides vectoriels", "Guides de diagnostic", "Guides d'intervention",
    "Guides de rédaction de rapports", "Guides d'analyse", "Guides des propriétés individuelles",
]
for i, title in enumerate(emod_categories, start=1):
    slug = slugify(title)
    cat, _ = GuideCategory.objects.get_or_create(
        title=title, defaults=dict(
            slug=slug, order=i,
            intro_text="Cliquez sur les liens du menu latéral gauche pour naviguer entre les différents guides EMOD.",
        ),
    )
    for j in range(1, 11):
        Guide.objects.get_or_create(
            category=cat, slug=f"{slug}-partie-{j}",
            defaults=dict(
                title=f"{title} — Partie {j}",
                content=(
                    f"Contenu de démonstration pour « {title} » (partie {j}). "
                    "Ce guide peut être complété ou remplacé depuis l'admin."
                ),
                order=j,
            ),
        )

# --- Resource categories + resources ---
resource_categories = [
    "Documents EMOD", "Ressources de codage", "Sources de données", "Communication scientifique",
]
type_cycle = [Resource.TYPE_DOCUMENT, Resource.TYPE_GUIDE, Resource.TYPE_MODULE]
level_cycle = [Resource.LEVEL_DEBUTANT, Resource.LEVEL_INTERMEDIAIRE, Resource.LEVEL_AVANCE]
for i, title in enumerate(resource_categories, start=1):
    slug = slugify(title)
    cat, _ = ResourceCategory.objects.get_or_create(title=title, defaults=dict(slug=slug, order=i))
    for j in range(1, 9):
        Resource.objects.get_or_create(
            category=cat, title=f"{title} — Ressource {j}",
            defaults=dict(
                description=f"Ressource de démonstration n°{j} pour la catégorie « {title} ».",
                resource_type=type_cycle[(j - 1) % len(type_cycle)],
                level=level_cycle[(j - 1) % len(level_cycle)],
                order=j,
            ),
        )
# --- FAQ ---
faq_items = [
    ("Programme", "Qui peut candidater au programme FE_SENEGAL ?",
     "Le programme s'adresse aux étudiants et jeunes chercheurs en sciences, mathématiques, "
     "épidémiologie ou informatique intéressés par la modélisation appliquée du paludisme. "
     "Un bon niveau en programmation (Python de préférence) est recommandé."),
    ("Programme", "Combien de temps dure le programme ?",
     "Le programme est une formation intensive en présentiel de 18 semaines, ponctuée de jalons "
     "hebdomadaires détaillés dans le manuel du programme."),
    ("Programme", "Le programme est-il payant ?",
     "Les frais de participation varient selon les éditions et les partenariats en cours. "
     "Contacte-nous pour connaître les modalités de l'édition en cours."),
    ("EMOD", "Qu'est-ce qu'EMOD ?",
     "EMOD est un logiciel de modélisation épidémiologique développé pour simuler la transmission "
     "de maladies comme le paludisme. Les guides pratiques de la section EMOD couvrent son "
     "installation, sa configuration et l'analyse des résultats."),
    ("EMOD", "Ai-je besoin de connaissances en programmation pour utiliser EMOD ?",
     "Oui, des bases en Python sont nécessaires pour configurer les simulations et analyser les "
     "sorties. Les guides d'installation et de simulation t'accompagnent pas à pas."),
    ("Inscription", "Comment s'inscrire aux événements de FE_SENEGAL ?",
     "Chaque événement listé dans la section Événements précise, si nécessaire, un lien "
     "d'inscription. Pour les ateliers sans lien direct, contacte-nous via le formulaire."),
    ("Inscription", "Puis-je obtenir une attestation de participation ?",
     "Oui, une attestation est délivrée aux participants ayant complété le programme ou un "
     "atelier certifiant. Adresse ta demande à notre équipe via le formulaire de contact."),
    ("Général", "Comment puis-je accéder aux ressources du site ?",
     "Toutes les ressources (documents, guides, modules) sont accessibles librement depuis la "
     "section Ressources, avec recherche et filtres par type et niveau."),
    ("Général", "Comment contacter l'équipe FE_SENEGAL ?",
     "Le plus simple est d'utiliser le formulaire sur la page Contact : nous répondons "
     "généralement sous quelques jours ouvrés."),
    ("Programme", "Le programme est-il accessible aux femmes et aux hommes de manière égale ?",
     "Oui. FE_SENEGAL encourage activement la participation des femmes dans les filières "
     "scientifiques et veille à une représentation équilibrée dans chaque promotion, sans quota "
     "fermé mais avec une politique volontariste de sensibilisation en amont des candidatures."),
    ("EMOD", "Sur quel système d'exploitation EMOD fonctionne-t-il ?",
     "EMOD fonctionne nativement sous Linux (Ubuntu recommandé). Les guides d'installation du "
     "site couvrent également la configuration sous Windows via WSL (Windows Subsystem for Linux) "
     "pour les stagiaires ne disposant pas d'une machine Linux dédiée."),
    ("Général", "Le contenu du site est-il disponible hors ligne ?",
     "Les guides et ressources peuvent être téléchargés individuellement (PDF, scripts, jeux de "
     "données) pour un usage hors connexion. Le manuel complet du programme est également "
     "téléchargeable depuis la page Manuel du programme."),
    ("Inscription", "Que se passe-t-il si je ne peux pas assister à une session en direct ?",
     "Les sessions majeures du programme sont enregistrées et mises à disposition des participants "
     "inscrits. Toute absence prolongée doit néanmoins être signalée à l'équipe pédagogique afin "
     "d'organiser un rattrapage adapté."),
]
for i, (topic, question, answer) in enumerate(faq_items, start=1):
    FAQItem.objects.get_or_create(question=question, defaults=dict(topic=topic, answer=answer, order=i))
# --- Actualités ---
news_now = timezone.now()
news_items = [
    ("Lancement officiel du programme FE_SENEGAL 2025", 10, "annonce", True,
     "L'équipe FE_SENEGAL a lancé la nouvelle promotion 2025 du programme de formation intensive "
     "en modélisation appliquée du paludisme. Dix-huit semaines d'apprentissage attendent les "
     "participants sélectionnés, avec un accent particulier sur la pratique via EMOD et l'analyse "
     "de données de santé publique réelles.\n\n"
     "Cette édition accueille des étudiants et jeunes chercheurs venus de plusieurs universités "
     "sénégalaises, avec le soutien de nos partenaires internationaux."),
    ("Atelier QGIS : cartographier les données épidémiologiques", 25, "evenement", False,
     "Un atelier pratique consacré à QGIS a réuni les participants autour de la cartographie des "
     "données de terrain collectées lors des campagnes de lutte contre le paludisme. Les "
     "participants ont appris à construire des couches de données géoréférencées et à produire "
     "des cartes exploitables pour la prise de décision locale."),
    ("Résultats de la promotion 2024 : bilan et perspectives", 60, "recherche", False,
     "La promotion 2024 du programme FE_SENEGAL a présenté ses projets finaux devant un jury "
     "d'experts en modélisation et santé publique. Plusieurs projets seront approfondis en vue "
     "d'une publication scientifique, notamment autour de la résistance aux insecticides et de la "
     "modélisation vectorielle en zone urbaine."),
    ("Partenariat renforcé avec Northwestern University", 90, "partenariat", False,
     "FE_SENEGAL annonce le renforcement de sa collaboration avec le programme Malaria Modeling de "
     "Northwestern University, incluant des sessions de mentorat conjointes et un accès élargi "
     "aux ressources pédagogiques EMOD pour l'ensemble de nos participants."),
    ("Nouvelle section Ressources : recherche et filtres", 120, "annonce", False,
     "Le site FE_SENEGAL propose désormais une recherche avancée dans la section Ressources, avec "
     "des filtres par type de contenu et niveau de difficulté, pour retrouver plus facilement "
     "documents, guides et modules."),
    ("Retour sur le séminaire de recherche ED2DS", 150, "evenement", False,
     "Le séminaire annuel de l'équipe de recherche doctorale ED2DS a rassemblé chercheurs et "
     "doctorants autour des dernières avancées en modélisation mathématique appliquée à la santé "
     "publique en Afrique de l'Ouest."),
    ("FE_SENEGAL au rendez-vous du PIARC 2027", 180, "recherche", False,
     "Une équipe de chercheurs affiliés à FE_SENEGAL prépare une contribution scientifique en vue "
     "du Congrès mondial de la route PIARC 2027, portant sur l'apport de la modélisation "
     "géospatiale aux infrastructures de santé publique."),
    ("Ouverture des candidatures pour la prochaine promotion", 200, "annonce", False,
     "Les candidatures pour la prochaine promotion du programme FE_SENEGAL sont désormais ouvertes. "
     "Consulte la page Contact pour connaître les modalités de candidature et les critères "
     "d'éligibilité."),
]
for i, (title, days_ago, category, is_featured, content) in enumerate(news_items, start=1):
    NewsArticle.objects.get_or_create(
        slug=slugify(title),
        defaults=dict(
            title=title,
            content=content,
            category=category,
            is_featured=is_featured,
            published_date=news_now - datetime.timedelta(days=days_ago),
        ),
    )
# --- Events ---
now = timezone.now()
events = [
    ("Atelier de lancement FE_SENEGAL 2025", "Dakar, Sénégal", now + datetime.timedelta(days=10)),
    ("Session de formation EMOD — Modélisation vectorielle", "UCAD, Dakar", now + datetime.timedelta(days=20)),
    ("Webinaire — Introduction à la modélisation du paludisme", "En ligne", now + datetime.timedelta(days=30)),
    ("Atelier QGIS pour la cartographie épidémiologique", "UCAD, Dakar", now + datetime.timedelta(days=40)),
    ("Séminaire de recherche ED2DS", "Thiès, Sénégal", now + datetime.timedelta(days=55)),
    ("Journée portes ouvertes FE_SENEGAL", "Dakar, Sénégal", now + datetime.timedelta(days=70)),
    ("Rencontre annuelle des modélisateurs d'Afrique de l'Ouest", "En ligne", now + datetime.timedelta(days=90)),
    ("Hackathon modélisation & santé publique", "Dakar, Sénégal", now + datetime.timedelta(days=110)),
    ("Journée scientifique FE_SENEGAL 2024", "Dakar, Sénégal", now - datetime.timedelta(days=60)),
    ("Atelier de clôture du programme 2024", "UCAD, Dakar", now - datetime.timedelta(days=120)),
    ("Conférence inaugurale FE_SENEGAL", "Dakar, Sénégal", now - datetime.timedelta(days=200)),
    ("Séminaire EMOD — Édition 2023", "En ligne", now - datetime.timedelta(days=300)),
]
for title, location, start in events:
    Event.objects.get_or_create(
        slug=slugify(title),
        defaults=dict(
            title=title,
            description=(
                f"« {title} » rassemble les membres du programme FE_SENEGAL autour de la "
                "modélisation appliquée du paludisme."
            ),
            location=location,
            start_datetime=start,
        ),
    )

print("Données de démonstration FE_SENEGAL insérées avec succès.")
# --- Galerie photo pour les événements passés ---
gallery_captions = ["Moment fort de l'événement", "Session de travail en groupe", "Photo souvenir des participants"]
demo_photo_path = os.path.join(STATIC_IMG, "hero-bg.jpg")
if os.path.exists(demo_photo_path):
    for title, location, start in events:
        if start >= now:
            continue
        event = Event.objects.filter(slug=slugify(title)).first()
        if not event or event.photos.exists():
            continue
        for i, caption in enumerate(gallery_captions, start=1):
            with open(demo_photo_path, "rb") as f:
                photo = EventPhoto(event=event, caption=caption, order=i)
                photo.image.save(f"{event.slug}-{i}.jpg", File(f), save=False)
            photo.save()

# --- Équipe (membres réels du programme, à compléter via l'admin) ---
mor_absa_loum_bio = (
    "Mor Absa Loum est enseignant-chercheur à l'Université Iba Der Thiam de Thiès, où il se "
    "consacre à la biostatistique et à la modélisation des maladies infectieuses. Après une "
    "maîtrise et un doctorat en mathématiques appliquées obtenus à l'Université Paris-Saclay, "
    "il a effectué un post-doctorat de trois ans à l'Université de Montréal, au sein du Centre "
    "de recherche du CHU Sainte-Justine, sur la modélisation de l'impact des variants génétiques "
    "sur les troubles du neurodéveloppement.\n\n"
    "À Thiès, il pilote des projets de recherche et de renforcement des capacités en modélisation "
    "du paludisme, notamment dans le cadre du projet WAMCAD et d'un programme dédié à la formation "
    "de modélisateurs. Il collabore avec des équipes internationales, encadre de jeunes "
    "professionnels en santé publique et publie régulièrement dans des revues à comité de lecture. "
    "Ses travaux visent à former des modélisateurs et à éclairer les décisions des pouvoirs publics "
    "sur l'efficacité des interventions de lutte antipaludique."
)
TeamMember.objects.get_or_create(
    slug="mor-absa-loum",
    defaults=dict(
        name="Mor Absa Loum",
        role="Enseignant-chercheur — Biostatistique & modélisation du paludisme",
        category="enseignant",
        bio=mor_absa_loum_bio,
        order=1,
        facebook_url="https://www.facebook.com/morabsa.loum",
        twitter_url="https://x.com/L_Mor_A",
        linkedin_url="https://www.linkedin.com/in/mor-absa-loum-3372aa73/",
        scholar_url="https://scholar.google.com/citations?user=EvXA_TwAAAAJ&hl=fr",
        researchgate_url="https://www.researchgate.net/profile/Mor-Absa-Loum-2",
        orcid_url="https://orcid.org/0000-0003-0349-0140",
    ),
)
# Ajoutez les autres membres réels de l'équipe directement via /admin/ (Core > Membres de l'équipe).

print("Membre de l'équipe : Mor Absa Loum inséré avec succès.")
