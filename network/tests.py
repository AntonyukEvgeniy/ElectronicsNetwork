import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from network.models import NetworkNode


@pytest.fixture
def api_client():
    return APIClient()


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


@pytest.mark.django_db
class TestNetworkNodeViewSet:
    def test_list_network_nodes(self, api_client, network_node):
        url = reverse("network-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == network_node.name

    def test_retrieve_network_node(self, api_client, network_node):
        url = reverse("network-detail", kwargs={"pk": network_node.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == network_node.name

    def test_create_network_node(self, api_client):
        url = reverse("network-list")
        data = {
            "name": "New Factory",
            "type": "factory",
            "email": "new@factory.com",
            "country": "New Country",
            "city": "New City",
            "street": "New Street",
            "building": "2",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert NetworkNode.objects.count() == 1
        assert NetworkNode.objects.first().name == "New Factory"

    def test_update_network_node(self, api_client, network_node):
        url = reverse("network-detail", kwargs={"pk": network_node.pk})
        data = {
            "name": "Updated Factory",
            "type": "factory",
            "email": "updated@factory.com",
            "country": "Updated Country",
            "city": "Updated City",
            "street": "Updated Street",
            "building": "3",
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        network_node.refresh_from_db()
        assert network_node.name == "Updated Factory"

    def test_delete_network_node(self, api_client, network_node):
        url = reverse("network-detail", kwargs={"pk": network_node.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert NetworkNode.objects.count() == 0

    def test_filter_by_country(self, api_client, network_node):
        url = reverse("network-list")
        response = api_client.get(url, {"country": "Test"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["country"] == network_node.country

    def test_search_by_name(self, api_client, network_node):
        url = reverse("network-list")
        response = api_client.get(url, {"search": "Test"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == network_node.name
