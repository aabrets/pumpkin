import pytest
from django.utils.datetime_safe import datetime
from rest_framework import status

from pumpkin.users.test.factories import UserFactory
from ..models import DayPlan
from .factories import DayPlanFactory, MealChoiceFactory

pytestmark = pytest.mark.django_db


@pytestmark
class TestDayPlanListTestCase:
    """
    Tests /dayplans list operations.
    """
    def test_get_dayplan_all(self, dayplan_list_url, view_client, make_meals_batch):
        user = UserFactory()
        view_client.force_login(user)
        meals = make_meals_batch(3)
        dayplan = DayPlanFactory(user=user)
        for i in range(3):
            MealChoiceFactory(day_plan=dayplan, meal=meals[i])

        response = view_client.get(dayplan_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results')) == 1

    def test_post_with_no_data_fails(self, dayplan_list_url, view_client):
        response = view_client.post(dayplan_list_url, {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_valid_data_succeeds(self, dayplan_list_url, view_client, make_meals_batch):
        user = UserFactory()
        view_client.force_login(user)
        meals_objects = make_meals_batch(3)
        meals = [meal.pk for meal in meals_objects]

        dayplan_data = {'user': user.pk, 'meals': meals}

        response = view_client.post(dayplan_list_url, dayplan_data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        dayplan = DayPlan.objects.get(pk=response.data.get('id'))
        assert len(response.data.get('meals')) == len(dayplan.meals.all())
        assert str(dayplan.user.id) == dayplan_data.get('user')


@pytestmark
class TestDayPlanDetailTestCase:
    """
    Tests /dayplans detail operations.
    """

    def test_get_dayplan(self, dayplan_detail_url, view_client, make_meals_batch):
        user = UserFactory()
        view_client.force_login(user)
        meals = make_meals_batch(3)
        dayplan = DayPlanFactory(user=user)
        for i in range(3):
            MealChoiceFactory(day_plan=dayplan, meal=meals[i])

        response = view_client.get(dayplan_detail_url(args=[dayplan.pk]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('id') == dayplan.pk

    def test_delete_dayplan(self, dayplan_detail_url, view_client):
        user = UserFactory()
        view_client.force_login(user)
        dayplan = DayPlanFactory(user=user)
        response = view_client.delete(dayplan_detail_url(args=[dayplan.pk]))

        assert response.status_code == status.HTTP_204_NO_CONTENT

        dayplans = DayPlan.objects.all()
        assert len(dayplans) == 0

    def test_put_dayplan(self, dayplan_detail_url, view_client, make_meals_batch):
        user = UserFactory()
        view_client.force_login(user)
        meals = make_meals_batch(3)
        dayplan = DayPlanFactory(user=user)
        choices = ['BREAKFAST', 'LUNCH', 'DINNER']

        for i in range(3):
            MealChoiceFactory(day_plan=dayplan, meal=meals[i], meal_choice=choices[i])

        date = datetime.now()
        meals = make_meals_batch(3)
        payload = {'date': date, 'user': user.id, 'meals': [meal.pk for meal in meals]}
        response = view_client.put(dayplan_detail_url(args=[dayplan.pk]), payload, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK

    def test_patch_dayplan(self, dayplan_detail_url, view_client, make_meals_batch):
        user = UserFactory()
        view_client.force_login(user)
        meals = make_meals_batch(3)
        dayplan = DayPlanFactory(user=user)
        for i in range(3):
            MealChoiceFactory(day_plan=dayplan, meal=meals[i])
        date = datetime.now()
        payload = {'date': date}

        response = view_client.patch(dayplan_detail_url(args=[dayplan.pk]), payload, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
