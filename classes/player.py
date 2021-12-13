# from ..utils.constant import NB_OF_PLAYERS

class Player(object):

  def __init__(self):
    self._name = 'Player'
    self._score = 0

  def _get_name(self):
    return self._name
  
  def _set_name(self, new_name):
    self._name = new_name
  
  def _get_score(self):
    return self._score
  
  def _set_score(self, new_score):
    self._score = new_score
  
  name = property(_get_name, _set_name, _get_score, _set_score)

def initialize_players():
  players_list = []
  for i in range(2): # replace 2 by NB_OF_PLAYERS
    player = Player()
    print('Vous êtes le joueur numéro ', i+1,', veuillez entrer votre nom : ')
    player_name = input()
    player._set_name(player_name)
    players_list.append(player)
  for player in players_list:
    print('name : ', player._name, ', score : ', player._score)

initialize_players()