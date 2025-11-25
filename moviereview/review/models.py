from django.db import models

# Create your models here.

class movie_details(models.Model):
    movie_name=models.CharField(max_length=100,unique=True)
    release_date=models.CharField(max_length=100)
    budget=models.CharField(max_length=100)
    rating = models.CharField(max_length=10)
