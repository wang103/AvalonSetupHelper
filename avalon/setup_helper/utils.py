from enum import Enum

PLAYER_NUMBER_SETUP = {
  5:  (3, 2),
  6:  (4, 2),
  7:  (4, 3),
  8:  (5, 3),
  9:  (6, 3),
  10: (6, 4),
}

class RoomState(Enum):
  new       = 1
  full      = 2
  abandoned = 3

class Character(Enum):
  merlin          = 1
  percival        = 2
  loyal_servant_1 = 3
  loyal_servant_2 = 4
  loyal_servant_3 = 5
  loyal_servant_4 = 6
  loyal_servant_5 = 7
  assasin         = 8
  mordred         = 9
  morgana         = 10
  oberon          = 11
  minion_1        = 12
  minion_2        = 13
  minion_3        = 14

def is_character_included(bit_vector, character):
  return ((bit_vector >> character.value) & 1) != 0

def mark_char_as_included(bit_vector, character):
  return bit_vector | (1 << character.value)

def all_avail_characters(bit_vector):
  chars = []
  for c in Character:
    if is_character_included(bit_vector, c):
      chars.append(c.name)
  return ', '.join(chars)

def gather_player_knowledge(players, p):
  knowledge = []
  if p.character == Character.merlin.value:
    for player in players:
      if player.character >= 8 and player.character != 9:
        knowledge.append("%s is on the evil side." % (player.name))

  elif p.character == Character.percival.value:
    for player in players:
      if player.character == 1 or player.character == 10:
        knowledge.append("%s is Merlin." % (player.name))

  elif p.character >= 8 and p.character != 11:
    for player in players:
      if player.character >= 8 and player.character != 11 and player.character != p.character:
        knowledge.append("%s is on your (evil) side." % (player.name))

  return knowledge

