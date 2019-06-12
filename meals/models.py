from django.db import models

from pumpkin.users.models import User


class Meal(models.Model):

    name = models.CharField(max_length=100, unique=True)
    detail = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='meals', default=None)
    recipes = models.ManyToManyField('recipes.Recipe', related_name='meals')
    diet_category = models.CharField(max_length=30, default='NON-DIET')

    def __str__(self):
        return '%s %s, owner=%s, diet=%s' % (self.name, self.name, self.owner, self.diet_category)
