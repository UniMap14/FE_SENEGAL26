from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Event


def event_list_view(request):
    now = timezone.now()
    upcoming = Event.objects.filter(start_datetime__gte=now)
    past = Event.objects.filter(start_datetime__lt=now).order_by("-start_datetime")

    upcoming_paginator = Paginator(upcoming, 6)
    upcoming_page = upcoming_paginator.get_page(request.GET.get("page_upcoming"))

    past_paginator = Paginator(past, 6)
    past_page = past_paginator.get_page(request.GET.get("page_past"))

    context = {
        "upcoming_events": upcoming_page.object_list,
        "upcoming_page_obj": upcoming_page,
        "past_events": past_page.object_list,
        "past_page_obj": past_page,
    }
    return render(request, "events/event_list.html", context)


def event_detail_view(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, "events/event_detail.html", {"event": event})