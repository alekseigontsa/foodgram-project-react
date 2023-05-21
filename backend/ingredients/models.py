from django.db import models


class Ingredient(models.Model):
    """Модель списка ингридиентов."""

    name = models.CharField('Hазвание', max_length=256)
    measurement_unit = models.CharField('Единицы измерения', max_length=25)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name[:8]