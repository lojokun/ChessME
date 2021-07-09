from django.contrib.auth.models import User
# from django.core import serializers
from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from matches.models import Player, GameState, Match
from friends.models import Friendship


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
        friendships1 = Friendship.objects.filter(friend1=player)
        friendships2 = Friendship.objects.filter(friend2=player)
        friends1 = [friendship.friend2 for friendship in friendships1]
        friends2 = [friendship.friend1 for friendship in friendships2]
        # friends1values = friendships1.values()
        # friends2values = friendships2.values()
        friend_list = [friend for friend in friends1]
        friend_list.extend([friend for friend in friends2])
        friendships = [{"id": friend.user.id, "name": friend.user.username} for friend in friend_list]
        response_dict = {"id": player.user.id,
                         "name": player.user.username,
                         "friendships": friendships}
        return HttpResponse(json.dumps(response_dict))
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
        new_user.save()
    except User.objects.get(username=username):
        print("Username already taken")
        return HttpResponse(status=402)
    except User.objects.get(email=email):
        print("Email already used")
        return HttpResponse(status=401)

    return HttpResponse()


@csrf_exempt
def create_match(request):
    print(request.POST)
    white_player = request.POST.get("white_player", "")
    black_player = request.POST.get("black_player", "")

    new_match = Match.objects.create(white_player=white_player, black_player=black_player, move_log="")
    GameState.objects.create(match=new_match)
    return HttpResponse()


@csrf_exempt
def create_friendship(request):
    print(request.POST)
    friend1 = request.POST.get("friend1", "")
    friend2 = request.POST.get("friend2", "")

    Friendship.objects.create(friend1=friend1, friend2=friend2)
    return HttpResponse()
