from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, TagViewSet, RecipeViewSet, IngredientViewSet, FavoriteViewSet


router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                FavoriteViewSet, basename='favorite')


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
