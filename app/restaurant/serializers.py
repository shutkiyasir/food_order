from rest_framework import serializers

from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """Serialize a restaurant"""

    class Meta:
        model = Restaurant
        fields = ("id", "title")
        read_only_fields = ("id",)
