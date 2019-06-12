import pytest
from rest_framework import status
from ..models import Ingredient


pytestmark = pytest.mark.django_db


@pytestmark
class TestIngredientListTestCase:
    """
    Tests /ingredients list operations.
    """
    def test_get_ingredient_list(self, make_ingredients_batch, ingredient_list_url, view_client):
        make_ingredients_batch(3)
        response = view_client.get(ingredient_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results')) == 3

    def test_post_with_no_data_fails(self, ingredient_list_url, view_client):
        response = view_client.post(ingredient_list_url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_valid_data_succeeds(self, ingredient_list_url, view_client):
        ingredient_data = {'food': 'a', 'kcal': 5}
        response = view_client.post(ingredient_list_url, ingredient_data)
        assert response.status_code == status.HTTP_201_CREATED

        ingredient = Ingredient.objects.get(pk=response.data.get('id'))
        assert ingredient.food == ingredient_data.get('food')


@pytestmark
class TestIngredientDetailTestCase:
    """
    Tests /ingredients detail operations.
    """

    def test_get_ingredient(self, ingredient_detail_url, view_client, make_ingredient):
        ingredient = make_ingredient
        response = view_client.get(ingredient_detail_url(args=[ingredient.pk]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('food') == ingredient.food
        assert response.data.get('kcal') == float(ingredient.kcal)
        assert response.data.get('measure') == ingredient.measure

    def test_delete_ingredient(self, ingredient_detail_url, view_client, make_ingredient):
        ingredient = make_ingredient
        response = view_client.delete(ingredient_detail_url(args=[ingredient.pk]))

        assert response.status_code == status.HTTP_204_NO_CONTENT

        ingredients = Ingredient.objects.all()
        assert len(ingredients) == 0

    def test_put_ingredient(self, ingredient_detail_url, view_client, make_ingredient):
        ingredient = make_ingredient
        payload = {'food': 'testuser7', 'kcal': 11, 'measure': 'CUP'}
        response = view_client.put(ingredient_detail_url(args=[ingredient.pk]), payload,
                                   content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('food') == payload.get('food')
        assert response.data.get('kcal') == payload.get('kcal')
        assert response.data.get('measure') == payload.get('measure')

    def test_patch_ingredient(self, ingredient_detail_url, view_client, make_ingredient):
        ingredient = make_ingredient
        payload = {'food': 'fries', 'kcal': 11}
        response = view_client.patch(ingredient_detail_url(args=[ingredient.pk]), payload,
                                     content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('kcal') == payload.get('kcal')
        assert response.data.get('food') == payload.get('food')
