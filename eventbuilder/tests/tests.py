import json

import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from meals.tests.factories import MealFactory
from pumpkin.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytestmark
class TestEventBuilderTestCase:
    """
    Tests post event in google calendar list operations.
    """

    def test_post_event(self, view_client):
        user = UserFactory()
        meal = MealFactory(owner=user)
        view_client.force_login(user)
        data = {
            "meal_name": meal.name,
            "choice": "BREAKFAST",
            "event_date": "2019-05-26 01:19:26"
        }
        response = view_client.post(reverse('event'), data)

        assert response.status_code == status.HTTP_201_CREATED
        assert json.loads(response.data).get('status') == 'confirmed'
