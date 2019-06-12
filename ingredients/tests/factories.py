import random

import factory


class IngredientFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'ingredients.Ingredient'

    food = factory.Sequence(lambda n: f'testname{n}')
    kcal = round(random.uniform(1, 1000), 2)
