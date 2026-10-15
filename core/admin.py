from django.contrib import admin

from .models import AboutPage, GalleryPhoto, HomeSlide, Mission, Partner, SiteSettings, SocialLink, TeamMember


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "order")
    list_editable = ("order",)


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("text", "order")
    list_editable = ("order",)


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not AboutPage.objects.exists()


@admin.register(HomeSlide)
class HomeSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order")
    list_editable = ("order",)


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ("caption", "category", "order", "created_at")
    list_editable = ("order",)
    list_filter = ("category",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "category", "cohort_year", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category", "cohort_year", "is_active")
    search_fields = ("name", "first_name", "last_name", "role", "organization", "country", "bio")
    readonly_fields = ("slug",)
    fieldsets = (
        ("1. Identité", {"fields": ("first_name", "last_name", "name", "role", "organization")}),
        ("2. Coordonnées", {"fields": ("email", "phone", "show_phone", "country")}),
        ("3. Présentation", {"fields": ("bio",)}),
        ("4. Liens", {"fields": (
            "website_url", "linkedin_url", "scholar_url", "orcid_url", "researchgate_url",
            "youtube_url", "facebook_url", "twitter_url", "other_url",
        )}),
        ("5. Photo de profil", {"fields": ("photo",)}),
        ("Affichage sur le site", {"fields": ("category", "cohort_year", "order", "is_active", "slug")}),
    )
