import random

NB_DICE_SIDE = 6  # Nb of side of the Dices
SCORING_DICE_VALUE_LIST = [1, 5]  # List of the side values of the dice who trigger a standard score
SCORING_MULTIPLIER_LIST = [100, 50]  # List of multiplier for standard score

THRESHOLD_BONUS = 3  # Threshold of the triggering for bonus in term of occurrence of the same slide value
STD_BONUS_MULTIPLIER = 100  # Standard multiplier for bonus
ACE_BONUS_MULTIPLIER = 1000  # Special multiplier for aces bonus

NB_DICE_TO_ROLL = 5

NB_OF_PLAYERS = 2
SCORE_TO_WIN = 1000

# Stats
MAX_TURN_SCORING = { 'player': '', 'score': 0}
LONGUEST_TURN = { 'player': '', 'roll': 0}
MAX_TURN_LOSS = { 'player': '', 'score': 0}
MEAN_SCORING_TURN = []
MEAN_NO_SCORING_TURN = []

# return a list of dices value occurrence for a roll of nb_dice_to_roll dices
def roll_dice_set(nb_dice_to_roll):
    dice_value_occurrence_list = [0] * NB_DICE_SIDE
    for n in range(nb_dice_to_roll):
      dice_value = random.randint(1, NB_DICE_SIDE)
      dice_value_occurrence_list[dice_value - 1] += 1

    return dice_value_occurrence_list


def analyse_bonus_score(dice_value_occurrence_list):
    score = 0
    for side_value_index, dice_value_occurrence in enumerate(dice_value_occurrence_list):
        nb_of_bonus = dice_value_occurrence // THRESHOLD_BONUS
        if nb_of_bonus > 0:
            if side_value_index == 0:
                bonus_multiplier = ACE_BONUS_MULTIPLIER
            else:
                bonus_multiplier = STD_BONUS_MULTIPLIER
            score += nb_of_bonus * bonus_multiplier * (side_value_index + 1)
            dice_value_occurrence_list[side_value_index] %= THRESHOLD_BONUS

    return score, dice_value_occurrence_list


def analyse_standard_score(dice_value_occurrence_list):
    score = 0
    for scoring_value, scoring_multiplier in zip(SCORING_DICE_VALUE_LIST, SCORING_MULTIPLIER_LIST):
        score += dice_value_occurrence_list[scoring_value - 1] * scoring_multiplier
        dice_value_occurrence_list[scoring_value - 1] = 0

    return score, dice_value_occurrence_list


def analyse_score(dice_value_occurrence_list):
  bonus_score, dice_value_occurrence_list = analyse_bonus_score(dice_value_occurrence_list)
  standard_score, dice_value_occurrence_list = analyse_standard_score(dice_value_occurrence_list)

  return bonus_score + standard_score, dice_value_occurrence_list, bonus_score, standard_score

def initialize_players():
  players_list = []
  for i in range(NB_OF_PLAYERS):
    player_name = input(f"Entrez votre nom joueur {i+1}: ")
    players_list.append({'name': player_name, 'score': 0, 'turn': 1, 'nb_roll': 0, 'nb_bonus': 0})

  return players_list

def get_score(player):
  return player.get('score')

def sort_players(players_list):
  players_list.sort(key=get_score, reverse=True)
  return players_list

def hasWon(player):
  if player['score'] >= SCORE_TO_WIN:
    print(f"La partie est finie, {player['name']} a atteint ou dépassé les {SCORE_TO_WIN} points")
    return True
  else:
    return False

def get_scoring_dice(nb_dice_to_reroll):
  return NB_DICE_TO_ROLL - nb_dice_to_reroll

def get_number_of_bonus(player_roll, player):
  bonus_score = player_roll[2]
  if bonus_score > 0:
    player['nb_bonus'] += 1
  return player['nb_bonus']

def set_highest_number_of_turn(player, highest_nb_turn):
  if player['turn'] >= highest_nb_turn:
    highest_nb_turn = player['turn']
  return highest_nb_turn

def play_turn(player, highest_nb_turn):
  nb_roll, isRerolling = 1, True
  player_roll = analyse_score(roll_dice_set(NB_DICE_TO_ROLL))
  player['score'] += player_roll[0]
  get_number_of_bonus(player_roll, player)
  player['turn'] += 1
  highest_nb_turn = set_highest_number_of_turn(player, highest_nb_turn)
  print(f"roll #{nb_roll} : scoring {player_roll[0]} vous avez maintenant {player['score']}")

  nb_dice_to_reroll = sum(player_roll[1])
  MEAN_SCORING_TURN.append(player_roll[0])

  if player_roll[0] > MAX_TURN_SCORING['score']: 
    MAX_TURN_SCORING['player'] = player['name']
    MAX_TURN_SCORING['score'] = player_roll[0]
  if nb_dice_to_reroll == 0:
    isRerolling = False
    print("Vous n'avez plus de dés pour jouer, c'est au joueur suivant")
  
  while isRerolling and nb_dice_to_reroll != 0:
    new_nb_dice_to_reroll = 0
    print(f"Voulez-vous relancer les {nb_dice_to_reroll} dé(s) restant(s) ( y/n )")
    reroll_response = input()
    if reroll_response == 'y':
      nb_roll +=1
      if nb_roll > LONGUEST_TURN['roll']:
        LONGUEST_TURN['player'] = player['name']
        LONGUEST_TURN['roll'] = nb_roll

      player_roll = analyse_score(roll_dice_set(nb_dice_to_reroll))
      player['score'] += player_roll[0]
      print()
      print(f"roll #{nb_roll} : scoring {player_roll[0]} avec {get_scoring_dice(nb_dice_to_reroll)} dé(s), vous avez maintenant : {player['score']}")
      new_nb_dice_to_reroll = sum(player_roll[1])
      player['nb_roll'] += nb_roll

    if reroll_response != 'y':
      print()
      print("Vous avez décidé de ne pas rejouer, c'est au joueur suivant")
      isRerolling = False

    if nb_dice_to_reroll == new_nb_dice_to_reroll:
      print("Vous n'avez pas marqué sur votre nouveau lancé, CHEH !")
      print()
      MEAN_NO_SCORING_TURN.append(player_roll[0])
      if player_roll[0] > MAX_TURN_LOSS['score']: 
        MAX_TURN_LOSS['player'] = player['name']
        MAX_TURN_LOSS['score'] = player_roll[0]
      player['score'] = 0
      break

    nb_dice_to_reroll = new_nb_dice_to_reroll

  return player['score'], highest_nb_turn

def display_turn_finished(players_list):
  players_list = sort_players(players_list)

def main():
  turn_count = 1
  isFinished = False
  players_list = initialize_players()
  highest_nb_turn = 0

  while isFinished == False:
    for index, player in enumerate(players_list):

      print("turn #",player['turn']+1, "--->", player['name'], "rank #",index+1 ,",score:", player['score'],"points")
      return_of_play_turn = play_turn(player, highest_nb_turn)

      
      if return_of_play_turn[0] != 0:
        player['score'] = return_of_play_turn[0]

      isFinished = hasWon(player)
      if isFinished:
        break
    
    sorted_players = sort_players(players_list)
    print("Classement: ")
    for index, player in enumerate(sorted_players):
      print(f"-{index+1} {player['name']} a un score de: {player['score']}")

  print()
  print(f"Game in {return_of_play_turn[1]} turns")
  players_list = sort_players(players_list)
  for player in players_list:
    if player['score'] >= SCORE_TO_WIN:
      print(f"{player['name']} WIN ! scoring {player['score']} points avec {player['nb_bonus']} bonus, en {player['turn']} tours roll {player['nb_roll']}")
    else:
      print(f"{player['name']} LOSE ! scoring {player['score']} points avec {player['nb_bonus']} bonus, en {player['turn']} tours roll {player['nb_roll']}")
  
  print("\n---- STATS ----")
  print(f"Max turn scoring : {MAX_TURN_SCORING['player']} with {MAX_TURN_SCORING['score']}")
  print(f"Longest turn : {LONGUEST_TURN['player']} with {LONGUEST_TURN['roll']}")
  print(f"Max turn loss : {MAX_TURN_LOSS['player']} with {MAX_TURN_LOSS['score']}")

  print(f"\nMean scoring turn : {sum(MEAN_SCORING_TURN) / len(MEAN_SCORING_TURN)}")
  print(f"Mean non scoring turn : {sum(MEAN_NO_SCORING_TURN) / len(MEAN_NO_SCORING_TURN)}")
  return 0

main()
