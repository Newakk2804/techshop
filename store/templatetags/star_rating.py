from django import template

register = template.Library()


@register.filter
def filled_stars(rating):
    try:
        return range(int(rating))
    except (ValueError, TypeError):
        return range(0)


@register.filter
def empty_stars(rating):
    try:
        return range(5 - int(rating))
    except (ValueError, TypeError):
        return range(5)
