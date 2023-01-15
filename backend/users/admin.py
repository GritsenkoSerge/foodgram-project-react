from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from .models import Subscription, User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "is_active",
            "is_superuser",
            "is_staff",
        )


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

    form = UserChangeForm
    add_form = UserCreationForm

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
            "Доступ",
            {
                "fields": (
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
