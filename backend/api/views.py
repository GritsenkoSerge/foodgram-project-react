import pdfkit
from datetime import datetime
from django.db.models import Sum
from django.db.models.query_utils import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from djoser import views
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    IngredientSerializer,
    RecipeListSerializer,
    RecipeMinifiedSerializer,
    RecipeSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserWithRecipesSerializer,
)
from ingredients.models import Ingredient
from recipes.models import (
    IngredientInRecipe,
    FavoriteRecipe,
    Recipe,
    TagRecipe,
    ShoppingCartRecipe,
)
from tags.models import Tag
from users.models import Subscription, User


class TokenCreateView(views.TokenCreateView):
    def _action(self, serializer):
        response = super()._action(serializer)
        # По ТЗ нужен ответ 201, в то время как Djoser возвращает 200
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
        if self.request.user.is_authenticated:
            return User.objects.filter(authors__user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data.update(author=self.get_author())
        super().create(request, *args, **kwargs)
        serializer = self.serializer_class(
            instance=self.get_author(), context=self.get_serializer_context()
        )
        headers = self.get_success_headers(serializer.data)
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
            qs_starts = queryset.filter(name__istartswith=name)
            qs_contains = queryset.filter(
                ~Q(name__istartswith=name) & Q(name__icontains=name)
            )
            # преобразуем в list, чтобы результирующий queryset
            # имел первоначальную сортировку
            queryset = list(qs_starts) + list(qs_contains)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeListSerializer
    edit_serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_serializer_class(self):
        if self.action in (
            "create",
            "partial_update",
        ):
            return self.edit_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = Recipe.objects.all()
        user = self.request.user
        is_favorited = self.request.query_params.get("is_favorited")
        if is_favorited:
            if user.is_authenticated:
                recipes_id = user.favorite_recipes.values("id")
            else:
                recipes_id = []
            condition = Q(id__in=recipes_id)
            queryset = queryset.filter(
                condition if is_favorited == "1" else ~condition
            ).all()
        is_in_shopping_cart = self.request.query_params.get("is_in_shopping_cart")
        if is_in_shopping_cart:
            if user.is_authenticated:
                recipes_id = user.shopping_cart_recipes.values("id")
            else:
                recipes_id = []
            condition = Q(id__in=recipes_id)
            queryset = queryset.filter(
                condition if is_in_shopping_cart == "1" else ~condition
            ).all()
        author_id = self.request.query_params.get("author")
        if author_id:
            queryset = queryset.filter(author__id=author_id).all()
        tags = self.request.query_params.getlist("tags")
        if tags:
            tags = Tag.objects.filter(slug__in=tags).all()
            recipes_id = (
                TagRecipe.objects.filter(tag__in=tags).values("recipe__id").distinct()
            )
            queryset = queryset.filter(id__in=recipes_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # после создания возвращаем основной сериализатор
        serializer = self.serializer_class(
            instance=recipe, context=self.get_serializer_context()
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        # после изменения возвращаем основной сериализатор
        serializer = self.serializer_class(
            instance=self.get_object(), context=self.get_serializer_context()
        )
        return Response(serializer.data)

    @action(permission_classes=((IsAuthenticated,)), detail=False)
    def download_shopping_cart(self, request):
        page_objects = (
            IngredientInRecipe.objects.filter(
                recipe__in=request.user.shopping_cart_recipes.all()
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(Sum("amount"))
            .order_by("ingredient__name")
        )

        data = {
            "page_objects": page_objects,
            "user": request.user,
            "created": datetime.now(),
        }

        template = get_template("shopping_cart.html")
        html = template.render(data)
        pdf = pdfkit.from_string(html, False, options={"encoding": "UTF-8"})

        filename = "shopping_cart.pdf"
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class FavoriteRecipeViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    serializer_class = RecipeMinifiedSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        return get_object_or_404(Recipe, id=self.kwargs.get("id"))

    def create(self, request, *args, **kwargs):
        recipe = self.get_object()
        if recipe.favorites.filter(id=request.user.id).exists():
            data = {"errors": "Рецепт уже есть в избранном."}
            return Response(data, status.HTTP_400_BAD_REQUEST)
        recipe.favorites.add(request.user)
        recipe.save()
        serializer = self.serializer_class(
            instance=self.get_object(), context=self.get_serializer_context()
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()
        favorite_user = recipe.favorites.filter(id=request.user.id)
        if not favorite_user:
            data = {"errors": "Рецепта нет в избранном."}
            return Response(data, status.HTTP_400_BAD_REQUEST)
        FavoriteRecipe.objects.get(
            recipe_id=recipe.id, user_id=request.user.id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartRecipeViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    serializer_class = RecipeMinifiedSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        return get_object_or_404(Recipe, id=self.kwargs.get("id"))

    def create(self, request, *args, **kwargs):
        recipe = self.get_object()
        if recipe.shopping_carts.filter(id=request.user.id).exists():
            data = {"errors": "Рецепт уже есть в корзине."}
            return Response(data, status.HTTP_400_BAD_REQUEST)
        recipe.shopping_carts.add(request.user)
        recipe.save()
        serializer = self.serializer_class(
            instance=self.get_object(), context=self.get_serializer_context()
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()
        shopping_cart_user = recipe.shopping_carts.filter(id=request.user.id)
        if not shopping_cart_user:
            data = {"errors": "Рецепта нет в корзине."}
            return Response(data, status.HTTP_400_BAD_REQUEST)
        ShoppingCartRecipe.objects.get(
            recipe_id=recipe.id, user_id=request.user.id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
