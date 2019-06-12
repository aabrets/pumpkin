from django.db import models

from meals.models import Meal


class DayPlan(models.Model):

    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey('users.User', on_delete='PROTECT')
    meals = models.ManyToManyField(Meal, through='MealChoice', related_name='dayplans')

    class Meta:
        unique_together = (('user', 'date'),)
        ordering = ['date']


class MealChoice(models.Model):
    MEAL_CHOICES = (
        ('BREAKFAST', 'Breakfast'),
        ('LUNCH', 'Lunch'),
        ('DINNER', 'Dinner'),
    )
    day_plan = models.ForeignKey(DayPlan, on_delete='PROTECT')
    meal = models.ForeignKey(Meal, on_delete='PROTECT')
    meal_choice = models.CharField(choices=MEAL_CHOICES, default='BREAKFAST', max_length=30)
