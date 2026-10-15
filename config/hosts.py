"""Aide à la configuration des domaines (hôtes autorisés, origines CSRF de confiance)."""
import re

_LOCAL = {"localhost", "127.0.0.1", "testserver", "[::1]", "*"}
_IP = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")


def trusted_origins_from_hosts(hosts):
    """Déduit les origines CSRF de confiance (https://domaine) des domaines autorisés.

    - "monsite.sn"      -> "https://monsite.sn"
    - ".monsite.sn"     -> "https://*.monsite.sn" (tous les sous-domaines)
    - localhost, IP, "*" -> ignorés
    Sans cela, la connexion à /admin/ échoue en production avec « Origin checking failed »
    quand DJANGO_CSRF_TRUSTED_ORIGINS n'est pas renseignée.
    """
    origins = []
    for host in hosts:
        host = (host or "").strip()
        if not host or host in _LOCAL or _IP.match(host):
            continue
        origin = f"https://*{host}" if host.startswith(".") else f"https://{host}"
        if origin not in origins:
            origins.append(origin)
    return origins
