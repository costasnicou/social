
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like/<int:postid>",views.like,name="like"),
    path("unlike/<int:postid>",views.unlike,name="unlike"),
    path("profile/<str:profile_user>",views.profile,name="profile"),
    path("following",views.following,name="following"),
    path("save_edited_post/<int:postid>",views.save_edited_post,name="save_edited_post"),


]
