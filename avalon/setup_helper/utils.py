from enum import Enum

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

