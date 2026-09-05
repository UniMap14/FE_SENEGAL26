from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Guide, GuideCategory


def emod_index_view(request):
    categories = GuideCategory.objects.all()

    query = request.GET.get("q", "").strip()
    search_results = None
    if query:
        search_results = Guide.objects.select_related("category").filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    context = {
        "categories": categories,
        "total_guides": Guide.objects.count(),
        "query": query,
        "search_results": search_results,
    }
    return render(request, "emod/guide_index.html", context)


def guide_category_view(request, slug):
    categories = GuideCategory.objects.all()
    category = get_object_or_404(GuideCategory, slug=slug)

    paginator = Paginator(category.guides.all(), 8)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {"categories": categories, "category": category, "guides": page_obj.object_list, "page_obj": page_obj}
    return render(request, "emod/guide_category.html", context)


def guide_detail_view(request, category_slug, slug):
    categories = GuideCategory.objects.all()
    category = get_object_or_404(GuideCategory, slug=category_slug)
    guide = get_object_or_404(Guide, category=category, slug=slug)

    siblings = list(category.guides.all())
    index = next((i for i, g in enumerate(siblings) if g.pk == guide.pk), None)
    prev_guide = siblings[index - 1] if index is not None and index > 0 else None
    next_guide = siblings[index + 1] if index is not None and index < len(siblings) - 1 else None

    context = {
        "categories": categories,
        "category": category,
        "guide": guide,
        "prev_guide": prev_guide,
        "next_guide": next_guide,
        "position": (index + 1) if index is not None else None,
        "total_in_category": len(siblings),
    }
    return render(request, "emod/guide_detail.html", context)