from django.contrib.auth.models import User
from django.db import models


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()