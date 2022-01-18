from datetime import date

from django.contrib.auth import get_user_model
from restaurant.models import Menu, Restaurant, Vote


def sample_user(email="test@gmail.com", password="password123"):
    """Create and return sample user"""
    return get_user_model().objects.create_user(email=email, password=password)


def sample_restaurant(title="Barcode"):
    """Create and return a sample restaurant"""
    return Restaurant.objects.create(title=title)


def sample_menu(name="Biryani", restaurant=None, serve_date=None):
    """Create and return a sample menu"""
    if not restaurant:
        restaurant = sample_restaurant()
    if not serve_date:
        serve_date = date.today()
    return Menu.objects.create(name=name, serve_date=serve_date, restaurant=restaurant)


def sample_vote(menu=None, user=None):
    """Create and return a sample vote"""
    if not menu:
        menu = sample_menu()
    if not user:
        user = sample_user()
    return Vote.objects.create(menu=menu, user=user)
