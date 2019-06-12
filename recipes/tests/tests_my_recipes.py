import pytest
from django.db.models import Sum
from django.forms.models import model_to_dict
from rest_framework import status

from pumpkin.users.test.factories import UserFactory
from ..models import Recipe
from .factories import RecipeFactory

pytestmark = pytest.mark.django_db


@pytestmark
class TestMyRecipeListTestCase:
    """
    Tests /my_recipes list operations.
    """
    def test_get_recipe_list(self, my_recipe_list_url, view_client):
        user = UserFactory()
        for i in range(3):
            RecipeFactory(owner=user, private=True)
        view_client.force_login(user=user)
        response = view_client.get(my_recipe_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results')) == 3

    def test_post_with_no_data_fails(self, my_recipe_list_url, view_client):
        response = view_client.post(my_recipe_list_url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_valid_data_succeeds(self, my_recipe_list_url, view_client):
        user = UserFactory()
        view_client.force_login(user=user)
        recipe_data = model_to_dict(RecipeFactory.build())
        recipe_data['owner'] = user
        recipe_data['diet_category'] = 'VEGAN'
        response = view_client.post(my_recipe_list_url, recipe_data)
        assert response.status_code == status.HTTP_201_CREATED

        recipe = Recipe.objects.get(pk=response.data.get('id'))
        assert recipe.name == recipe_data.get('name')
        assert recipe.diet_category == recipe_data.get('diet_category')

    def test_post_with_ingredients_recipe(self, my_recipe_list_url, view_client, make_ingredients_batch):
        user = UserFactory()
        view_client.force_login(user)
        ingredient_objects = make_ingredients_batch(6)
        amounts = [1.5, 2.3, 0.5, 0.4, 4.3, 5.2]
        ingredients = [ingredient.pk for ingredient in ingredient_objects]
        view_client.force_login(user=user)
        payload = {'private': True, 'name': 'testuser7', 'recipe': 'recipe7', 'diet_category': 'LACTOSE_FREE',
                   'ingredients': ingredients, 'amounts': amounts}

        response = view_client.post(my_recipe_list_url, payload, content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('name') == payload.get('name')
        assert response.data.get('recipe') == payload.get('recipe')
        assert len(response.data.get('ingredients')) == len(payload.get('ingredients'))


@pytestmark
class TestRecipeDetailTestCase:
    """
    Tests /my_recipes detail operations.
    """

    def test_get_recipe(self, my_recipe_detail_url, view_client, make_my_recipe_user):
        recipe_user = make_my_recipe_user
        recipe = recipe_user['recipe']
        user = recipe_user['user']
        view_client.force_login(user=user)
        response = view_client.get(my_recipe_detail_url(args=[recipe.pk]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == recipe.name
        assert response.data.get('recipe') == recipe.recipe
        assert response.data.get('diet_category') == 'RAW'

    def test_delete_recipe(self, my_recipe_detail_url, view_client, make_my_recipe_user):
        recipe_user = make_my_recipe_user
        recipe = recipe_user['recipe']
        user = recipe_user['user']
        view_client.force_login(user=user)
        response = view_client.delete(my_recipe_detail_url(args=[recipe.pk]))

        assert response.status_code == status.HTTP_204_NO_CONTENT

        recipes = Recipe.objects.all()
        assert len(recipes) == 0

    def test_put_recipe(self, my_recipe_detail_url, my_recipe_list_url, view_client,
                        make_ingredients_batch, ingredient_list_url):
        user = UserFactory()
        view_client.force_login(user)
        ingredient_objects = make_ingredients_batch(6)
        amounts = [1.5, 2.3, 0.5, 0.4, 4.3, 5.2]
        ingredients = [ingredient.pk for ingredient in ingredient_objects]
        view_client.force_login(user=user)
        post_payload = {'private': True, 'name': 'testuser7', 'recipe': 'recipe7', 'diet_category': 'LACTOSE_FREE',
                        'ingredients': ingredients, 'amounts': amounts}

        response = view_client.post(my_recipe_list_url, post_payload, content_type='application/json')
        put_payload = {'private': True, 'name': 'testuser11', 'recipe': 'recipe11', 'diet_category': 'RAW',
                       'ingredients': [ingredients[0]], 'amounts': [amounts[1]]}
        response = view_client.put(my_recipe_detail_url(args=[response.data.get('id')]), put_payload,
                                   content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == put_payload.get('name')
        assert response.data.get('recipe') == put_payload.get('recipe')
        assert response.data.get('diet_category') == 'RAW'
        assert response.data.get('total_ingredients') == len(ingredients)

        # check if quantity_total and weight_total for ingredient are calculated
        response = view_client.get(ingredient_list_url)
        assert dict(response.data.get('results')[0]).get('quantity_total') is not None
        assert dict(response.data.get('results')[0]).get('weight_total') is not None

    def test_create_recipe_with_ingredients(self, my_recipe_detail_url, view_client, make_my_recipe_user,
                                            make_ingredients_batch, make_recipeingredient, ingredient_list_url):
        ingredients = make_ingredients_batch(6)
        recipe_user = make_my_recipe_user
        recipe = recipe_user['recipe']
        user = recipe_user['user']
        view_client.force_login(user=user)

        for i in range(len(ingredients)):
            make_recipeingredient(ingredient=ingredients[i], recipe=recipe)
        response = view_client.get(my_recipe_detail_url(args=[recipe.pk]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == recipe.name
        assert response.data.get('recipe') == recipe.recipe
        assert response.data.get('total_ingredients') == len(list(recipe.ingredients.all()))

        # check if quantity_total and weight_total for ingredient are calculated
        response = view_client.get(ingredient_list_url)
        assert dict(response.data.get('results')[0]).get('quantity_total') is not None
        assert dict(response.data.get('results')[0]).get('weight_total') is not None

    def test_count_calories(self, my_recipe_detail_url, view_client, make_my_recipe_user, make_ingredients_batch,
                            make_recipeingredient, ingredient_list_url):
        ingredients = make_ingredients_batch(6)
        recipe_user = make_my_recipe_user
        recipe = recipe_user['recipe']
        user = recipe_user['user']
        view_client.force_login(user=user)
        for i in range(len(ingredients)):
            make_recipeingredient(ingredient=ingredients[i], recipe=recipe)
        response = view_client.get(my_recipe_detail_url(args=[recipe.pk]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == recipe.name
        assert response.data.get('recipe') == recipe.recipe
        assert response.data.get('total_ingredients') == len(list(recipe.ingredients.all()))
        calories = Recipe.objects.aggregate(sum=Sum('ingredients__kcal'))
        assert calories['sum'] == response.data.get('total_kcals')

        # check if quantity_total and weight_total for ingredient are calculated
        response = view_client.get(ingredient_list_url)
        assert dict(response.data.get('results')[0]).get('quantity_total') is not None
        assert dict(response.data.get('results')[0]).get('weight_total') is not None

    def test_patch_recipe(self, my_recipe_detail_url, view_client, make_my_recipe_user):
        recipe_user = make_my_recipe_user
        recipe = recipe_user['recipe']
        user = recipe_user['user']
        view_client.force_login(user=user)
        payload = {'recipe': 'recipe7'}
        response = view_client.patch(my_recipe_detail_url(args=[recipe.pk]), payload, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('recipe') == payload.get('recipe')

    def test_private_get_no_authentication_fail(self, my_recipe_detail_url, view_client, make_my_recipe_user):
        recipe_user = make_my_recipe_user
        recipe = recipe_user['recipe']
        user = recipe_user['user']
        user2 = UserFactory()
        view_client.force_login(user=user2)

        response = view_client.get(my_recipe_detail_url(args=[recipe.pk]))

        assert response.status_code == status.HTTP_404_NOT_FOUND

        # now we authenticate with the owner's credentials
        view_client.force_login(user=user)
        response = view_client.get(my_recipe_detail_url(args=[recipe.pk]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == recipe.name
        assert response.data.get('recipe') == recipe.recipe
        assert response.data.get('diet_category') == 'RAW'
