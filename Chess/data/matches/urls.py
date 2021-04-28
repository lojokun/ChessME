from django.urls import path

from matches import views

urlpatterns = [
    path("login/", views.do_login, name="login"),
    path("create-account/", views.create_account, name="create_account")
]