# FE_SENEGAL — Projet Django

Site du programme de formation en modélisation appliquée du paludisme (FE_SENEGAL),
sous forme d'application Django. La base de données et les médias (logo, photos
d'équipe, galerie) sont inclus dans ce dépôt : après installation, le site est
immédiatement fonctionnel avec son contenu réel, et reste entièrement gérable
depuis l'admin.

## Structure du projet

| App | Rôle |
|---|---|
| `core` | Accueil, À propos / Nos Missions, Équipe (membres + profils), Galerie photo, réglages globaux (logo, contact, réseaux sociaux) |
| `programme` | Manuel du programme + tableau des jalons |
| `emod` | Guides pratiques EMOD (catégories + guides, recherche) |
| `resources` | Ressources par catégorie (recherche, filtres, ressources récentes) |
| `events` | Événements à venir / passés + galerie photo par événement |
| `news` | Actualités (catégories, article à la une) |
| `faq` | Questions fréquentes groupées par thème |
| `contact` | Formulaire de contact (messages stockés en base, visibles dans l'admin) |

## Installation

```bash
python3 -m venv venv
source venv/bin/activate          # sous Windows (PowerShell) : venv\Scripts\Activate.ps1
pip install -r requirements.txt

python3 manage.py migrate
```

La base `db.sqlite3` fournie contient déjà tout le contenu actuel du site
(guides, ressources, événements, équipe, galerie...) — `migrate` applique
seulement les éventuelles migrations en attente, il n'écrase rien.

Pour créer ton propre compte administrateur :

```bash
python3 manage.py createsuperuser
```

## Recharger des données de démonstration (optionnel)

Le script `seed_demo_data.py` peut recréer le contenu de démonstration de base
(missions, jalons, catégories EMOD/ressources, FAQ, actualités...). Il est
`get_or_create`-safe : le relancer ne duplique rien.

```bash
python3 manage.py shell < seed_demo_data.py
```

## Lancer le serveur de développement

```bash
python3 manage.py runserver
```

- Site : http://127.0.0.1:8000/
- Admin : http://127.0.0.1:8000/admin/

**Identifiants admin de démo créés pendant le développement :**
- utilisateur : `admin`
- mot de passe : `admin12345`

⚠️ Change ce mot de passe (ou recrée un superuser) avant tout déploiement réel.

## Gérer le contenu

Tout le contenu du site (textes, images, guides, ressources, jalons, événements,
membres de l'équipe, galerie, réglages de contact) se gère depuis `/admin/` —
aucune modification de code n'est nécessaire pour mettre à jour le site au
quotidien.

## Avant la mise en production

- Générer une nouvelle `SECRET_KEY` et la définir via la variable d'environnement
  `DJANGO_SECRET_KEY` (ne jamais garder la clé de développement du dépôt)
- Mettre `DJANGO_DEBUG=False`
- Renseigner `DJANGO_ALLOWED_HOSTS` avec le(s) nom(s) de domaine réel(s)
- Configurer un serveur de fichiers statiques/médias (ex: WhiteNoise, S3, etc.)
- Utiliser une vraie base de données (PostgreSQL recommandé) plutôt que SQLite,
  et à ce moment-là retirer `db.sqlite3` du suivi Git (voir `.gitignore`)
