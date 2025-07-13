import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from network.models import NetworkNode


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def active_staff_user():
    User = get_user_model()
    user = User.objects.create_user(
        username="staff_user", password="testpass123", is_staff=True, is_active=True
    )
    return user


@pytest.fixture
def authenticated_client(api_client, active_staff_user):
    refresh = RefreshToken.for_user(active_staff_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def network_node():
    return NetworkNode.objects.create(
        name="Test Factory",
        type="factory",
        email="test@factory.com",
        country="Test Country",
        city="Test City",
        street="Test Street",
        building="1",
    )
