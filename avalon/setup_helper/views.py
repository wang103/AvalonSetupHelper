from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils import timezone
from random import choice
from string import ascii_letters

from .models import Room, Player
from .utils import *


# Home page, lists all rooms in the READY_TO_JOIN state.
def index(request):
  available_rooms = Room.objects.filter(state=RoomState.new.value).order_by('-created_at_date')
  
  context = {
    'available_rooms': available_rooms,
  }

  return render(request, 'setup_helper/index.html', context)


# The page player sees before player joins the room.
def room_info_before_join(request, room_id):
  try:
    room = Room.objects.get(pk=room_id)
  except Room.DoesNotExist:
    raise Http404("Room does not exist")

  context = {
    'room': room,
  }

  return render(request, 'setup_helper/room_info_before_join.html', context)


# An action to join a room.
def join_room(request, room_id):
  try:
    with transaction.atomic():
      room = Room.objects.select_for_update().get(pk=room_id)

      passcode = request.POST['passcode']
      player_name = request.POST['player_name']

      error_message = ""

      # Check for passcode
      if passcode != room.passcode:
        error_message = "Wrong passcode"

      # Check of player name
      if not player_name:
        error_message = "Invalid player name"

      # Check for max number of players
      existing_players = room.player_set.all()
      num_existing_players = existing_players.count()
      if num_existing_players >= room.num_players:
        error_message = "Room is full"

      if error_message != "":
        return render(request, 'setup_helper/error.html', { 'error_message': error_message })

      # All good.

      # Generate a random token for this player.
      existing_tokens = [x.token for x in existing_players]
      while True:
        token = ''.join(choice(ascii_letters) for i in range(10))
        if token not in existing_tokens:
          break

      # Randomly pick a character for this player.
      char_candidates = set()
      existing_chars = [Character(x.character) for x in existing_players]
      chars_bit_vector = room.characters_vector
      for c in Character:
        if is_character_included(chars_bit_vector, c) and c not in existing_chars:
          char_candidates.add(c)
      character = choice(char_candidates)

      player = Player(
        room=room,
        name=player_name,
        token=token,
        character=character.value,
        created_at_date=timezone.now()
      )
      player.save()

      # Update room state if needed.
      if num_existing_players + 1 >= room.num_players:
        room.state = RoomState.full.value
        room.save()



  except Exception:
    raise Http404("Something went wrong")


# The page player sees after player joins the room.
def room_info_after_join(requset, room_id, player_token):
  return HttpResponse("stub")



# Host page, show form to create a new room.
def host(request):
  return HttpResponse("You're looking at creating a new room")


# An action to create a new room.
def create_room(request):
  return HttpResponse("stub")

