from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
    User
)

class Tag(models.Model):
    title = models.CharField(max_length=512, unique=True)

    def __str__(self):
        return self.title


class Snippet(models.Model):
    title = models.CharField(max_length=512)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
