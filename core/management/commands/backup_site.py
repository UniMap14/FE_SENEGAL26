"""Sauvegarde complète du site : base de données + médias, dans une archive .zip datée.

Usage :
    python manage.py backup_site                      # -> dossier backups/
    python manage.py backup_site --output D:\\Sauvegardes --keep 30
    python manage.py backup_site --no-media           # base de données seulement

La copie de la base utilise l'API de sauvegarde de SQLite : elle est cohérente même si le
site est en cours d'utilisation. Les archives les plus anciennes sont supprimées au-delà
de --keep (14 par défaut). Pensez à copier régulièrement le dossier de sauvegarde AILLEURS
que sur le serveur (autre disque, cloud, autre machine).
"""
import sqlite3
import zipfile
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.utils import timezone

PREFIX = "fe_senegal_backup_"


class Command(BaseCommand):
    help = "Sauvegarde la base de données SQLite et les médias dans une archive .zip datée."

    def add_arguments(self, parser):
        parser.add_argument("--output", default=str(settings.BASE_DIR / "backups"),
                            help="Dossier de destination (par défaut : backups/ à la racine du projet).")
        parser.add_argument("--keep", type=int, default=14,
                            help="Nombre d'archives à conserver (défaut : 14, les plus anciennes sont supprimées).")
        parser.add_argument("--no-media", action="store_true",
                            help="Ne sauvegarder que la base de données (sans le dossier media/).")

    def handle(self, *args, **options):
        if connection.vendor != "sqlite":
            raise CommandError(
                "Cette commande ne gère que SQLite. Avec PostgreSQL, utilisez pg_dump "
                "(et copiez aussi le dossier media/)."
            )
        if options["keep"] < 1:
            raise CommandError("--keep doit être au moins 1.")

        out_dir = Path(options["output"]).expanduser()
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = timezone.localtime().strftime("%Y-%m-%d_%H%M%S")
        archive = out_dir / f"{PREFIX}{stamp}.zip"
        n = 1
        while archive.exists():
            archive = out_dir / f"{PREFIX}{stamp}-{n}.zip"
            n += 1

        tmp_db = out_dir / f".tmp-{stamp}.sqlite3"
        try:
            connection.ensure_connection()
            dest = sqlite3.connect(str(tmp_db))
            try:
                connection.connection.backup(dest)  # copie cohérente, même site en ligne
            finally:
                dest.close()

            media_count = 0
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(tmp_db, "db.sqlite3")
                media_root = Path(settings.MEDIA_ROOT)
                if not options["no_media"] and media_root.is_dir():
                    for f in sorted(media_root.rglob("*")):
                        if f.is_file():
                            zf.write(f, Path("media") / f.relative_to(media_root))
                            media_count += 1
                zf.writestr(
                    "LISEZ-MOI.txt",
                    f"Sauvegarde FE_SENEGAL du {timezone.localtime():%d/%m/%Y à %H:%M:%S}\n"
                    f"Contenu : db.sqlite3 + {media_count} fichier(s) média.\n"
                    "Restauration : arrêter le site, remplacer db.sqlite3 et le dossier media/ "
                    "du projet par ceux de cette archive, puis redémarrer.\n",
                )
        finally:
            if tmp_db.exists():
                tmp_db.unlink()

        # Rotation : ne garder que les --keep archives les plus récentes
        archives = sorted(out_dir.glob(f"{PREFIX}*.zip"))
        removed = 0
        for old in archives[:-options["keep"]]:
            old.unlink()
            removed += 1

        size_mb = archive.stat().st_size / (1024 * 1024)
        self.stdout.write(self.style.SUCCESS(
            f"Sauvegarde créée : {archive} ({size_mb:.1f} Mo, {media_count} média(s))"
        ))
        if removed:
            self.stdout.write(f"{removed} ancienne(s) sauvegarde(s) supprimée(s) (conservées : {options['keep']}).")
