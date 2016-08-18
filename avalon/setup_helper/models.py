from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Room(models.Model):
  name = models.CharField(max_length=100)
  num_players = models.IntegerField()
  state = models.IntegerField()
  created_at_date = models.DateTimeField()
  updated_at_date = models.DateTimeField()

  def __str__(self):
    return self.name

@python_2_unicode_compatible
class Player(models.Model):
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  token = models.CharField(max_length=10)
  character = models.IntegerField()
  created_at_date = models.DateTimeField()

  def __str__(self):
    return self.name

