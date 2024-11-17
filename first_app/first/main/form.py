from django.forms import ValidationError
from django.forms import ModelForm
from . import models
import datetime


class Bookform(ModelForm):
    class Meta:
        model = models.Books_table
        fields = ["title", "description", "price", "publication_date", "publisher"]


class Publisherform(ModelForm):
    class Meta:
        model = models.Publisher
        fields = ["name", "website", "contact_email"]
