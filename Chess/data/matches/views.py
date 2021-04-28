from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from matches.models import Player


@csrf_exempt
def do_login(request):
    print(request.POST)
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    if user is not None and user.check_password(password):
        player = Player.objects.get(user=user)
        return HttpResponse(f"{player.rating}")
    else:
        return HttpResponse(status=403)


@csrf_exempt
def pass_board(request):
    pass


@csrf_exempt
def create_account(request):
    print(request.POST)
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    email = request.POST.get("email", "")
    try:
        new_user = User.objects.create_user(username=username, email=email, password=password)
    except:
        new_user = None

    if new_user is not None:
        return HttpResponse()
    else:
        return HttpResponse(status=403)
