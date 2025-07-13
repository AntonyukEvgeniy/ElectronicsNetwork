from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from .models import NetworkNode
from .serializers import NetworkNodeSerializer


class NetworkNodeFilter(filters.FilterSet):
    country = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = NetworkNode
        fields = ['country']


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type', 'city', 'country']
    search_fields = ['name', 'email']