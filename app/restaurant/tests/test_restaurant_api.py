from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.models import Restaurant
from restaurant.serializers import RestaurantSerializer

from .utils import sample_restaurant

RECIPES_URL = reverse("restaurant:restaurant-list")


class PublicRestaurantApiTests(TestCase):
    """Test unauthenticated restaurant API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRestaurantApiTests(TestCase):
    """Test unauthenticated restaurant API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@gmail.com", "testpass")
        self.client.force_authenticate(self.user)

    def test_retrieve_restaurants(self):
        """Test retrieving a list of restaurants"""
        sample_restaurant()
        sample_restaurant()

        res = self.client.get(RECIPES_URL)

        restaurants = Restaurant.objects.all().order_by("-id")
        serializer = RestaurantSerializer(restaurants, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_restaurant(self):
        """Test creating restaurant"""
        payload = {"title": "Sultan's Dine"}
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        restaurant = Restaurant.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(restaurant, key))
