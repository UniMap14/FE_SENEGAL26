# FE_senegal — Projet Django

Site du programme de formation en modélisation appliquée du paludisme (FE_senegal),
sous forme d'application Django. Le contenu est pré-rempli par défaut (valeurs par
défaut des modèles + script de démo) et reste entièrement gérable depuis l'admin.

## Structure du projet

| App | Rôle |
|---|---|
| `core` | Accueil, À propos / Nos Missions, réglages globaux (logo, contact, réseaux sociaux) |
| `programme` | Manuel du programme + tableau des jalons |
| `emod` | Guides pratiques EMOD (catégories + guides) |
| `resources` | Ressources par catégorie |
| `events` | Événements à venir / passés |
| `contact` | Formulaire de contact (messages stockés en base, visibles dans l'admin) |

## Installation

```bash
python3 -m venv venv
source venv/bin/activate          # sous Windows : venv\Scripts\activate
pip install -r requirements.txt

python3 manage.py migrate
python3 manage.py createsuperuser
```

## Charger des données de démonstration (optionnel)

Un script `seed_demo_data.py` reproduit le contenu vu dans les captures d'écran
(missions, jalons du programme 2025, catégories EMOD, catégories de ressources) :

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
réglages de contact) se gère depuis `/admin/` — aucune modification de code n'est
nécessaire pour mettre à jour le site au quotidien.

## Avant la mise en production

- Changer `SECRET_KEY` dans `config/settings.py` (utiliser une variable d'environnement)
- Mettre `DEBUG = False`
- Renseigner `ALLOWED_HOSTS` avec le(s) nom(s) de domaine réel(s)
- Configurer un serveur de fichiers statiques/médias (ex: WhiteNoise, S3, etc.)
- Utiliser une vraie base de données (PostgreSQL recommandé) plutôt que SQLite
