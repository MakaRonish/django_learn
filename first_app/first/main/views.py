from django.shortcuts import render, redirect
from . import models
from .form import Bookform, Publisherform


def home(request):
    books = models.Books_table.objects.all()
    context = {"books": books}
    return render(request, "main/block1.html", context)


def page2(request, pk):
    book = models.Books_table.objects.get(id=pk)
    publisher = models.Books_table.objects.all()
    context = {
        "book": book,
        "publisher": publisher,
    }
    return render(request, "main/block2.html", context)


def add_book(request):
    book_form = Bookform()
    context = {"book_form": book_form}
    if request.method == "POST":
        form = Bookform(request.POST)
        if form.is_valid():
            form.save()
            return redirect("root")

    return render(request, "main/bookForm.html", context)


def edit(request, pk):
    books = models.Books_table.objects.get(id=pk)
    book_form = Bookform(instance=books)
    context = {"book_form": book_form}
    if request.method == "POST":
        form = Bookform(request.POST, instance=books)
        if form.is_valid():
            form.save()
            return redirect("root")

    return render(request, "main/bookForm.html", context)


def delete(request, pk):
    books = models.Books_table.objects.get(id=pk)
    books.delete()
    return redirect("root")


# Create your views here.
