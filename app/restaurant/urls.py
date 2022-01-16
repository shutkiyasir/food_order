from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("restaurants", views.RestaurantViewSet)

app_name = "restaurant"

urlpatterns = [
    path("", include(router.urls)),
    path("menu/", views.ListCreateMenuView.as_view(), name="menu"),
]
