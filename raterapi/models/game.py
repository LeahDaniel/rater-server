from django.contrib.auth.models import User
from django.db import models
from .rating import Rating


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    designer = models.CharField(max_length=50)
    description = models.TextField()
    year_released = models.PositiveIntegerField()
    number_of_players = models.PositiveIntegerField()
    hours_playtime = models.PositiveIntegerField()
    min_age_recommended = models.PositiveIntegerField()
    categories = models.ManyToManyField(
        "Category", through="GameCategory", related_name="attending")

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Rating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        
        if len(ratings) > 0:
            for rating in ratings:
                total_rating += rating.rating

            return total_rating / len(ratings)
        else :
            return None
