from django.contrib.auth.base_user import AbstractBaseUser
from djoser import serializers as djoser_serializers
from rest_framework import serializers as serializers

from ingredients.models import Ingredient
from recipes.models import IngredientInRecipe, Recipe
from tags.models import Tag
from users.models import Subscription, User


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if "data:" in data and ";base64," in data:
                # Break out the header from the base64 content
                header, data = data.split(";base64,")

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("invalid_image")

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (
                file_name,
                file_extension,
            )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


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


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source="ingredient", slug_field="id", read_only=True
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
    author = UserSerializer(default=serializers.CurrentUserDefault(), read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientInRecipeSerializer(
        source="ingredientinrecipe_set", many=True
    )
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField("get_is_favorited")
    is_in_shopping_cart = serializers.SerializerMethodField("get_is_in_shopping_cart")

    def get_is_favorited(self, recipe):
        # TODO
        return True

    def get_is_in_shopping_cart(self, recipe):
        # TODO
        return True

    class Meta:
        model = Recipe
        exclude = (
            "carts",
            "created",
            "favorites",
        )
