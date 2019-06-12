from django.db import transaction
from rest_framework import serializers

from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer
from pumpkin.utils import PrimaryKeyRelatedFieldQueryset
from .models import Recipe, RecipeIngredient


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = PrimaryKeyRelatedFieldQueryset(many=True, queryset=Ingredient.objects)
    total_ingredients = serializers.IntegerField(required=False)
    total_kcals = serializers.FloatField(required=False)
    total_weight = serializers.FloatField(required=False)
    diet_category = serializers.ChoiceField(required=False, choices=Recipe.CATEGORIES)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    private = serializers.BooleanField(default=False)
    amounts = serializers.ListField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'ingredients', 'recipe', 'total_ingredients',
                  'total_kcals', 'total_weight', 'diet_category', 'owner', 'private', 'amounts')
        depth = 1

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        amount = validated_data.pop('amounts', None)
        recipe = super(RecipeSerializer, self).create(validated_data)
        if ingredients:
            for i in range(len(ingredients)):
                if amount:
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredients[i], amount=amount[i])
        return recipe

    @transaction.atomic
    def update(self, recipe, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        amount = validated_data.pop('amounts', None)
        existing_ingredients_ids = [ingredient.pk for ingredient in list(recipe.ingredients.all())]
        if ingredients:
            for i in range(len(ingredients)):
                if ingredients[i].pk in existing_ingredients_ids:
                    continue
                if amount:
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredients[i], amount=amount[i])
                else:
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredients[i])
        recipe.name = validated_data.pop('name', recipe.name)
        recipe.recipe = validated_data.pop('recipe', recipe.recipe)
        recipe.diet_category = validated_data.pop('diet_category', recipe.diet_category)
        recipe.private = validated_data.pop('private', recipe.private)
        recipe.save()
        return recipe


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer()
    ingredient = IngredientSerializer()
    amount = serializers.FloatField(required=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'recipe', 'ingredient', 'amount')
        depth = 1

    @transaction.atomic
    def create(self, validated_data):
        return super(RecipeIngredientSerializer, self).create(validated_data)
