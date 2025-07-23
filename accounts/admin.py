from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from favorites.models import Favorite

class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0
    readonly_fields = ("product", "added_at")

@admin.register(CustomUser)
class CustomerUserAdmin(UserAdmin):
    inlines = [FavoriteInline]
