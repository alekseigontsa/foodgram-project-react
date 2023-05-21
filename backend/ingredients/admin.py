from django.contrib import admin

from backend.settings import EMPTY_VALUE_DISPLAY

from .models import Ingredient


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    """Создает атрибуты для работы с ингредиентами в панели администратора"""
    list_display = ('pk', 'name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY
