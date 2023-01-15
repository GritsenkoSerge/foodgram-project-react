from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import Subscription, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    @admin.display(description="Количество подписчиков")
    def subscription_amount(self):
        """Количество подписчиков для вывода в админке."""
        return self.subscriptions.count()

    @admin.display(description="Количество рецептов")
    def recipe_amount(self):
        """Количество рецептов для вывода в админке."""
        return self.recipes.count()

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )
    list_filter = (
        "is_superuser",
        "is_staff",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональная информация",
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = (
        "username",
        "email",
    )
    ordering = ("email",)
    filter_horizontal = ()
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


admin.site.unregister(Group)
