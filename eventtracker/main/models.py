from django.db import models

# Create your models here.
class Url_json(models.Model):
    url   = models.CharField(max_length=100)
    json  = models.CharField(max_length=300)

class Obiekt(models.Model):
    pole1 = models.CharField(max_length=50)
    pole2 = models.CharField(max_length=50,blank=True)
    pole3 = models.CharField(max_length=50,blank=True)
    pole4 = models.CharField(max_length=50,blank=True)
    pole5 = models.CharField(max_length=50,blank=True)
    pole6 = models.CharField(max_length=50,blank=True)
    url   = models.CharField(max_length=100,blank=True)

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
