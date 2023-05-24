from django_filters.rest_framework import CharFilter, FilterSet, filters

from ingredients.models import Ingredient
from recipes.models import Recipe, Tag
from users.models import User


class RecipeFilter(FilterSet):
    """ Фильтр для рецептов по тегу.
     Фильтр по избранным рецептам и добавленных в покупки. """

    author = filters.ModelChoiceFilter(
        queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_is_in_shopping_cart')
    is_favorited = filters.NumberFilter(
        method='filter_is_favorited')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorite__user=self.request.user.pk)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(cart__user=self.request.user.pk)
        return queryset


class IngredientFilter(FilterSet):
    """ Фильтр для вывода ингредиентов по названию. """
    name = CharFilter(field_name='name',
                      lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')
