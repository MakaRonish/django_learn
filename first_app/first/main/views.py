from django.shortcuts import render
from . import models


def home(request):
    books = models.Books_table.objects.all()
    context = {"books": books}
    return render(request, "main/block1.html", context)


def page2(request):
    return render(request, "main/block2.html")


# Create your views here.
