from django.contrib.auth.base_user import AbstractBaseUser
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from djoser import views
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    IngredientSerializer,
    RecipeListSerializer,
    RecipeSerializer,
    UserWithRecipesSerializer,
    SubscriptionSerializer,
    TagSerializer,
)
from ingredients.models import Ingredient
from recipes.models import Recipe
from tags.models import Tag
from users.models import Subscription, User


class TokenCreateView(views.TokenCreateView):
    def _action(self, serializer):
        response = super()._action(serializer)
        if response.status_code == status.HTTP_200_OK:
            response.status_code = status.HTTP_201_CREATED
        return response


class UserWithRecipesViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserWithRecipesSerializer
    permission_classes = (IsAuthenticated,)

    def get_author(self) -> User:
        return get_object_or_404(User, id=self.kwargs.get("author_id"))

    def get_object(self):
        return get_object_or_404(
            Subscription, user=self.request.user, author=self.get_author()
        )

    def destroy(self, request, *args, **kwargs):
        self.get_author()
        try:
            self.get_object()
        except Http404:
            data = {"errors": "Нельзя отпистаться от того, на кого не подписан."}
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in (
            "create",
            "destroy",
        ):
            return SubscriptionSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if isinstance(self.request.user, AbstractBaseUser):
            return User.objects.filter(subscribed__user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data.update(author=self.get_author())
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer = self.serializer_class(
            instance=self.get_author(), context=self.get_serializer_context()
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(author=self.get_author())


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    pagination_class = None

    def get_queryset(self):
        return Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get("name")
        if name is not None:
            queryset = queryset.filter(name__startswith=name)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeListSerializer
    create_serializer_class = RecipeSerializer
    partial_update_serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        queryset = Recipe.objects.all()
        # TODO
        # is_favorited = self.request.query_params.get("is_favorited")
        # is_in_shopping_cart = self.request.query_params.get("is_in_shopping_cart")
        # author = self.request.query_params.get("author")
        # tags = self.request.query_params.get("tags")
        # if name is not None:
        #     queryset = queryset.filter(name__startswith=name)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer = self.serializer_class(
            instance=recipe, context=self.get_serializer_context()
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return self.create_serializer_class
        if self.action == "partial_update":
            return self.partial_update_serializer_class
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        # super().update(request, *args, **kwargs)
        serializer = self.serializer_class(
            instance=self.get_object(), context=self.get_serializer_context()
        )
        return Response(serializer.data)

    # def handle_exception(self, exc):
    #     response = super().handle_exception(exc)
    #     if response.status_code == status.HTTP_401_UNAUTHORIZED:
    #         return Response(
    #             status=status.HTTP_401_UNAUTHORIZED, headers=response.headers
    #         )
    #     return response
