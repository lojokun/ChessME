from django.urls import path

from matches import views

urlpatterns = [
    path("login/", views.do_login, name="login"),
    path("create-account/", views.create_account, name="create_account"),
    path("pass-board/<int:match_id>/", views.pass_board, name="pass_board"),
    path("refresh-board/<int:match_id>/", views.refresh_board, name="refresh_board"),
    path("create-match/", views.create_match, name="create_match"),
    path("create-friendship/", views.create_friendship, name="create_friendship"),
    path("send-challenge/<int:challenged_id>/", views.send_challenge, name="send_challenge"),
    path("get-challenge/", views.get_challenge, name="get_challenge"),
    # path("get-current-user/", views.get_current_user, name="get_current_user"),

]
