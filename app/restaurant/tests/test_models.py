from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from restaurant import models


def sample_user(email="test@gmail.com", password="testpass"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


def sample_restaurant(title="Barcode"):
    """Create a sample restaurant"""
    return models.Restaurant.objects.create(title=title)


def sample_menu(name="Biryani", restaurant=None):
    """Create a sample menu"""
    if not restaurant:
        restaurant = sample_restaurant()
    return models.Menu.objects.create(
        name=name, serve_date=date.today(), restaurant=restaurant
    )


class ModelTests(TestCase):
    def test_restaurant_str(self):
        """Test the restaurant string representation"""
        restaurant = sample_restaurant()
        self.assertEqual(str(restaurant), restaurant.title)

    def test_menu_str(self):
        """Test the menu string respresentation"""
        menu = sample_menu()
        self.assertEqual(str(menu), menu.name)

    def test_vote_str(self):
        """Test the vote string respresentation"""
        menu = sample_menu()
        user = sample_user()
        vote = models.Vote.objects.create(menu=menu, user=user)
        self.assertEqual(str(vote), f"{user.email} {menu.name}")
