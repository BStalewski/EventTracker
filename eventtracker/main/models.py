from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

class Place(models.Model):
    url = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

class Style(models.Model):
    style = models.CharField(max_length=30)

class Event(models.Model):
    place = models.ForeignKey(Place)
    title = models.CharField(max_length=50)
    start_date = models.DateField()
    duration = models.IntegerField()
