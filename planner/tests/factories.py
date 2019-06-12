import factory

from meals.tests.factories import MealFactory
from pumpkin.users.test.factories import UserFactory


class DayPlanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'planner.DayPlan'
    user = factory.SubFactory(UserFactory)
    date = factory.Faker('date')


class MealChoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'planner.MealChoice'

    day_plan = factory.SubFactory(DayPlanFactory)
    meal = factory.SubFactory(MealFactory)
