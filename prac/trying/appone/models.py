from django.db import models
import uuid


class database(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self) -> str:
        return self.title


# Create your models here.
