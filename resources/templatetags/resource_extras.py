from django import template

register = template.Library()

ICONS = {
    "document": "📄",
    "guide": "📘",
    "module": "🧩",
    "lien": "🔗",
}


@register.filter
def resource_icon(resource_type):
    return ICONS.get(resource_type, "📄")
