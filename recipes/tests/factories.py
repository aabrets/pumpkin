import random

import factory

from ingredients.tests.factories import IngredientFactory

recipe_name = factory.Sequence(lambda n: f'testuser{n}')


class RecipeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'recipes.Recipe'

    name = recipe_name
    recipe = factory.Sequence(lambda n: f'recipe{n}')


class RecipeIngredientFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'recipes.RecipeIngredient'

    recipe = factory.SubFactory(RecipeFactory)
    ingredient = factory.SubFactory(IngredientFactory)
    amount = round(random.uniform(1, 10), 2)
