import json

import pytest
from django.forms.models import model_to_dict
from rest_framework import status

from pumpkin.users.test.factories import UserFactory
from recipes.tests.factories import RecipeFactory
from ..models import Meal
from .factories import MealFactory

pytestmark = pytest.mark.django_db


@pytestmark
class TestMealListTestCase:
    """
    Tests /meals list operations.
    """

    def test_get_meal_list(self, make_meals_batch, meal_list_url, view_client):
        make_meals_batch(3)
        response = view_client.get(meal_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results')) == 3

    def test_post_with_no_data_fails(self, meal_list_url, view_client):
        response = view_client.post(meal_list_url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_valid_data_succeeds(self, meal_list_url, view_client):
        user = UserFactory()
        meal_data = model_to_dict(MealFactory.build(owner=user))
        view_client.force_login(user)
        response = view_client.post(meal_list_url, meal_data)

        assert response.status_code == status.HTTP_201_CREATED

        meal = Meal.objects.get(pk=response.data.get('id'))
        assert meal.name == meal_data.get('name')


@pytestmark
class TestMealDetailTestCase:
    """
    Tests /meals detail operations.
    """

    def test_get_meal(self, meal_detail_url, view_client, make_meal):
        meal = make_meal
        response = view_client.get(meal_detail_url(args=[meal.pk]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == meal.name
        assert response.data.get('detail') == meal.detail
        assert response.data.get('diet_category') == 'NON-DIET'

    def test_delete_meal(self, meal_detail_url, view_client, make_meal_user):
        meal_user = make_meal_user
        meal = meal_user['meal']
        user = meal_user['user']
        view_client.force_login(user=user)
        response = view_client.delete(meal_detail_url(args=[meal.pk]))

        assert response.status_code == status.HTTP_204_NO_CONTENT

        meals = Meal.objects.all()

        assert len(meals) == 0

    def test_put_meal(self, meal_detail_url, view_client, meal_list_url):
        user = UserFactory()
        view_client.force_login(user=user)

        rec1 = RecipeFactory(owner=user)

        meal_data = {'name': 'tess123', 'detail': 'tesst', 'diet_category': 'NON-DIET', 'recipes': rec1.pk}

        response = view_client.post(meal_list_url, meal_data)
        rec2 = RecipeFactory(owner=user)
        rec3 = RecipeFactory(owner=user)

        payload = {'name': 'testuser71', 'diet_category': 'LACTOSE_FREE',
                   'detail': 'detail7', 'recipes': [rec2.pk, rec3.pk]}
        response = view_client.put(meal_detail_url(args=[response.data.get('id')]),
                                   payload, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == response.data.get('name')
        assert response.data.get('detail') == response.data.get('detail')
        assert response.data.get('diet_category') == 'VARY'
        assert len(response.data.get('recipes')) == 3

    def test_patch_meal(self, meal_detail_url, view_client, make_meal_user):
        meal_user = make_meal_user
        meal = meal_user['meal']
        user = meal_user['user']
        view_client.force_login(user=user)
        payload = {'detail': 'detail7'}
        response = view_client.patch(meal_detail_url(args=[meal.pk]), payload, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('detail') == payload.get('detail')

    def test_diet_category_with_one_recipe(self, meal_list_url, meal_detail_url, view_client):
        user = UserFactory()
        view_client.force_login(user=user)

        rec1 = RecipeFactory(owner=user)

        meal_data = {'name': 'tess', 'detail': 'tesst', 'diet_category': 'NON-DIET', 'recipes': rec1.pk}

        response = view_client.post(meal_list_url, meal_data)

        response = view_client.get(meal_detail_url(args=[response.data.get('id')]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('diet_category') == 'RAW'
        assert len(response.data.get('recipes')) == 1
        assert response.data.get('name') == meal_data['name']
        assert response.data.get('detail') == meal_data['detail']

    def test_diet_category_with_multiple_recipes(self, meal_list_url, meal_detail_url, view_client):
        user = UserFactory()
        view_client.force_login(user=user)

        rec1 = RecipeFactory(owner=user)
        rec2 = RecipeFactory(owner=user)

        meal_data = {'name': 'tess', 'detail': 'tesst', 'diet_category': 'NON-DIET', 'recipes': [rec1.pk, rec2.pk]}

        response = view_client.post(meal_list_url, meal_data)

        response = view_client.get(meal_detail_url(args=[response.data.get('id')]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('diet_category') == 'VARY'
        assert len(response.data.get('recipes')) == 2

    def test_diet_category_filter(self, meal_diet_filter_url, meal_list_url, view_client):
        user = UserFactory()

        view_client.force_login(user)

        choices = ['VEGAN', 'RAW', 'LACTOSE_FREE']

        for i in range(2):
            meal_data = {'name': 'tess' + str(i), 'diet_category': choices[i], 'detail': 'tesst' + str(i)}
            response = view_client.post(meal_list_url, meal_data)
            assert response.status_code == status.HTTP_201_CREATED

        response = view_client.get(meal_diet_filter_url, {'diet_category': 'VEGAN'})

        assert response.status_code == status.HTTP_200_OK
        response_data = json.loads(json.dumps(response.data))
        assert response_data.get('results')[0].get('diet_category') == 'VEGAN'
