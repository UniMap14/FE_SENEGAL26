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

## Sauvegardes

Le site stocke tout son contenu dans `db.sqlite3` (profils, actualités, messages) et le
dossier `media/` (photos, logos). Une commande crée une archive `.zip` datée des deux :

```
python manage.py backup_site                          # -> dossier backups/
python manage.py backup_site --output D:\Sauvegardes --keep 30
python manage.py backup_site --no-media               # base de données seulement
```

- La copie de la base est cohérente même si le site est en ligne.
- Les archives les plus anciennes sont supprimées au-delà de `--keep` (14 par défaut).
- Le dossier `backups/` n'est pas suivi par Git (il contient des données personnelles).
- **Copiez régulièrement les archives ailleurs que sur le serveur** (autre disque, cloud, autre machine) : une sauvegarde sur le même disque ne protège pas d'une panne du serveur.

**Automatiser** (une sauvegarde par nuit à 2 h) :

- Linux (cron, `crontab -e`) :
  `0 2 * * * cd /chemin/du/projet && /chemin/du/venv/bin/python manage.py backup_site`
- Windows (Planificateur de tâches) :
  `schtasks /Create /SC DAILY /ST 02:00 /TN "FE_SENEGAL sauvegarde" /TR "cmd /c cd /d C:\chemin\du\projet && venv\Scripts\python.exe manage.py backup_site"`

**Restaurer** : arrêter le site, dézipper l'archive choisie, remplacer `db.sqlite3` et le
dossier `media/` du projet par ceux de l'archive, puis redémarrer le site.

## Avant la mise en production

- Générer une nouvelle `SECRET_KEY` et la définir via la variable d'environnement
  `DJANGO_SECRET_KEY` (ne jamais garder la clé de développement du dépôt)
- Mettre `DJANGO_DEBUG=False`
- Renseigner `DJANGO_ALLOWED_HOSTS` avec le(s) nom(s) de domaine réel(s)
- Fichiers statiques : WhiteNoise est déjà configuré. À chaque déploiement, lancer
`python manage.py migrate` puis `python manage.py collectstatic --noinput`, puis
redémarrer l'application (sinon l'admin s'affiche sans style).
- Médias (logo, photos de profil, galerie) : servis par Django par défaut ; si nginx/Apache
sert déjà `/media/`, définir `DJANGO_SERVE_MEDIA=False`
- Utiliser une vraie base de données (PostgreSQL recommandé) plutôt que SQLite,
  et à ce moment-là retirer `db.sqlite3` du suivi Git (voir `.gitignore`)
