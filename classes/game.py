from classes.player import Player
from constant import *

class Game:

  def __init__(self):
    self._isFinished = False

  def _initialize_players(self):
    players_list = []
    for i in range(NB_OF_PLAYERS): # replace 2 by NB_OF_PLAYERS
      print('Vous êtes le joueur numéro ', i + 1,', veuillez entrer votre nom : ')
      player_name = input()
      player = Player(player_name)
      players_list.append(player)
      print('------------------------------------')
      print()
    """ for player in players_list:
      print('name : ', player._name, ', score : ', player._score) """
    return players_list

  def _start_game(self):
    players = self._initialize_players()
    max_player_score = 0
    lap_index = 1
    while MAX_SCORE_LIMIT > max_player_score:
      for player in players:
        print("%s c'est à toi: " % (player._get_name()))
        print('------------------------------------')
        print()
        player._play_turn()
        if max_player_score < player._get_score():
          max_player_score = player._get_score()
        print('Joueur %s || score: %s' % (player._get_name(), player._get_score()))
        print('------------------------------------')
        print()
      print('Tour %s terminé, voici le classement' % (lap_index))
      players_sorted = players
      players_sorted.sort(key=lambda x: x._get_score(), reverse=True)
      for index, player in enumerate(players_sorted):
        print('%s --> %s || score: %s' % (index + 1, player._get_name(), player._get_score()))   
      print()
      print('------------------------------------')
      lap_index += 1
