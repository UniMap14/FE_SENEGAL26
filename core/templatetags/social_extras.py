from django import template
from django.utils.safestring import mark_safe

register = template.Library()

BRAND_COLORS = {
    "facebook": "#1877F2",
    "twitter": "#000000",
    "linkedin": "#0A66C2",
    "youtube": "#FF0000",
    "wordpress": "#21759B",
    "instagram": "#E4405F",
    "scholar": "#4285F4",
    "researchgate": "#00CCBB",
    "orcid": "#A6CE39",
    "other": "#0B1A3D",
}

_SVGS = {
    "facebook": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5 3.66 9.15 8.44 9.94v-7.03H7.9v-2.9h2.54V9.85c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.88h2.78l-.44 2.9h-2.34v7.03C18.34 21.21 22 17.06 22 12.06z"/></svg>',
    "twitter": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2h3.1l-7.6 8.7L23 22h-6.6l-5.2-6.6L5.2 22H2.1l8.1-9.3L1 2h6.8l4.7 6.1L18.9 2zm-1.2 18.2h1.7L7.4 3.7H5.6l12.1 16.5z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.1c.55-1 1.9-2 3.9-2 4.1 0 4.9 2.6 4.9 6.1V21h-4v-5.3c0-1.3 0-2.9-1.8-2.9s-2.1 1.4-2.1 2.8V21H9z"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4l6.3 3.6z"/></svg>',
    "wordpress": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM3.5 12c0-1.3.3-2.6.8-3.7l4.4 12A8.5 8.5 0 0 1 3.5 12zm8.5 8.5c-.7 0-1.5-.1-2.1-.3l2.3-6.6 2.3 6.4c0 .1.1.2.1.3-.8.2-1.7.2-2.6.2zm1.1-12.5c.5 0 .9-.1.9-.1.4 0 .4-.7 0-.6 0 0-1.2.1-2 .1-.7 0-2-.1-2-.1-.4 0-.5.6 0 .6 0 0 .4.1.8.1l1.2 3.3-1.7 5-2.8-8.3c.5 0 .9-.1.9-.1.4 0 .4-.7-.1-.6 0 0-1.2.1-2 .1-.1 0-.3 0-.5 0A8.5 8.5 0 0 1 12 3.5c1.9 0 3.6.7 4.9 1.8-1.4-.1-2.4.9-2.4 2.1 0 1 .5 1.8 1.1 2.7.4.7.9 1.6.9 3 0 .9-.3 1.9-.7 3.3l-1 3.2-3.5-10.3zm5.2 1.2c.6 1.1 1 2.4 1 3.8 0 1.2-.2 2.2-.6 3.1l-2.7 7.7A8.5 8.5 0 0 0 20.5 12c0-1.6-.4-3-1.2-4.3z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>',
    "scholar": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 3 1 9.5l4 2.3v5.7l7 3.5 7-3.5v-5.7l2-1.2v6.4h1.5V9.5zM12 4.8l7.7 4.5L12 13.8 4.3 9.3zM6 13l6 3.4 6-3.4v3.7l-6 3-6-3z"/></svg>',
    "researchgate": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="10"/><text x="12" y="15.5" font-size="8.2" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" fill="currentColor" stroke="none">RG</text></svg>',
    "orcid": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="10"/><text x="12" y="15.5" font-size="8" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" fill="currentColor" stroke="none">iD</text></svg>',
    "other": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M10 13a5 5 0 0 0 7 0l2.5-2.5a5 5 0 0 0-7-7L11 5"/><path d="M14 11a5 5 0 0 0-7 0L4.5 13.5a5 5 0 0 0 7 7L13 19"/></svg>',
}


@register.filter
def social_svg(kind):
    return mark_safe(_SVGS.get(kind, _SVGS["other"]))


@register.filter
def brand_color(kind):
    return BRAND_COLORS.get(kind, "#0B1A3D")
