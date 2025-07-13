from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import NetworkNode
from .serializers import NetworkNodeSerializer


class NetworkNodeFilter(filters.FilterSet):
    country = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = NetworkNode
        fields = ["country"]


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkNodeFilter
    filterset_fields = ["type", "city", "country"]
    search_fields = ["name", "email"]
