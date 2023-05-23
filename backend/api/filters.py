# from django_filters import rest_framework as dfilters
# from rest_framework import filters
from django_filters.rest_framework import FilterSet, filters, CharFilter
from rest_framework.filters import SearchFilter

from ingredients.models import Ingredient
from recipes.models import Tag, Recipe
from users.models import User


# class RecipeFilter(dfilters.FilterSet):
#     """ Фильтр для вывода рецептов по query parameters. """
#     tags = dfilters.ModelMultipleChoiceFilter(
#         field_name='tags__slug', to_field_name='slug',
#         queryset=Tag.objects.all(),)
#     author = dfilters.ModelChoiceFilter(queryset=User.objects.all())
#     is_favorited = dfilters.BooleanFilter(field_name='faved_by')
#     is_in_shopping_cart = dfilters.BooleanFilter(field_name='in_cart_for')

#     class Meta:
#         model = Recipe
#         fields = ('author', 'tags',)


class RecipeFilter(FilterSet):

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
        print(queryset.filter(favorite__author=self.request.user))
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorite__author=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(cart__author=self.request.user)
        return queryset


class IngredientFilter(FilterSet):
    """ Фильтр для вывода ингредиентов по query parameters. """
    name = CharFilter(field_name='name',
                      lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')
