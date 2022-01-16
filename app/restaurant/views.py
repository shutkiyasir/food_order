from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import Menu, Restaurant


class RestaurantViewSet(viewsets.ModelViewSet):
    """Manage restaurants in the database"""

    serializer_class = serializers.RestaurantSerializer
    queryset = Restaurant.objects.all().order_by("-id")
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ListCreateMenuView(generics.ListCreateAPIView):
    """Manage resturant menus in the database"""

    serializer_class = serializers.MenuSerializer
    queryset = Menu.objects.all().order_by("-name")
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
