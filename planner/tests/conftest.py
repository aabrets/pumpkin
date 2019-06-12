import pytest
from functools import partial

from django.urls import reverse

from meals.tests.factories import MealFactory
from .factories import DayPlanFactory


@pytest.fixture()
def make_dayplan():
    meal1 = MealFactory()
    meal2 = MealFactory()
    dayplan = DayPlanFactory(meals=(meal1.pk, meal2.pk))
    return dayplan


@pytest.fixture()
def make_meals_batch():
    return partial(MealFactory.create_batch)


@pytest.fixture()
def make_dayplans_batch():
    return partial(DayPlanFactory.create_batch)


@pytest.fixture(scope='session')
def dayplan_list_url():
    return reverse('dayplan-list')


@pytest.fixture(scope='session')
def dayplan_detail_url():
    return partial(reverse, viewname='dayplan-detail')
