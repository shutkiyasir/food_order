from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer

from .utils import sample_restaurant

MENUS_URL = reverse("restaurant:menu")


class PrivateMenusApiTests(TestCase):
    """Test the private menus API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@gmail.com", "testpass")
        self.client.force_authenticate(self.user)

    def test_retrieve_menu_list(self):
        """Test retrieving a list of menus"""
        restaurant = sample_restaurant()
        restaurant2 = sample_restaurant(title="Pitstop")
        Menu.objects.create(
            name="Salad", serve_date=date.today(), restaurant=restaurant
        )
        Menu.objects.create(
            name="Mutton Curry", serve_date=date.today(), restaurant=restaurant2
        )

        res = self.client.get(MENUS_URL)

        menus = Menu.objects.all().order_by("-name")
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_menu_for_specific_date(self):
        """Test retriving menus for a single date"""
        restaurant = sample_restaurant()
        current_date = date.today()
        previous_date = current_date - timedelta(1)

        menu = Menu.objects.create(
            name="Salad", serve_date=current_date, restaurant=restaurant
        )
        menu2 = Menu.objects.create(
            name="Ramen", serve_date=previous_date, restaurant=restaurant
        )

        res = self.client.get(MENUS_URL, {"serve_date": current_date})

        serializer1 = MenuSerializer(menu)
        serializer2 = MenuSerializer(menu2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)


class AdminUsersApiTests(TestCase):
    """Test the admin menus API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@gmail.com", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_menu(self):
        """Test creating menu"""
        restaurant = sample_restaurant()
        payload = {
            "name": "Salad",
            "serve_date": date.today(),
            "restaurant": restaurant.id,
        }
        res = self.client.post(MENUS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        menu = Menu.objects.get(id=res.data["id"])
        self.assertEqual(menu.name, payload["name"])
        self.assertEqual(menu.serve_date, payload["serve_date"])
        self.assertEqual(menu.restaurant, restaurant)

    def test_create_menu_successful(self):
        """Test create a new menu"""
        restaurant = sample_restaurant()
        payload = {
            "name": "Fried Rice",
            "serve_date": date.today(),
            "restaurant": restaurant.id,
        }
        self.client.post(MENUS_URL, payload)

        exists = Menu.objects.filter(
            name=payload["name"],
        ).exists()
        self.assertTrue(exists)

    def test_create_menu_invalid(self):
        """Test creating invalid menu fails"""
        payload = {"name": ""}
        res = self.client.post(MENUS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_only_one_menu_per_day_for_each_restaurant(self):
        """Test creating only one menu per day for each restaurant"""
        restaurant = sample_restaurant()
        current_date = date.today()
        payload = {
            "name": "Salad",
            "serve_date": current_date,
            "restaurant": restaurant.id,
        }

        res = self.client.post(MENUS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.post(MENUS_URL, payload)
        self.assertNotEqual(res.status_code, status.HTTP_201_CREATED)
