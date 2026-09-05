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
    list_display = ("name", "role", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "role", "bio")
    prepopulated_fields = {"slug": ("name",)}
