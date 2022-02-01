from django.contrib.auth.models import User
from django.db import models
from .game import Game
from .category import Category

class GameCategory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)