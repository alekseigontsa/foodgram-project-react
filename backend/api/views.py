from django.shortcuts import get_object_or_404
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from ingredients.models import Ingredient
from recipes.models import Tag, Recipe, Favorite, Subscribe
from .mixins import CreateDestroyViewSet
from users.models import User
from .serializers import (DjoserUserSerializer, TagSerializer,
                          ReciepeReadSerializer, ReciepeCreateSerializer,
                          IngredientSerializer,
                          FavoriteSerializer,
)

from djoser.views import UserViewSet


# class CustomUserViewSet(UserViewSet):
#     """Позволяет просматривать собственные данные пользователя и изменять их.
#      Позволяет администратору создавать пользователей
#       и изменять их информацию."""
    
    # @action(
    #     detail=False,
    #     url_path='me',
    #     methods=['GET'],
    #     permission_classes=(permissions.IsAuthenticated,))
    # def me(self, request):
    #     serializer = self.get_serializer(request.user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    # @action(
    #     detail=False,
    #     url_path='set_password',
    #     methods=['POST'],
    #     permission_classes=(permissions.IsAuthenticated,))
    # def set_password(self, request):
    #     serializer = self.get_serializer(request.user)
    #     if request.method == 'POST':
    #         serializer = self.get_serializer(
    #             request.user,
    #             data=request.data,
    #             partial=True)
    #         if serializer.is_valid(raise_exception=True):
    #             return Response(serializer.data,
    #                             status=status.HTTP_200_OK)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Отправляет информацию о тегах.
     Доступно всем пользователям."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Отправляет информацию о ингредиентах.
     Доступно всем пользователям."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Отправляет информацию о рецептах.
     Создавать рецепты может только авторизованный."""

    queryset = Recipe.objects.all()
    serializer_class = ReciepeCreateSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    # filterset_class = TitleFilter

    # def get_serializer(self):
    #     if self.request.method in SAFE_METHODS:
    #         return ReciepeReadSerializer
    #     return ReciepeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(CreateDestroyViewSet):
    """Добавляет рецепты в избранное"""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    # def get_queryset(self):
    #     recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
    #     return recipe

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, favorite=recipe)

    def destroy (self, serializer):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, favorite=recipe)
