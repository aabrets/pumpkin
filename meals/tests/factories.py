import factory

from pumpkin.users.test.factories import UserFactory


class MealFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'meals.Meal'
        django_get_or_create = ['name']

    name = factory.Sequence(lambda an: f'testuser{an}')
    detail = factory.Sequence(lambda an: f'detail{an}')
    owner = factory.SubFactory(UserFactory)
