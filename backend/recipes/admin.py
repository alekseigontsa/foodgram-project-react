from django.contrib import admin

from backend.settings import EMPTY_VALUE_DISPLAY

from .models import (Cart, Favorite, Recipe, RecipeIngredientAmount, Subscribe,
                     Tag, TagRecipe)

admin.site.register(RecipeIngredientAmount)
admin.site.register(Tag)
admin.site.register(Cart)
admin.site.register(Subscribe)
admin.site.register(TagRecipe)
admin.site.register(Favorite)


class RecipeIngredientAmountAdmin(admin.TabularInline):
    model = RecipeIngredientAmount


class TagRecipeadmin(admin.TabularInline):
    model = TagRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Создает атрибуты для работы с рецептами в панели администратора"""
    list_display = ('pk', 'name', 'author', 'favorite')
    inlines = (RecipeIngredientAmountAdmin, TagRecipeadmin,)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY

    def favorite(self, obj):
        return Favorite.objects.filter(recipe=obj.id).count()
