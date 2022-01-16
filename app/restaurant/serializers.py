from rest_framework import serializers

from .models import Menu, Restaurant, Vote


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


class VoteSerializer(serializers.ModelSerializer):
    """Serialize a vote"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vote
        fields = ("id", "menu", "user")
        read_only_fields = ("id",)
