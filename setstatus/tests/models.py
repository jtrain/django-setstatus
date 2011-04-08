from django.db import models

class Factory(models.Model):
    name = models.CharField(max_length=255)
