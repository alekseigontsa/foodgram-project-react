import base64
import re

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        ValidationError)
from djoser.serializers import UserSerializer

from recipes.models import (Ingredient, Tag, TagRecipe,
                            Recipe, RecipeIngredientAmount,
                            Favorite, Subscribe, Cart)

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


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagRecipeSerializer(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = TagSerializer(value)
        return serializer.data


class RecipeIngredientAmountSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeAddIngredientSerializer(serializers.ModelSerializer):

    # id = serializers.IntegerField(source='ingredient.id')
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),)
    # amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredientAmount
        fields = ('id', 'amount')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class ReciepeReadSerializer(serializers.ModelSerializer):

    # tags = TagRecipeSerializer(slug_field='slug',
    #                            queryset=Tag.objects.all(),
    #                            many=True)
    tags = TagSerializer(many=True, required=False)
    author = DjoserUserSerializer(required=False)
    ingredients = RecipeIngredientAmountSerializer(
        source='recipes_ingredients',
        many=True, required=False)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags',
                  'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(user=self.context['request'].user.id,
                                       favorite=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        return Cart.objects.filter(user=self.context['request'].user.id,
                                   cart=obj).exists()


class ReciepeCreateSerializer(serializers.ModelSerializer):

    # tags = TagRecipeSerializer(slug_field='slug',
    #                            queryset=Tag.objects.all(),
    #                            many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=True)
    author = DjoserUserSerializer(required=False)
    # ingredients = serializers.PrimaryKeyRelatedField(
    #     queryset=Ingredient.objects.all())
    ingredients = RecipeAddIngredientSerializer(source='recipes_ingredients',
                                                many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags',
                  'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(
            instance.tags.all(), many=True).data
        representation['ingredients'] = RecipeIngredientAmountSerializer(
            instance.recipes_ingredients.all(), many=True).data
        return representation

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(user=self.context['request'].user.id,
                                       favorite=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        return Cart.objects.filter(user=self.context['request'].user.id,
                                   cart=obj).exists()

    def crete(self, validated_data):
        print('123')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            try:
                current_tag, status = Tag.objects.get(pk=tag)
                
                TagRecipe.objects.create(tag=current_tag, recipe=recipe)
            except:
                raise ValidationError(
                    'Нет таких тегов!')
        for ingredient in ingredients:
            try:
                current_ingredient, status = Tag.objects.get(id=ingredient.id)
                RecipeIngredientAmount.objects.create(
                    ingredient=current_ingredient,
                    recipe=recipe,
                    amount=ingredient.amount)
            except:
                raise ValidationError(
                    'Нет таких ингредиентов!')
        return recipe

    def update(self, instance, validated_data):
        print('1------------', validated_data)
        print('2------------', instance.id)
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        if 'tags' in validated_data:
            print()
            tags_data = validated_data.pop('tags')
            lst = []
            for tag in tags_data:
                current_tag = Tag.objects.get(pk=tag.id)
                lst.append(current_tag)
        instance.tags.set(lst)
        print('3/1------------', instance.tags)
        if 'recipes_ingredients' in validated_data:
            ingredients_data = validated_data.pop('recipes_ingredients')
            print('4------------', validated_data)
            lst = []
            for ingredient in ingredients_data:
                print('5------------', instance.tags)
                RecipeIngredientAmount.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient['id'],
                    amount=ingredient['amount'])
                # current_ingredient, status = Ingredient.objects.get(id=ingredient.get('id'))
                # # amount = ingredient['amount']
                # lst.append(current_ingredient)
            # instance.ingredients.set(lst)
        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    favorite = ReciepeCreateSerializer(required=False)

    class Meta:
        model = Favorite
        fields = ('favorite', 'user')
