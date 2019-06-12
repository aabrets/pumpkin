import pytest
from django.urls import reverse
from functools import partial

from pumpkin.users.test.factories import UserFactory
from .factories import MealFactory


@pytest.fixture()
def make_meal():
    user = UserFactory()

    return MealFactory(owner=user)


@pytest.fixture()
def make_meal_user():
    user = UserFactory()
    return {'meal': MealFactory(owner=user), 'user': user}


@pytest.fixture()
def make_meals_batch():
    return partial(MealFactory.create_batch)


@pytest.fixture(scope='session')
def meal_list_url():
    return reverse('meal-list')


@pytest.fixture(scope='session')
def meal_detail_url():
    return partial(reverse, viewname='meal-detail')


@pytest.fixture(scope='session')
def meal_diet_filter_url():
    return reverse('meal_diet-list')
