from django.shortcuts import render


def home(request):
    return render(request, "main/block1.html")


def page2(request):
    return render(request, "main/block2.html")


# Create your views here.
