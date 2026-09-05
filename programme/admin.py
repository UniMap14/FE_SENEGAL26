from django.contrib import admin

from .models import Milestone, ProgrammeSection, ProgrammeYear


class ProgrammeSectionInline(admin.TabularInline):
    model = ProgrammeSection
    extra = 1


class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 1


@admin.register(ProgrammeYear)
class ProgrammeYearAdmin(admin.ModelAdmin):
    list_display = ("year_label", "is_current")
    list_editable = ("is_current",)
    inlines = [ProgrammeSectionInline, MilestoneInline]


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ("week", "task", "due_date", "programme_year")
    list_filter = ("programme_year",)
    ordering = ("programme_year", "order")
