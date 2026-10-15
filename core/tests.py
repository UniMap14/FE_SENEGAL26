import tempfile
import zipfile
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase, override_settings


class BackupCommandTests(TestCase):
    def test_backup_contains_db_and_media_and_rotates(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            media = tmp / "media"
            (media / "team").mkdir(parents=True)
            (media / "team" / "photo.jpg").write_bytes(b"fake-image")
            out = tmp / "out"
            out.mkdir()
            for old in ("2020-01-01_000000", "2020-01-02_000000"):
                (out / f"fe_senegal_backup_{old}.zip").write_bytes(b"x")

            with override_settings(MEDIA_ROOT=str(media)):
                call_command("backup_site", output=str(out), keep=2, verbosity=0)

            archives = sorted(out.glob("fe_senegal_backup_*.zip"))
            self.assertEqual(len(archives), 2)  # rotation : seules les 2 plus récentes restent
            self.assertFalse((out / "fe_senegal_backup_2020-01-01_000000.zip").exists())
            with zipfile.ZipFile(archives[-1]) as zf:
                names = zf.namelist()
            self.assertIn("db.sqlite3", names)
            self.assertIn("media/team/photo.jpg", names)
            self.assertFalse(list(out.glob(".tmp-*")))  # pas de fichier temporaire oublié


class AdminProfileEditTests(TestCase):
    """Un profil ajouté depuis l'admin doit pouvoir être modifié ensuite depuis l'admin."""

    def setUp(self):
        from django.contrib.auth import get_user_model
        get_user_model().objects.create_superuser("chef", "chef@example.org", "mot-de-passe-test-123")
        self.client.login(username="chef", password="mot-de-passe-test-123")
        self._media = tempfile.TemporaryDirectory()
        self._override = override_settings(MEDIA_ROOT=self._media.name)
        self._override.enable()

    def tearDown(self):
        self._override.disable()
        self._media.cleanup()

    @staticmethod
    def _png(color):
        import io
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        buf = io.BytesIO()
        Image.new("RGB", (40, 40), color).save(buf, "PNG")
        return SimpleUploadedFile("photo.png", buf.getvalue(), content_type="image/png")

    def _form(self, **over):
        data = {
            "first_name": "Aminata", "last_name": "Ndiaye", "name": "", "role": "Doctorante",
            "organization": "UIDT", "email": "", "phone": "", "country": "Sénégal",
            "bio": "Première version.", "website_url": "", "linkedin_url": "", "scholar_url": "",
            "orcid_url": "", "researchgate_url": "", "youtube_url": "", "facebook_url": "",
            "twitter_url": "", "other_url": "", "category": "participant", "cohort_year": "2026",
            "order": "0", "is_active": "on",
        }
        data.update(over)
        return data

    def test_add_then_edit_profile_from_admin(self):
        from django.urls import reverse
        from core.models import TeamMember

        # 1) Ajout depuis l'admin, avec photo
        r = self.client.post(reverse("admin:core_teammember_add"), self._form(photo=self._png("red")))
        self.assertEqual(r.status_code, 302, getattr(r, "context", None) and r.context["adminform"].form.errors)
        m = TeamMember.objects.get(last_name="Ndiaye")
        self.assertEqual(m.name, "Aminata Ndiaye")
        slug, old_photo = m.slug, m.photo.name
        self.assertEqual(self.client.get(m.get_absolute_url()).status_code, 200)

        # 2) Modification : prénom corrigé, nouvelle bio, nouvelle photo, promotion changée
        url = reverse("admin:core_teammember_change", args=[m.pk])
        r = self.client.post(url, self._form(first_name="Aïssatou", name="Aminata Ndiaye", bio="Bio mise à jour.",
                                             cohort_year="2025", photo=self._png("blue")))
        self.assertEqual(r.status_code, 302)
        m.refresh_from_db()
        self.assertEqual(m.bio, "Bio mise à jour.")
        self.assertEqual(m.cohort_year, 2025)
        self.assertNotEqual(m.photo.name, old_photo)             # photo remplacée
        self.assertEqual(m.slug, slug)                            # l'adresse de la page ne change pas
        self.assertEqual(m.name, "Aïssatou Ndiaye")               # le nom affiché suit le prénom corrigé
        page = self.client.get(m.get_absolute_url()).content.decode()
        self.assertIn("Bio mise à jour.", page)
        self.assertIn("Aïssatou Ndiaye", page)

    def test_custom_display_name_is_kept_on_edit(self):
        from django.urls import reverse
        from core.models import TeamMember
        self.client.post(reverse("admin:core_teammember_add"), self._form(name="Dr Aminata Ndiaye"))
        m = TeamMember.objects.get(last_name="Ndiaye")
        self.client.post(reverse("admin:core_teammember_change", args=[m.pk]),
                         self._form(name="Dr Aminata Ndiaye", first_name="Aminata", bio="Autre bio."))
        m.refresh_from_db()
        self.assertEqual(m.name, "Dr Aminata Ndiaye")             # un nom d'affichage choisi n'est jamais écrasé
        self.assertEqual(m.bio, "Autre bio.")
