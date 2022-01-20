from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    path("", views.ListCreateRestaurantViewSet.as_view(), name="restaurant"),
    path("<int:id>/", views.RetrieveRestaurantView.as_view(), name="restaurant-detail"),
    path("menu/", views.ListCreateMenuView.as_view(), name="menu"),
    path("menu/<int:id>/", views.RetrieveMenuDetailView.as_view(), name="menu-detail"),
    path("vote/", views.CreateVoteView.as_view(), name="vote"),
    path("winner/", views.ListWinnerRestaurantView.as_view(), name="winner"),
]
