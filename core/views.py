from django.shortcuts import render

from .models import AboutPage, GalleryPhoto, HomeSlide, Mission, SiteSettings, TeamMember


def home_view(request):
    context = {
        "slides": HomeSlide.objects.filter(is_active=True),
        "about": AboutPage.load(),
        "missions": Mission.objects.all()[:5],
    }
    return render(request, "core/home.html", context)


def about_view(request):
    from emod.models import Guide
    from resources.models import Resource
    from events.models import Event

    context = {
        "about": AboutPage.load(),
        "missions": Mission.objects.all(),
        "stats": {
            "guides": Guide.objects.count(),
            "resources": Resource.objects.count(),
            "events": Event.objects.count(),
        },
    }
    return render(request, "core/about.html", context)


def gallery_view(request):
    photos = list(GalleryPhoto.objects.all())
    total_count = len(photos)

    category_counts = {}
    for p in photos:
        category_counts[p.category] = category_counts.get(p.category, 0) + 1

    category = request.GET.get("categorie")
    if category:
        photos = [p for p in photos if p.category == category]

    for i, p in enumerate(photos):
        p.next_id = photos[(i + 1) % len(photos)].id if photos else None
        p.prev_id = photos[(i - 1) % len(photos)].id if photos else None

    categories_with_counts = [
        {"key": key, "label": label, "count": category_counts.get(key, 0)}
        for key, label in GalleryPhoto.CATEGORY_CHOICES
    ]

    context = {
        "photos": photos,
        "categories": categories_with_counts,
        "active_category": category,
        "total_count": total_count,
    }
    return render(request, "core/gallery.html", context)


def team_list_view(request):
    members = TeamMember.objects.filter(is_active=True)
    category = request.GET.get("categorie", "").strip()
    if category:
        members = members.filter(category=category)

    context = {
        "members": members,
        "categories": TeamMember.CATEGORY_CHOICES,
        "active_category": category,
        "total_count": TeamMember.objects.filter(is_active=True).count(),
    }
    return render(request, "core/team_list.html", context)


def team_detail_view(request, slug):
    from django.shortcuts import get_object_or_404
    member = get_object_or_404(TeamMember, slug=slug, is_active=True)
    others = TeamMember.objects.filter(is_active=True).exclude(pk=member.pk)[:3]
    context = {"member": member, "others": others}
    return render(request, "core/team_detail.html", context)
