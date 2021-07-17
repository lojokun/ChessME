from django.urls import path

from .consumers import GetChallengeConsumer, SendChallengeConsumer

ws_urlpatterns = [
    path("get-challenge/", GetChallengeConsumer.as_asgi()),
    path("send-challenge/", SendChallengeConsumer.as_asgi()),
]
