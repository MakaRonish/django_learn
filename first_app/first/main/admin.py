from django.contrib import admin
from . import models

admin.site.register(models.Books_table)
admin.site.register(models.Publisher)

# Register your models here.
