from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"


@register.inclusion_tag("users/profile_detail.html")
def render_user_card(user):
    return {"user": user}
