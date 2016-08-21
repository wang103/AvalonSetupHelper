from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
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
      if not player_name and not error_message:
        error_message = "Invalid player name"

      # Check for max number of players
      existing_players = room.player_set.all()
      num_existing_players = existing_players.count()
      if num_existing_players >= room.num_players and not error_message:
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
      char_candidates = []
      existing_chars = [Character(x.character) for x in existing_players]
      chars_bit_vector = room.characters_vector
      for c in Character:
        if is_character_included(chars_bit_vector, c) and c not in existing_chars:
          char_candidates.append(c)
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

      return HttpResponseRedirect(reverse('setup_helper:room_info_after_join', args=(room.id, player.token)))

  except Exception as e:
    raise Http404("Something went wrong: %s" % (e.message))


# The page player sees after player joins the room.
def room_info_after_join(request, room_id, player_token):
  try:
    room = Room.objects.get(pk=room_id)
  except Room.DoesNotExist:
    raise Http404("Room does not exist")

  try:
    player = Player.objects.get(room=room, token=player_token)
  except Player.DoesNotExist:
    raise Http404("Player does not exist in the room")

  existing_players = room.player_set.all()
  num_existing_players = existing_players.count()

  context = {
    'room': room,
    'num_good': PLAYER_NUMBER_SETUP[room.num_players][0],
    'num_evil': PLAYER_NUMBER_SETUP[room.num_players][1],
    'num_existing_players': num_existing_players,
    'available_chars': all_avail_characters(room.characters_vector),
  }

  # If the game is ready to go, add player info to the context.
  if room.state == RoomState.full.value:
    context['player'] = player
    context['character'] = Character(player.character).name
    context['knowledge'] = gather_player_knowledge(existing_players, player)

  return render(request, 'setup_helper/room_info_after_join.html', context)



# Host page, show form to create a new room.
def host(request):
  context = {}
  return render(request, 'setup_helper/host.html', context)


# An action to create a new room.
def create_room(request):
  room_name = request.POST['room_name']
  passcode = request.POST['passcode']
  num_players_str = request.POST['num_players']
  characters = request.POST.getlist('characters[]')

  error_message = ""

  if not room_name:
    error_message = "Invalid room name"

  if not passcode and not error_message:
    error_message = "Invalid passcode"

  try:
    num_players = int(num_players_str)
  except ValueError:
    if not error_message:
      error_message = "Invalid number of players"

  if (num_players < 5 or num_players > 10) and not error_message:
    error_message = "Invalid number of players"

  if len(characters) != num_players and not error_message:
    error_message = "Incorrect number of characters"

  num_good = PLAYER_NUMBER_SETUP[num_players][0]
  num_evil = PLAYER_NUMBER_SETUP[num_players][1]

  # Convert characters array into actual Character object array.
  chars = [Character(int(c_str)) for c_str in characters]

  actual_num_good = num_good_characters(chars)
  if actual_num_good != num_good and not error_message:
    error_message = "Incorrect divide between good and evil"

  # Convert Character object array into bit vector.
  bit_vector = convert_to_bit_vector(chars)

  # In all games, make sure Merlin is included.
  if not is_character_included(bit_vector, Character.merlin) and not error_message:
    error_message = "Merlin must be included"

  # In all games, make sure Assasin is included.
  if not is_character_included(bit_vector, Character.assasin) and not error_message:
    error_message = "Assasin must be included"

  # In games of 5, if Percival is included, make sure Mordred or Morgana is included.
  if num_players == 5 and is_character_included(bit_vector, Character.percival) and not error_message:
    if not is_character_included(bit_vector, Character.mordred) and \
       not is_character_included(bit_vector, Character.morgana):
       error_message = "For game of 5 with Percival, must include Mordred or Morgana"

  if error_message != "":
    return render(request, 'setup_helper/error.html', { 'error_message': error_message })

  # All good.

  room = Room(
    name=room_name,
    passcode=passcode,
    num_players=num_players,
    state=RoomState.new.value,
    characters_vector=bit_vector,
    created_at_date=timezone.now()
  )
  room.save()

  return HttpResponseRedirect(reverse('setup_helper:index', args=()))

