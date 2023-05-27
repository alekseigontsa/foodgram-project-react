import base64
import re

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredientAmount, Subscribe, Tag)
from users.models import User

REGEXP = r'^[\w.@+-]+\Z'


def valid_username(value):
    if not re.fullmatch(REGEXP, value):
        raise serializers.ValidationError('Недопустимое имя!')
    return value


class DjoserUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed',
                  )

    def get_is_subscribed(self, obj):

        return Subscribe.objects.filter(user=self.context['request'].user.id,
                                        author=obj).exists()

    def validate_username(self, value):
        return valid_username(value)


class DjoserUserCreateSerializer(UserCreateSerializer):
    """ Сериализатор для вывода пользователей. """
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'password')

    def validate_username(self, value):
        return valid_username(value)


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор для вывода тегов. """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор для вывода ингредиентов. """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientAmountSerializer(serializers.ModelSerializer):
    """ Сериализатор для вывода ингредиентов через
     промежуточную таблицу при запросе get. """
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name',)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = RecipeIngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ReciIngrediWriteSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания и обновления рецептов. """
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.IntegerField(write_only=True, min_value=1)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredients',
        queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredientAmount
        fields = ('id', 'amount', 'recipe')


class Base64ImageField(serializers.ImageField):
    """ Сериализатор для вывода картинок. """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeWriteSerializer(serializers.ModelSerializer):
    """ Сериализатор для добавления и изменения рецептов. """
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    ingredients = ReciIngrediWriteSerializer(many=True)
    image = Base64ImageField(max_length=None, use_url=True)
    author = DjoserUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time', 'author')
        read_only_fields = ('id', 'author', 'tags')

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_list) != len(set(ingredients_list)):
            raise serializers.ValidationError(
                'Проверьте, какой-то ингредиент был выбран более 1 раза'
            )
        return data

    def create(self, validated_data):
        """ Создаёт вложенные сериализаторы tag и ingredient. """
        current_user = self.context['request'].user
        if not current_user.pk:
            raise serializers.ValidationError('Пользователя не существует.')
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        ing_bulk_data = (
            RecipeIngredientAmount(ingredient=ing['ingredients'],
                                   recipe=recipe,
                                   amount=ing['amount'])
            for ing in ingredients_data)
        RecipeIngredientAmount.objects.bulk_create(ing_bulk_data)
        return recipe

    def update(self, instance, validated_data):
        """ Переписывает целиком вложенные сериализаторы tag и ingredient. """
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        current_ings = RecipeIngredientAmount.objects.filter(
            recipe=instance.id)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            lst = []
            for tag in tags_data:
                current_tag = Tag.objects.get(pk=tag.id)
                lst.append(current_tag)
        instance.tags.set(lst)
        current_ings.delete()
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            ing_bulk_data = (
                RecipeIngredientAmount(
                    ingredient=ing['ingredients'],
                    recipe=instance,
                    amount=ing['amount'])
                for ing in ingredients_data)
            RecipeIngredientAmount.objects.bulk_create(ing_bulk_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        self.fields.pop('ingredients')
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(
            instance.tags.all(), many=True).data
        representation['ingredients'] = RecipeIngredientAmountSerializer(
            instance.recipes_with_ingredients.all(), many=True).data
        return representation


class ReciepeReadSerializer(serializers.ModelSerializer):
    """ Сериализатор для вывода рецептов. """
    tags = TagSerializer(many=True)
    author = DjoserUserSerializer(required=False, read_only=True)
    ingredients = RecipeIngredientAmountSerializer(
        source='recipes_with_ingredients',
        many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags',
                  'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ingredients'] = RecipeIngredientAmountSerializer(
            instance.recipes_with_ingredients.all(), many=True).data
        return representation

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(user=self.context['request'].user.id,
                                       recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        return Cart.objects.filter(user=self.context['request'].user.id,
                                   recipe=obj).exists()


class RecipeReadMiniSerializer(serializers.ModelSerializer):
    """ Сериализатор миниформата рецепта (для Favorite и Cart). """

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    """ Сериализатор для вывода страницы подписок. """
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(
        source='author.author_recipe.count')

    class Meta:
        model = Subscribe
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """ Возвращает True, если есть подписка. """
        return Subscribe.objects.filter(
            user=obj.user, author=obj.author).exists()

    def get_recipes(self, obj):
        """ Выводит заданное число рецептов автора в его карточке. """
        request = self.context['request']
        rec_limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(
            author=obj.author).order_by('-pub_date')
        if rec_limit:
            queryset = queryset[:int(rec_limit)]
        return RecipeReadMiniSerializer(queryset, many=True).data
