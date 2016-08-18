from __future__ import unicode_literals

from django.db import models

class Room(models.Model):
  name = models.CharField(max_length=100)
  num_players = models.IntegerField(min_value=5, max_value=10)
  state = models.IntegerField()
  created_at_date = models.DateTimeField()
  updated_at_date = models.DateTimeField()

class Player(models.Model):
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  token = models.CharField(max_length=10)
  character = models.IntegerField()
  created_at_date = models.DateTimeField()

