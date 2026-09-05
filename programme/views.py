from django.shortcuts import render

from .models import ProgrammeYear


def handbook_view(request):
    programme_year = ProgrammeYear.objects.filter(is_current=True).first() or ProgrammeYear.objects.first()
    sections = programme_year.sections.all() if programme_year else []
    milestones = programme_year.milestones.all() if programme_year else []
    context = {
        "programme_year": programme_year,
        "sections": sections,
        "milestones": milestones,
    }
    return render(request, "programme/handbook.html", context)
