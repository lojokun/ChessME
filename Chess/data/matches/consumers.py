from channels.generic.websocket import WebsocketConsumer
import requests
import json


# from django.views.decorators.csrf import csrf_exempt


class GetChallengeConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        response = self.receive()
        print(response)

    # Get's the challenge from the user
    def get_challenge(self, response):
        print("GET")
        data_dict = json.loads(response)
        friend = data_dict["friend"]
        print(friend)


class SendChallengeConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    # Sends the challenge to the user
    def send_challenge(self):
        pass
        # friend = request.POST.get("friend", "")
        # print(friend)
