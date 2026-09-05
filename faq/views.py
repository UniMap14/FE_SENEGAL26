from django.shortcuts import render

from .models import FAQItem


def faq_view(request):
    items = FAQItem.objects.filter(is_published=True)
    context = {"items": items}
    return render(request, "faq/faq.html", context)