import base64
import binascii
import imghdr
import uuid

import six
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser import serializers as djoser_serializers
from rest_framework import serializers as serializers

from ingredients.models import Ingredient
from recipes.models import IngredientInRecipe, Recipe
from tags.models import Tag
from users.models import Subscription, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if "data:" in data and ";base64," in data:
                _, data = data.split(";base64,")
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("invalid_image")
            except binascii.Error:
                self.fail("invalid_image")
            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = f"{file_name}.{file_extension}"
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
        read_only_fields = fields


class UserSerializer(djoser_serializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField("get_is_subscribed")

    def get_is_subscribed(self, user_object):
        user = self.context["request"].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, author=user_object).exists()
        return False

    class Meta(djoser_serializers.UserSerializer.Meta):
        model = User
        fields = djoser_serializers.UserSerializer.Meta.fields + ("is_subscribed",)


class UserWithRecipesSerializer(UserSerializer):
    recipes = RecipeMinifiedSerializer(many=True)
    recipes_count = serializers.SerializerMethodField("get_recipes_count")

    def get_recipes_count(self, user_object):
        # TODO
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


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source="ingredient", slug_field="id", queryset=Ingredient.objects.all()
    )
    name = serializers.SlugRelatedField(
        source="ingredient", slug_field="name", read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source="ingredient", slug_field="measurement_unit", read_only=True
    )

    class Meta:
        model = IngredientInRecipe
        exclude = (
            "recipe",
            "ingredient",
        )


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientInRecipeSerializer(
        source="ingredientinrecipe_set", many=True
    )
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        depth = 2
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def create(self, validated_data):
        ingredientinrecipe_set = validated_data.pop("ingredientinrecipe_set")
        tags = validated_data.pop("tags")

        instance = Recipe.objects.create(**validated_data)

        for ingredientinrecipe in ingredientinrecipe_set:
            ingredient = ingredientinrecipe["ingredient"]
            amount = ingredientinrecipe["amount"]
            instance.ingredients.add(ingredient, through_defaults={"amount": amount})
        instance.tags.set(tags)

        return instance

    def update(self, instance, validated_data):
        if "ingredientinrecipe_set" in validated_data:
            ingredientinrecipe_set = validated_data.pop("ingredientinrecipe_set")
            if ingredientinrecipe_set:
                instance.ingredients.clear()
            for ingredientinrecipe in ingredientinrecipe_set:
                ingredient = ingredientinrecipe["ingredient"]
                amount = ingredientinrecipe["amount"]
                instance.ingredients.add(
                    ingredient, through_defaults={"amount": amount}
                )
        return super().update(instance, validated_data)

    def is_valid(self, raise_exception=False):
        if raise_exception:
            tags_id = self.initial_data.get("tags")
            if isinstance(tags_id, list):
                for id in tags_id:
                    get_object_or_404(Tag, id=id)
            ingredients = self.initial_data.get("ingredients")
            if isinstance(ingredients, list):
                for ingredient in ingredients:
                    get_object_or_404(Ingredient, id=ingredient["id"])
        return super().is_valid(raise_exception)


class RecipeListSerializer(serializers.ModelSerializer):
    author = UserSerializer(default=serializers.CurrentUserDefault(), read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientInRecipeSerializer(
        source="ingredientinrecipe_set", many=True
    )
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField("get_is_favorited")
    is_in_shopping_cart = serializers.SerializerMethodField("get_is_in_shopping_cart")

    class Meta:
        model = Recipe
        exclude = (
            "carts",
            "created",
            "favorites",
        )

    def get_is_favorited(self, recipe):
        user = self.context.get("request").user
        if user.is_authenticated:
            return user.favorite_recipes.filter(id=recipe.id).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get("request").user
        if user.is_authenticated:
            return user.cart_recipes.filter(id=recipe.id).exists()
