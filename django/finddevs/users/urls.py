from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>/", views.userProfile, name="user-profile"),
    path("account/", views.userAccount, name="account"),
    path("edit-account/", views.editAccount, name="edit-account"),
    path("add-skills/", views.addSkill, name="add-skills"),
]
