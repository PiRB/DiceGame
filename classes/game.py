from classes.player import Player

class Game:

  def __init__(self):
    self._isFinished = False

  def initialize_players(self):
    players_list = []
    for i in range(2): # replace 2 by NB_OF_PLAYERS
      print('Vous êtes le joueur numéro ', i+1,', veuillez entrer votre nom : ')
      player_name = input()
      player = Player(player_name)
      players_list.append(player)
      print('------------------------------------')
      print()
    """ for player in players_list:
      print('name : ', player._name, ', score : ', player._score) """
    return players_list

  def start_game(self):
    players = self.initialize_players()
    for player in players:
      print("%s c'est à toi: " % (player._get_name()))
      print('------------------------------------')
      print()
      player._play_turn()
      print('Joueur %s || score: %s' % (player._get_name(), player._get_score()))
      print('------------------------------------')
      print()

