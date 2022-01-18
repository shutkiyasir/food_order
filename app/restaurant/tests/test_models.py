from django.test import TestCase
from restaurant import models

from .utils import sample_menu, sample_restaurant, sample_user


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
