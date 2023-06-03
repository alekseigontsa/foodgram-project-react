from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient

User = get_user_model()


class Tag(models.Model):
    """Класс тегов."""

    name = models.CharField('Hазвание', max_length=75)
    color = ColorField('Цвет', format="hex", null=True)
    slug = models.SlugField('slug', unique=True, null=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name[:8]


class Recipe(models.Model):
    """Модель рецептов."""

    name = models.CharField('Hазвание', max_length=200)
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='author_recipe',
    )
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)
    tags = models.ManyToManyField(Tag,
                                  verbose_name='тег',
                                  through='TagRecipe',
                                  related_name='tag_recipes')
    image = models.ImageField('Изображение', upload_to='recipes/',)
    text = models.TextField('Текстовое описание')
    cooking_time = models.SmallIntegerField('Время приготовления',
                                            validators=[
                                                MinValueValidator(1),
                                                ]
                                            )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='ингридиент',
        through='RecipeIngredientAmount',
        related_name='ingredients')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name[:15]


class TagRecipe(models.Model):
    """Вспомогательный класс, связывающий теги и рецепты."""

    tag = models.ForeignKey(
        Tag,
        verbose_name='Тег',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        on_delete=models.CASCADE,
        related_name='recipes_tags',
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'


class RecipeIngredientAmount(models.Model):
    """Модель списка ингредиентов в рецепте."""

    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='ingredients_in_recipe',
                                   verbose_name='Ингредиент',)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipes_with_ingredients',
                               verbose_name='Рецепт',)
    amount = models.IntegerField(validators=
                                 [MinValueValidator(
                                     1, message=('Убедитесь, что это'
                                     ' значение больше либо равно 1.')),])

    class Meta:
        verbose_name = 'Количество ингридиента в рецепте'
        verbose_name_plural = 'Количество ингридиентов в рецепте'
        constraints = [models.UniqueConstraint(fields=('ingredient', 'recipe'),
                                               name='unique_ingredient'),]


class Favorite(models.Model):
    """Создает модель избранных рецептов пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Избранное',
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_favorite'
            ),
        )

    def __str__(self):
        return f'{self.user.username}'


class Cart(models.Model):
    """Создает модель покупок рецептов пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Покупки',
    )

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        constraints = [models.UniqueConstraint(fields=('user', 'recipe'),
                                               name='unique_cart'),]

    def __str__(self):
        return f'{self.user.username}'


class Subscribe(models.Model):
    """Создает модель подписок к автору."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписка',
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [models.UniqueConstraint(fields=('user', 'author'),
                                               name='unique_follow'),
                       models.CheckConstraint(
            check=~models.Q(user=models.F('author')),
            name='user_author_diferent'), ]

    def __str__(self):
        return f'{self.user.username}'
