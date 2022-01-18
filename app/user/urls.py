from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("", views.CreateUserView.as_view(), name="create"),
    path("me/", views.ManageUserView.as_view(), name="me"),
]
