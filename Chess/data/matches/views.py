from django.contrib.auth.models import User
# from django.core import serializers
from django.http import HttpResponse
# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from matches.models import Player, GameState, Match


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
        friends = []
        return HttpResponse(f"{player.id}/{player.rating}")
    else:
        return HttpResponse(status=403)


@csrf_exempt
def refresh_board(request, match_id):
    match = Match.objects.get(id=match_id)
    all_states = GameState.objects.filter(match_id=match_id)
    old_gamestate = all_states[len(all_states) - 1]
    old_gamestate.board += f"\n{match_id}"
    # response = {"match": match,
    #             "board": old_gamestate.board}
    return HttpResponse(old_gamestate.board)


@csrf_exempt
def pass_board(request, match_id):
    print(request.POST)
    string_board = request.POST.get("board", "")
    all_states = GameState.objects.filter(match_id=match_id)
    old_gamestate = all_states[len(all_states) - 1]
    gamestate = GameState.objects.create(board=string_board, match_id=match_id,
                                         white_to_move=not old_gamestate.white_to_move)
    # gamestate.board = string_board
    # gamestate.white_to_move = not gamestate.white_to_move
    # gamestate.save()
    print(string_board)
    return HttpResponse()


@csrf_exempt
def create_account(request):
    print(request.POST)
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    email = request.POST.get("email", "")
    try:
        new_user = User.objects.create_user(username=username, password=password)
        new_user.email = email
    except User.objects.get(username=username):
        print("Username already taken")
        new_user = None
        return HttpResponse(status=402)
    except User.objects.get(email=email):
        print("Email already used")
        new_user = None
        return HttpResponse(status=401)

    new_user.save()
    return HttpResponse()


@csrf_exempt
def create_match(request):
    print(request.POST)
    white_player = request.POST.get("white_player", "")
    black_player = request.POST.get("black_player", "")

    Match.objects.create(white_player=white_player, black_player=black_player, move_log="")
    return HttpResponse()
