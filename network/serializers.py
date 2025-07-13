from rest_framework import serializers
from .models import NetworkNode


class NetworkNodeSerializer(serializers.ModelSerializer):
    debt_to_supplier = serializers.DecimalField(
        source='debt',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'type', 'email', 'country',
            'city', 'street', 'building', 'created_at',
            'debt_to_supplier', 'parent'
        ]