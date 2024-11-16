from django.shortcuts import render


def view(request):
    return render(request, "viewtable/view.html")


# Create your views here.
