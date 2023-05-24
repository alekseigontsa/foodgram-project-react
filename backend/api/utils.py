from datetime import date

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe, RecipeIngredientAmount

from .serializers import RecipeReadMiniSerializer


def post_or_delete_recipe(self, request, pk, model):
    user = self.request.user
    recipe = get_object_or_404(Recipe, id=pk)
    if request.method == 'POST':
        if model.objects.filter(user=user,
                                recipe=recipe).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeReadMiniSerializer(recipe)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    if not model.objects.filter(user=user,
                                recipe=recipe).exists():
        return Response({'errors': 'Рецепт не найден!'},
                        status=status.HTTP_404_NOT_FOUND)
    model.objects.get(user=user,
                      recipe=recipe).delete()
    return Response('Рецепт удален из списка',
                    status=status.HTTP_204_NO_CONTENT)

def download_cart(self, request, user):
    """Скачивание списка продуктов для выбранных рецептов пользователя."""
    sum_ingredients_in_recipes = RecipeIngredientAmount.objects.filter(
        recipe__cart__user=user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(
        amounts=Sum('amount')).order_by('amounts')
    today = date.today().strftime("%d-%m-%Y")
    shopping_list = f'Список покупок на: {today}\n\n'
    for ingredient in sum_ingredients_in_recipes:
        shopping_list += (
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["amounts"]} '
            f'{ingredient["ingredient__measurement_unit"]}\n'
        )
    shopping_list += '\n\nFoodgram 05.2023 by @alekseigontsa'
    filename = 'shopping_list.txt'
    response = HttpResponse(shopping_list, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
