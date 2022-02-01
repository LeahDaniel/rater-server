from django.contrib.auth.models import User
from django.db import models
from .game import Game

class GameReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    review = models.TextField()