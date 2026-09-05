from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import NewsArticle


def news_list_view(request):
    base_qs = NewsArticle.objects.filter(is_published=True, published_date__lte=timezone.now())

    category = request.GET.get("categorie", "").strip()
    if category:
        base_qs = base_qs.filter(category=category)

    featured = None
    articles_qs = base_qs
    if not category and not request.GET.get("page"):
        featured = base_qs.filter(is_featured=True).first() or base_qs.first()
        if featured:
            articles_qs = base_qs.exclude(pk=featured.pk)

    paginator = Paginator(articles_qs, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "articles": page_obj.object_list,
        "page_obj": page_obj,
        "featured": featured,
        "categories": NewsArticle.CATEGORY_CHOICES,
        "active_category": category,
    }
    return render(request, "news/news_list.html", context)


def news_detail_view(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug, is_published=True)
    other_articles = (
        NewsArticle.objects.filter(is_published=True)
        .exclude(pk=article.pk)
        .order_by("-published_date")[:3]
    )
    context = {"article": article, "other_articles": other_articles}
    return render(request, "news/news_detail.html", context)