from datetime import datetime

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

    def get_queryset(self):
        """Return objects for specific date only"""
        serve_date = self.request.query_params.get("serve_date")
        queryset = self.queryset
        if serve_date:
            serve_date = datetime.strptime(serve_date, "%Y-%m-%d").date()
            queryset = queryset.filter(serve_date=serve_date)
        return queryset.order_by("-name")
