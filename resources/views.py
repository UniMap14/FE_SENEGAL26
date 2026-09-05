from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Resource, ResourceCategory


def resources_index_view(request):
    categories = ResourceCategory.objects.all()

    query = request.GET.get("q", "").strip()
    resource_type = request.GET.get("type", "").strip()
    level = request.GET.get("level", "").strip()
    is_search = bool(query or resource_type or level)

    results = None
    if is_search:
        results = Resource.objects.select_related("category").all()
        if query:
            results = results.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if resource_type:
            results = results.filter(resource_type=resource_type)
        if level:
            results = results.filter(level=level)

    context = {
        "categories": categories,
        "is_search": is_search,
        "results": results,
        "query": query,
        "selected_type": resource_type,
        "selected_level": level,
        "type_choices": Resource.TYPE_CHOICES,
        "level_choices": Resource.LEVEL_CHOICES,
        "total_resources": Resource.objects.count(),
        "recent_resources": Resource.objects.select_related("category").order_by("-id")[:4],
    }
    return render(request, "resources/resource_index.html", context)


def category_detail_view(request, slug):
    categories = ResourceCategory.objects.all()
    category = get_object_or_404(ResourceCategory, slug=slug)
    context = {"categories": categories, "category": category, "resources": category.resources.all()}
    return render(request, "resources/category_detail.html", context)