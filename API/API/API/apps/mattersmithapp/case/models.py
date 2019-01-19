from __future__ import unicode_literals

from django.db import models

# Create your models here.
class case(models.Model):
    name=models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)