from djoser import serializers as djoser_serializers
from rest_framework import serializers as serializers

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import Subscription, User


class UserSerializer(djoser_serializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField("get_is_subscribed")

    def get_is_subscribed(self, user_object):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, author=user_object).exists()

    class Meta(djoser_serializers.UserSerializer.Meta):
        model = User
        fields = djoser_serializers.UserSerializer.Meta.fields + ("is_subscribed",)


class UserWithRecipesSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField("get_recipes")
    recipes_count = serializers.SerializerMethodField("get_recipes_count")

    def get_recipes(self, user_object):
        return 1

    def get_recipes_count(self, user_object):
        return 0

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            "recipes",
            "recipes_count",
        )
        read_only_fields = fields


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = (
            "user",
            "author",
        )

    def validate(self, attrs):
        user = self.context.get("request").user
        author = self.initial_data.get("author")
        if user == author:
            raise serializers.ValidationError("Нельзя подписаться на самого себя!")
        if Subscription.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                "Нельзя подписаться дважды на одного пользователя!"
            )
        return super().validate(attrs)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"
