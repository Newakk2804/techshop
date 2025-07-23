from django import template
from favorites.models import Favorite

register = template.Library()


@register.simple_tag
def is_favorited(product, user):
    if not user.is_authenticated:
        return False
    return Favorite.objects.filter(user=user, product=product).exists()
