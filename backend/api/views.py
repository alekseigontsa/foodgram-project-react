from django_filters import rest_framework as dfilters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ingredients.models import Ingredient
from recipes.models import Cart, Favorite, Recipe, Tag

from .filters import IngredientFilter, RecipeFilter
from .paginations import AvailablePagination
from .permissions import IsAuthorAdminOrReadOnly
from .serializers import (IngredientSerializer, ReciepeReadSerializer,
                          RecipeWriteSerializer, TagSerializer)
from .utils import download_cart, post_or_delete_recipe


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Отправляет информацию о тегах.
     Доступно всем пользователям."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Отправляет информацию о ингредиентах.
     Доступно всем пользователям."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Отправляет информацию о рецептах.
     Создавать рецепты может только авторизованный."""

    queryset = Recipe.objects.all()
    pagination_class = AvailablePagination
    filter_backends = (dfilters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeWriteSerializer
        return ReciepeReadSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update',):
            return (IsAuthorAdminOrReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        url_path='favorite',
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthorAdminOrReadOnly,))
    def favorite(self, request, pk):
        return post_or_delete_recipe(self, request, pk, model=Favorite)

    @action(
        detail=True,
        url_path='shopping_cart',
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthorAdminOrReadOnly,))
    def shopping_cart(self, request, pk):
        return post_or_delete_recipe(self, request, pk, model=Cart)

    @action(
        detail=False,
        url_path='download_shopping_cart',
        methods=['GET'],
        permission_classes=(IsAuthorAdminOrReadOnly,))
    def download_shopping_cart(self, request):
        """Скачать список покупок."""
        user = self.request.user
        if user.user_cart.exists():
            return download_cart(self, request, user)
        return Response({'errors': 'Список покупок пуст!'},
                        status=status.HTTP_404_NOT_FOUND)
