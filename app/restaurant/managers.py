from django.db import models
from django.db.models import Count


class VoteManager(models.Manager):
    def filter_highest_vote(self, serve_date, previous_winner=None):
        """Filters highest voted menu of the serve_date"""
        return (
            self.filter(menu__serve_date=serve_date)
            .exclude(menu__restaurant=previous_winner)
            .values("menu")
            .annotate(vote_count=Count("menu"))
            .order_by("vote_count")
            .last()
        )
