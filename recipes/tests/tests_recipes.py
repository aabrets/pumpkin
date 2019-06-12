import pytest
from django.db.models import Sum
from django.forms.models import model_to_dict
from rest_framework import status

from pumpkin.users.test.factories import UserFactory
from ..models import Recipe, RecipeIngredient
from .factories import RecipeFactory

pytestmark = pytest.mark.django_db


@pytestmark
class TestRecipeListTestCase:
    """
    Tests /recipes list operations.
    """
    def test_get_recipe_list(self, recipe_list_url, view_client):
        user = UserFactory()
        for i in range(3):
            RecipeFactory(owner=user)
        view_client.force_login(user=user)
        response = view_client.get(recipe_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results')) == 3

    def test_post_with_no_data_fails(self, recipe_list_url, view_client):
        response = view_client.post(recipe_list_url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_valid_data_succeeds(self, recipe_list_url, view_client):
        user = UserFactory()
        view_client.force_login(user=user)
        recipe_data = model_to_dict(RecipeFactory.build())
        recipe_data['owner'] = user
        recipe_data['diet_category'] = 'VEGAN'
        response = view_client.post(recipe_list_url, recipe_data)
        assert response.status_code == status.HTTP_201_CREATED

        recipe = Recipe.objects.get(pk=response.data.get('id'))
        assert recipe.name == recipe_data.get('name')
        assert recipe.diet_category == recipe_data.get('diet_category')

    def test_post_with_ingredients_recipe(self, recipe_list_url, view_client, make_ingredients_batch):
        user = UserFactory()
        view_client.force_login(user)
        ingredient_objects = make_ingredients_batch(6)
        amounts = [1.5, 2.3, 0.5, 0.4, 4.3, 5.2]
        ingredients = [ingredient.pk for ingredient in ingredient_objects]
        view_client.force_login(user=user)
        payload = {'name': 'testuser7', 'recipe': 'recipe7', 'diet_category': 'LACTOSE_FREE',
                   'ingredients': ingredients, 'amounts': amounts}
        response = view_client.post(recipe_list_url, payload, content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('name') == payload.get('name')
        assert response.data.get('recipe') == payload.get('recipe')
        assert len(response.data.get('ingredients')) == len(payload.get('ingredients'))


@pytestmark
class TestRecipeDetailTestCase:
    """
    Tests /recipes detail operations.
    """

    def test_get_recipe(self, recipe_detail_url, view_client, make_recipe_user):
        recipe_user = make_recipe_user
        recipe = recipe_user['recipe']
        user = recipe_user['user']
        view_client.force_login(user=user)
        response = view_client.get(recipe_detail_url(args=[recipe.pk]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == recipe.name
        assert response.data.get('recipe') == recipe.recipe
        assert response.data.get('diet_category') == 'RAW'

    def test_delete_recipe(self, recipe_detail_url, view_client, make_recipe_user):
        recipe_user = make_recipe_user
        recipe = recipe_user['recipe']
        user = recipe_user['user']
        view_client.force_login(user=user)
        response = view_client.delete(recipe_detail_url(args=[recipe.pk]))

        assert response.status_code == status.HTTP_204_NO_CONTENT

        recipes = Recipe.objects.all()
        assert len(recipes) == 0

    def test_put_recipe(self, recipe_detail_url, recipe_list_url, view_client, make_ingredients_batch):
        user = UserFactory()
        view_client.force_login(user)
        ingredient_objects = make_ingredients_batch(6)
        amounts = [1.5, 2.3, 0.5, 0.4, 4.3, 5.2]
        ingredients = [ingredient.pk for ingredient in ingredient_objects]
        view_client.force_login(user=user)
        post_payload = {'name': 'testuser7', 'recipe': 'recipe7', 'diet_category': 'LACTOSE_FREE',
                        'ingredients': ingredients, 'amounts': amounts}

        response = view_client.post(recipe_list_url, post_payload, content_type='application/json')
        put_payload = {'name': 'testuser11', 'recipe': 'recipe11', 'diet_category': 'RAW',
                       'ingredients': [ingredients[0]], 'amounts': [amounts[1]]}
        response = view_client.put(recipe_detail_url(args=[response.data.get('id')]), put_payload,
                                   content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == put_payload.get('name')
        assert response.data.get('recipe') == put_payload.get('recipe')
        assert response.data.get('diet_category') == 'RAW'
        assert response.data.get('total_ingredients') == len(ingredients)
        calories = Recipe.objects.aggregate(sum=Sum('ingredients__kcal'))
        assert calories['sum'] == response.data.get('total_kcals')

    def test_create_recipe_with_ingredients(self, recipe_detail_url, view_client, make_recipe_user,
                                            make_ingredients_batch, ingredient_list_url):
        ingredients = make_ingredients_batch(6)

        recipe_user = make_recipe_user
        recipe = recipe_user['recipe']
        user = recipe_user['user']
        view_client.force_login(user=user)
        for i in range(6):
            RecipeIngredient.objects.create(amount=3, ingredient=ingredients[i], recipe=recipe)
        response = view_client.get(recipe_detail_url(args=[recipe.pk]))

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

    def test_count_calories(self, recipe_detail_url, view_client, make_recipe_user, make_ingredients_batch,
                            make_recipeingredient, ingredient_list_url):
        ingredients = make_ingredients_batch(6)
        recipe_user = make_recipe_user
        recipe = recipe_user['recipe']
        user = recipe_user['user']
        view_client.force_login(user=user)
        for i in range(len(ingredients)):
            make_recipeingredient(ingredient=ingredients[i], recipe=recipe)
        response = view_client.get(recipe_detail_url(args=[recipe.pk]))

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

    def test_patch_recipe(self, recipe_detail_url, view_client, make_recipe_user):
        recipe_user = make_recipe_user
        recipe = recipe_user['recipe']
        user = recipe_user['user']
        view_client.force_login(user=user)
        payload = {'recipe': 'recipe7'}
        response = view_client.patch(recipe_detail_url(args=[recipe.pk]), payload, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('recipe') == payload.get('recipe')
