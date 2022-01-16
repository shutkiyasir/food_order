from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.models import Menu, Restaurant, Vote
from restaurant.serializers import VoteSerializer

VOTES_URL = reverse("restaurant:vote")


class PublicVotesApiTests(TestCase):
    """Test the publicly available votes API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving votes"""
        res = self.client.get(VOTES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateVotesApiTests(TestCase):
    """Test the authorized user votes API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@gmail.com", "password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_vote_successful(self):
        """Test creating a new vote"""
        restaurant = Restaurant.objects.create(title="Barcode")
        menu = Menu.objects.create(
            name="Salad", serve_date=date.today(), restaurant=restaurant
        )
        payload = {"menu": menu.id}
        self.client.post(VOTES_URL, payload)

        exists = Vote.objects.filter(user=self.user, menu=menu).exists()
        self.assertTrue(exists)

    def test_create_vote_invalid(self):
        """Test creating a new vote with invalid payload"""
        payload = {"menu": ""}
        res = self.client.post(VOTES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_only_one_vote_per_user_per_menu(self):
        """Test creating only one vote per menu by a user"""
        restaurant = Restaurant.objects.create(title="Barcode")
        menu = Menu.objects.create(
            name="Salad", serve_date=date.today(), restaurant=restaurant
        )
        payload = {"menu": menu.id}
        res = self.client.post(VOTES_URL, payload)
        # First vote creation successful
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res2 = self.client.post(VOTES_URL, payload)
        # Second vote for same menu failed
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
