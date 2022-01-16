from rest_framework import serializers

from .models import Menu, Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """Serialize a restaurant"""

    class Meta:
        model = Restaurant
        fields = ("id", "title")
        read_only_fields = ("id",)


class MenuSerializer(serializers.ModelSerializer):
    """Serialize a restaurant menu"""

    class Meta:
        model = Menu
        fields = ("id", "name", "serve_date", "restaurant")
        read_only_fields = ("id",)
