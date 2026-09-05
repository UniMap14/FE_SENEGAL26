from .models import Partner, SiteSettings, SocialLink

HERO_IMAGES = [f"img/hero-slides/hero-{i:02d}.jpg" for i in range(1, 13)]


def site_globals(request):
    return {
        "site_settings": SiteSettings.load(),
        "social_links": SocialLink.objects.all(),
        "partners": Partner.objects.all(),
        "hero_images": HERO_IMAGES,
    }
