from datetime import date, datetime

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from . import serializers
from .models import Menu, Restaurant, Vote
from .permissions import IsAdminUserOrReadOnly


class ListCreateRestaurantViewSet(generics.ListCreateAPIView):
    """Manage restaurants in the database"""

    serializer_class = serializers.RestaurantSerializer
    queryset = Restaurant.objects.all().order_by("-id")
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)


class ListCreateMenuView(generics.ListCreateAPIView):
    """Manage resturant menus in the database"""

    serializer_class = serializers.MenuSerializer
    queryset = Menu.objects.all().order_by("-name")
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)

    def get_queryset(self):
        """Return objects for specific date or restaurant"""
        queryset = self.queryset

        serve_date = self.request.query_params.get("serve_date")
        if serve_date:
            queryset = queryset.filter(serve_date=serve_date)

        restaurant_id = self.request.query_params.get("restaurant_id")
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        return queryset.order_by("-name")


class CreateVoteView(generics.CreateAPIView):
    """Manage votes in the database"""

    serializer_class = serializers.VoteSerializer
    queryset = Vote.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ListWinnerRestaurantView(generics.ListAPIView):
    """Lists winner restaurant"""

    serializer_class = serializers.RestaurantSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        serve_date = self.request.query_params.get("serve_date")
        if serve_date:
            serve_date = datetime.strptime(serve_date, "%Y-%m-%d")
        else:
            serve_date = date.today()

        return Vote.get_winner_restaurant(serve_date)
