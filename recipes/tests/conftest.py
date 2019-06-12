import pytest
from django.urls import reverse
from functools import partial

from ingredients.tests.factories import IngredientFactory
from pumpkin.users.test.factories import UserFactory
from .factories import RecipeFactory, RecipeIngredientFactory


@pytest.fixture()
def make_recipe():
    return RecipeFactory()


@pytest.fixture()
def make_recipe_user():
    user = UserFactory()
    recipe = RecipeFactory(owner=user)
    return {'recipe': recipe, 'user': user}


@pytest.fixture()
def make_recipes_batch():
    return partial(RecipeFactory.create_batch)


@pytest.fixture()
def make_recipeingredient():
    return RecipeIngredientFactory


@pytest.fixture(scope='session')
def make_ingredients_batch():
    return partial(IngredientFactory.create_batch)


@pytest.fixture(scope='session')
def recipe_list_url():
    return reverse('recipe-list')


@pytest.fixture(scope='session')
def recipe_detail_url():
    return partial(reverse, viewname='recipe-detail')


@pytest.fixture()
def make_my_recipe_user():
    user = UserFactory()
    recipe = RecipeFactory(owner=user, private=True)
    return {'recipe': recipe, 'user': user}


@pytest.fixture()
def make_my_recipe():
    return RecipeFactory(private=True)


@pytest.fixture(scope='session')
def my_recipe_list_url():
    return reverse('my_recipe-list')


@pytest.fixture(scope='session')
def my_recipe_detail_url():
    return partial(reverse, viewname='my_recipe-detail')


@pytest.fixture(scope='session')
def ingredient_list_url():
    return reverse('ingredient-list')
