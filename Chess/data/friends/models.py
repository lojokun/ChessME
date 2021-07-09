import json

from django.db import models

from matches.models import Player


class Friendship(models.Model):
    friend1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="friend1")
    friend2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="friend2")
