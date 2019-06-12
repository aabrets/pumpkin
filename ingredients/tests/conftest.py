import pytest
from django.urls import reverse
from functools import partial
from .factories import IngredientFactory


@pytest.fixture()
def make_ingredient():
    return IngredientFactory()


@pytest.fixture(scope='session')
def make_ingredients_batch():
    return partial(IngredientFactory.create_batch)


@pytest.fixture(scope='session')
def ingredient_list_url():
    return reverse('ingredient-list')


@pytest.fixture(scope='session')
def ingredient_detail_url():
    return partial(reverse, viewname='ingredient-detail')
