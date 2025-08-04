from django import template
from django.core.cache import cache
from store.models import Category


register = template.Library()


@register.simple_tag
def get_all_categories():
    categories = cache.get("all_categories")
    if categories is None:
        categories = list(Category.objects.all())
        cache.set("all_categories", categories, 60 * 60)

    return categories
