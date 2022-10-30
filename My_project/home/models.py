from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FavBooks(models.Model):
    user = models.CharField(max_length=100, null=False, blank=False)
    btitle = models.CharField(max_length=100, null=True, blank=True)
    isbn = models.IntegerField(null = False, blank = False)
    author = models.CharField(max_length=100, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    thumb = models.CharField(max_length=1000, null=True, blank=True)


    def __str__(self):
        return self.btitle

    class Meta:
        verbose_name_plural = "Favorite Books"