from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Subscription, User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    @admin.display(description="Количество подписчиков")
    def subscription_amount(self):
        """Количество подписчиков для вывода в админке."""
        return self.subscriptions.count()

    @admin.display(description="Количество рецептов")
    def recipe_amount(self):
        """Количество рецептов для вывода в админке."""
        return self.recipes.count()

    list_display = (
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    search_fields = (
        "username",
        "email",
    )
    list_filter = (
        "username",
        "email",
    )
    readonly_fields = (
        subscription_amount,
        recipe_amount,
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "author",
    )
    search_fields = (
        "user",
        "author",
    )
    list_filter = (
        "user",
        "author",
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE
