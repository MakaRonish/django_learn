from django.shortcuts import render


def page1(request):
    return render(request, "appone/page1.html")


def page2(request):
    return render(request, "appone/page2.html")


# Create your views here.
