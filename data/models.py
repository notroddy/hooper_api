from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    url = models.URLField()