import pytest
from django.test import Client
from rest_framework.test import APIRequestFactory


@pytest.fixture()
def api_client():
    return APIRequestFactory()


@pytest.fixture()
def view_client():
    return Client()
