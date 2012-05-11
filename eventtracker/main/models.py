from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

class Place(models.Model):
    name = models.CharField(max_length=50)

class Title(models.Model):
    name = models.CharField(max_length=50)

class Event(models.Model):
    name = models.CharField(max_length=50)
