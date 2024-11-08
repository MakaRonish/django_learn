from django.shortcuts import render
from .models import database


def page1(request):
    items = database.objects.all()
    context = {"item": items}
    return render(request, "appone/page1.html", context)


def page2(request):
    return render(request, "appone/page2.html")


# Create your views here.
