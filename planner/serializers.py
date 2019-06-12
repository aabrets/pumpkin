from django.db import transaction
from rest_framework import serializers

from meals.models import Meal
from meals.serializers import MealSerializer
from pumpkin.utils import PrimaryKeyRelatedFieldQueryset

from .models import DayPlan, MealChoice


class DayPlanSerializer(serializers.ModelSerializer):
    meals = PrimaryKeyRelatedFieldQueryset(many=True, queryset=Meal.objects)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DayPlan
        fields = ('id', 'date', 'user', 'meals')
        depth = 1

    @transaction.atomic
    def create(self, validated_data):
        meals = validated_data.pop('meals')
        mealchoices = validated_data.pop('mealchoices', None)
        dayplan = super(DayPlanSerializer, self).create(validated_data)
        for i in range(len(meals)):
            if mealchoices:
                MealChoice.objects.create(day_plan=dayplan, meal=meals[i], meal_choice=mealchoices[i])
            else:
                MealChoice.objects.create(day_plan=dayplan, meal=meals[i])
        return dayplan

    @transaction.atomic
    def update(self, dayplan, validated_data):
        meals = validated_data.pop('meals', None)
        existing_meals_ids = [meal.pk for meal in list(dayplan.meals.all())]
        mealchoices = validated_data.pop('mealchoices', None)
        if meals:
            for i in range(len(meals)):
                if meals[i].pk in existing_meals_ids:
                    continue
                if mealchoices:
                    MealChoice.objects.create(day_plan=dayplan, meal=meals[i], meal_choice=mealchoices[i])
                else:
                    MealChoice.objects.create(day_plan=dayplan, meal=meals[i])
        dayplan.date = validated_data.pop('date', dayplan.date)
        dayplan.user = validated_data.pop('user', dayplan.user)
        dayplan.save()

        return dayplan


class MealChoiceSerializer(serializers.ModelSerializer):
    day_plan = DayPlanSerializer()
    meal = MealSerializer()
    meal_choice = serializers.ChoiceField(required=False, choices=MealChoice.MEAL_CHOICES)

    class Meta:
        model = DayPlan
        fields = ('id', 'date', 'user', 'meals')
        depth = 1

    def create(self, validated_data):
        return super(MealChoiceSerializer, self).create(validated_data)
