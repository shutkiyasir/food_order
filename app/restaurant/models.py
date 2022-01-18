from datetime import timedelta

from django.conf import settings
from django.db import models

from .managers import VoteManager


class Vote(models.Model):
    """Vote given by user"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    menu = models.ForeignKey("Menu", on_delete=models.CASCADE)

    objects = VoteManager()

    class Meta:
        unique_together = ("user", "menu")

    def __str__(self):
        return f"{self.user.email} {self.menu.name}"

    @classmethod
    def get_winner_restaurant(cls, serve_date):
        """Filter and return winner restaurant"""
        previous_winner = cls.get_previous_winner_restaurant(serve_date)
        highest_vote = cls.objects.filter_highest_vote(serve_date, previous_winner)

        if highest_vote is None:
            # No restaurant found
            return Restaurant.objects.none()

        winner_menu = Menu.objects.filter(id=highest_vote["menu"]).last()
        return Restaurant.objects.filter(id=winner_menu.restaurant_id)

    @classmethod
    def get_previous_winner_restaurant(cls, serve_date):
        """Filter and return previous two time winner restaurant id"""
        previous_winner_menus = [
            cls.objects.filter_highest_vote(serve_date - timedelta(1)),
            cls.objects.filter_highest_vote(serve_date - timedelta(2)),
        ]
        previous_winner_restaurants = list(
            Menu.objects.filter(id__in=previous_winner_menus).values_list(
                "restaurant_id", flat=True
            )
        )

        # Check if a restaurant won both times in last two days
        if (
            len(previous_winner_restaurants) > 1
            and previous_winner_restaurants[0] == previous_winner_restaurants[1]
        ):
            return previous_winner_restaurants[0]


class Menu(models.Model):
    """Menu to be served by a restaurant"""

    name = models.CharField(max_length=255)
    serve_date = models.DateField(help_text="Date on which the menu will be served")
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "serve_date",
            "restaurant",
        )

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    """Restaurant object"""

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
