from django.conf import settings
from django.db import models


class Vote(models.Model):
    """Vote given by user"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    menu = models.ForeignKey("Menu", on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "menu",
        )

    def __str__(self):
        return f"{self.user.email} {self.menu.name}"


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
