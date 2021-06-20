from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    rating = models.IntegerField(default=1200)


class Match(models.Model):
    white_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="white_player")
    black_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="black_player")
    move_log = models.TextField()


class GameState(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    board = models.TextField(
        default="""bRbNbBbQbKbBbNbRbpbpbpbpbpbpbpbp----------------------------------------------------------------wpwpwpwpwpwpwpwpwRwNwBwQwKwBwNwR""")
    white_to_move = models.BooleanField(default=True)
    state = models.IntegerField(default=0)  # 0 - create, 1 - ongoing, 2 - finished
