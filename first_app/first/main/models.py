from django.db import models
import uuid
import datetime


# Create your models here.
class Books_table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    publication_date = models.DateField(default=datetime.date.today)
    is_available = models.BooleanField(default=True)
    publisher = models.ForeignKey(
        "Publisher", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.title


class Publisher(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=50)
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name
