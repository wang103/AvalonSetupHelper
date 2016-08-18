from django.http import HttpResponse
from django.template import loader

from .models import Room, Player
from .utils import Character, RoomState

# Home page, lists all rooms in the READY_TO_JOIN state.
def index(request):
  available_rooms = Room.objects.filter(state=RoomState.new.value).order_by('-updated_at_date')
  
  template = loader.get_template('setup_helper/index.html')
  context = {
    'available_rooms': available_rooms,
  }

  return HttpResponse(template.render(context, request))

# The page player sees before player joins the room.
def room_info_before_join(request, room_id):
  return HttpResponse("stub")

# An action to join a room.
def join_room(request, room_id):
  return HttpResponse("stub")

# The page player sees after player joins the room.
def room_info_after_join(requset, room_id, player_token):
  return HttpResponse("stub")


# Host page, show form to create a new room.
def host(request):
  return HttpResponse("You're looking at creating a new room")

# An action to create a new room.
def create_room(request):
  return HttpResponse("stub")

