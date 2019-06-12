from django.contrib.postgres.fields import ArrayField
from django.db import models

from ingredients.models import Ingredient
from pumpkin.users.models import User


class RecipeManager(models.Manager):

    def public_recipes(self, *args, **kwargs):
        return super(RecipeManager, self).filter(private=False)

    def private_recipes(self, *args, **kwargs):
        user = kwargs.pop('owner')
        return super(RecipeManager, self).filter(private=True, owner=user)


class Recipe(models.Model):
    CATEGORIES = (
        ('LACTOSE_FREE', 'Lactose Free'),
        ('GLUTEN_FREE', 'Gluten Free'),
        ('DAIRY_FREE', 'Dairy Free'),
        ('VEGETARIAN', 'Vegetarian'),
        ('VEGAN', 'Vegan'),
        ('RAW', 'Raw'),
    )

    name = models.CharField(max_length=100)
    recipe = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient", related_name='recipes')
    diet_category = models.CharField(choices=CATEGORIES, default='RAW', max_length=30)
    private = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='recipes', default=None)
    amounts = ArrayField(ArrayField(models.IntegerField(default=100)), default=None, null=True, blank=True)

    objects = RecipeManager()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT, unique=False)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    amount = models.FloatField(blank=False)
