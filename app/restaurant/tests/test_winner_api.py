from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.serializers import RestaurantSerializer

from .utils import sample_menu, sample_restaurant, sample_user, sample_vote

WINNER_URL = reverse("restaurant:winner")


class PublicVotesApiTests(TestCase):
    """Test the publicly available winner API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving winner restaurant"""
        res = self.client.get(WINNER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateVotesApiTests(TestCase):
    """Test the authorized winner API"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_winner_restaurant(self):
        """Test retrieving winner restaurant"""
        restaurant1 = sample_restaurant(title="Pizza Hut")
        restaurant2 = sample_restaurant(title="KFC")

        serve_date = date.today()
        menu1 = sample_menu(name="Pizza", restaurant=restaurant1, serve_date=serve_date)
        menu2 = sample_menu(
            name="Chicken", restaurant=restaurant2, serve_date=serve_date
        )

        user2 = sample_user(email="test2@gmail.com")
        user3 = sample_user(email="test3@gmail.com")

        sample_vote(menu1, user=self.user)
        sample_vote(menu2, user=user2)
        sample_vote(menu2, user3)

        res = self.client.get(WINNER_URL, {"serve_date": date.today()})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = RestaurantSerializer([restaurant2], many=True)
        self.assertEqual(res.data, serializer.data)
