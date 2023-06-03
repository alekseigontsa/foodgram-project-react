from datetime import date

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
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
    filename = f'shopping_list_{today}.pdf'
    pdfmetrics.registerFont(
        TTFont('TNR', 'times.ttf', 'UTF-8'))
    font = 'TNR'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    pdf_file = canvas.Canvas(response)
    pdf_file.setFont(font, 10)
    pdf_file.drawString(
        230,
        810,
        'FOODGRAM'
    )
    pdf_file.setFont(font, 14)
    pdf_file.drawString(
        200,
        740,
        f'Список покупок на: {today}')
    from_bottom = 720
    pdf_file.setFont(font, 11)
    for number, ingredient in enumerate(sum_ingredients_in_recipes, start=1):
        pdf_file.drawString(
            60,
            from_bottom,
            (f'{number}.  {ingredient["ingredient__name"]} - '
             f'{ingredient["amounts"]} '
             f'{ingredient["ingredient__measurement_unit"]}')
        )
        from_bottom -= 20
        if from_bottom <= 50:
            from_bottom = 700
            pdf_file.showPage()
            pdf_file.setFont(font, 10)
            pdf_file.drawString(
                230,
                810,
                'FOODGRAM')
            pdf_file.setFont(font, 11)
    pdf_file.setFont(font, 6)
    pdf_file.drawString(
        50,
        from_bottom - 20,
        'Foodgram 05.2023 by @alekseigontsa')
    pdf_file.showPage()
    pdf_file.save()
    return response
