from django.contrib.auth.models import User
from django.db import models

from .category import Category
from .game_category import GameCategory


class Game(models.Model):
    title = models.CharField(max_length=50)
    designer = models.CharField(max_length=50)
    description = models.TextField()
    year_released = models.PositiveIntegerField()
    number_of_players = models.PositiveIntegerField()
    hours_playtime = models.PositiveIntegerField()
    min_age_recommended = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category, through=GameCategory, related_name="attending")
