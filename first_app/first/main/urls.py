from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="root"),
    path("block2", views.page2, name="page2"),
    path("addbook", views.add_book, name="AddBook"),
    path("editbook/<str:pk>/", views.edit, name="edit"),
]
