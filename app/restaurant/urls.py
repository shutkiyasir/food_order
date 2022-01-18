from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    path("", views.ListCreateRestaurantViewSet.as_view(), name="restaurant"),
    path("menu/", views.ListCreateMenuView.as_view(), name="menu"),
    path("vote/", views.CreateVoteView.as_view(), name="vote"),
    path("winner/", views.ListWinnerRestaurantView.as_view(), name="winner"),
]
