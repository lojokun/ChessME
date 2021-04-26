from django.contrib.auth.models import User
from django.db import models


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    rating = models.IntegerField(default=1200)


class Match(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player1")
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player2")
    move_log = models.TextField()
