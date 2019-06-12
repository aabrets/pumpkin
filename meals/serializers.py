from django.db import transaction
from rest_framework import serializers

from pumpkin.utils import PrimaryKeyRelatedFieldQueryset
from recipes.models import Recipe
from .models import Meal


class MealSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    meal_time = serializers.SerializerMethodField()
    recipes = PrimaryKeyRelatedFieldQueryset(many=True, queryset=Recipe.objects)
    diet_category = serializers.CharField(max_length=30)

    def get_meal_time(self, meal_instance):
        choice = meal_instance.mealchoice_set.all().first()
        if choice:
            return choice.meal_choice
        else:
            return None

    class Meta:
        model = Meal
        fields = ['id', 'name', 'detail', 'owner', 'meal_time', 'recipes', 'diet_category']

    @transaction.atomic
    def create(self, validated_data):
        recipes = validated_data.pop('recipes', None)
        meal = super(MealSerializer, self).create(validated_data)
        if recipes:
            for recipe in recipes:
                meal.recipes.add(recipe)
        diet_category = meal.diet_category
        if len(meal.recipes.all()) == 1:
            diet_category = recipes[0].diet_category
        elif len(meal.recipes.all()) > 1:
            diet_category = "VARY"
        meal.diet_category = diet_category
        meal.save()
        return meal

    @transaction.atomic
    def update(self, meal_instance, validated_data):
        recipes = validated_data.pop('recipes', None)
        existing_recipes_ids = [recipe.pk for recipe in list(meal_instance.recipes.all())]
        if recipes:
            for recipe in recipes:
                if recipe.pk in existing_recipes_ids:
                    continue
                meal_instance.recipes.add(recipe)
        diet_category = meal_instance.diet_category
        if len(meal_instance.recipes.all()) == 1:
            diet_category = recipes[0].diet_category
        elif len(meal_instance.recipes.all()) > 1:
            diet_category = "VARY"
        meal_instance.diet_category = diet_category
        meal_instance.meal_time = validated_data.pop('meal_time', None)
        meal_instance.save()
        return meal_instance
