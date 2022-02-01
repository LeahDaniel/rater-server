from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    designer = models.CharField(max_length=50)
    description = models.TextField()
    year_released = models.PositiveIntegerField()
    number_of_players = models.PositiveIntegerField()
    hours_playtime = models.PositiveIntegerField()
    min_age_recommended = models.PositiveIntegerField()
