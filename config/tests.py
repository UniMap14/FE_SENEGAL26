from django.contrib.auth import get_user_model
from django.test import Client, SimpleTestCase, TestCase, override_settings

from .hosts import trusted_origins_from_hosts

SITE = "fe-senegal.uidt.sn"


class TrustedOriginsTests(SimpleTestCase):
    def test_derived_from_hosts(self):
        self.assertEqual(
            trusted_origins_from_hosts(["localhost", "127.0.0.1", "testserver", SITE, " www.x.sn ", ".uidt.sn", "10.0.0.5", "*", ""]),
            [f"https://{SITE}", "https://www.x.sn", "https://*.uidt.sn"],
        )

    def test_no_duplicates(self):
        self.assertEqual(trusted_origins_from_hosts([SITE, SITE]), [f"https://{SITE}"])


@override_settings(ALLOWED_HOSTS=[SITE])
class AdminLoginCsrfTests(TestCase):
    """Reproduit l'erreur « Origin checking failed » vue sur le site en ligne."""

    def setUp(self):
        get_user_model().objects.create_superuser("chef", "chef@example.org", "mot-de-passe-test-123")

    def _login(self, origin):
        c = Client(enforce_csrf_checks=True, HTTP_HOST=SITE)
        c.get("/admin/login/")  # pose le cookie CSRF
        token = c.cookies["csrftoken"].value
        # connexion vue comme "http" par Django (proxy qui ne transmet pas le https), Origin en https
        return c.post(
            "/admin/login/",
            {"username": "chef", "password": "mot-de-passe-test-123", "csrfmiddlewaretoken": token, "next": "/admin/"},
            HTTP_ORIGIN=origin,
        )

    def test_login_refused_without_trusted_origin(self):
        with override_settings(CSRF_TRUSTED_ORIGINS=[]):
            self.assertEqual(self._login(f"https://{SITE}").status_code, 403)

    def test_login_works_with_derived_origin(self):
        with override_settings(CSRF_TRUSTED_ORIGINS=trusted_origins_from_hosts([SITE])):
            self.assertEqual(self._login(f"https://{SITE}").status_code, 302)

    def test_foreign_origin_still_refused(self):
        with override_settings(CSRF_TRUSTED_ORIGINS=trusted_origins_from_hosts([SITE])):
            self.assertEqual(self._login("https://site-malveillant.example").status_code, 403)
