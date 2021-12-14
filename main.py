import random

NB_DICE_SIDE = 6  # Nb of side of the Dices
SCORING_DICE_VALUE_LIST = [1, 5]  # List of the side values of the dice who trigger a standard score
SCORING_MULTIPLIER_LIST = [100, 50]  # List of multiplier for standard score

THRESHOLD_BONUS = 3  # Threshold of the triggering for bonus in term of occurrence of the same slide value
STD_BONUS_MULTIPLIER = 100  # Standard multiplier for bonus
ACE_BONUS_MULTIPLIER = 1000  # Special multiplier for aces bonus

NB_DICE_TO_ROLL = 5

NB_OF_PLAYERS = 2
SCORE_TO_WIN = 500


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
    print('Entrez votre nom joueur ', i+1)
    player_name = input()
    start_score = 0
    player = {'name': player_name, 'score': start_score, 'turn': 1, 'nb_roll': 0, 'nb_bonus': 0}
    players_list.append(player)

  return players_list

def get_score(player):
  return player.get('score')

def sort_players(players_list):
  players_list.sort(key=get_score, reverse=True)
  return players_list

def hasWon(players_list):

  players_list = sort_players(players_list)
  
  if players_list[0]['score'] >= SCORE_TO_WIN:
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

def play_turn(player):
  nb_roll = 1
  isRerolling = True
  player_roll = analyse_score(roll_dice_set(NB_DICE_TO_ROLL))
  player['score'] += player_roll[0]
  get_number_of_bonus(player_roll, player)
  player['turn'] += 1
  print("Roll #",nb_roll ,"Vous avez scoré : ",player_roll[0], ", vous avez maintenant : ", player['score'])

  nb_dice_to_reroll = sum(player_roll[1])
  if nb_dice_to_reroll == 0:
    isRerolling = False
    print("Vous n'avez plus de dés pour jouer, c'est au joueur suivant")
  
  while isRerolling and nb_dice_to_reroll != 0:
    new_nb_dice_to_reroll = 0
    print('Voulez-vous relancer les ', nb_dice_to_reroll, ' dé(s) restant(s) ( y/n )')
    reroll_response = input()
    if reroll_response == 'y':

      nb_roll +=1
      player_roll = analyse_score(roll_dice_set(nb_dice_to_reroll))
      player['score'] += player_roll[0]
      print()
      print("Roll #",nb_roll ,"Vous avez scoré : ",player_roll[0]," avec ", get_scoring_dice(nb_dice_to_reroll), " dé(s), vous avez maintenant : ", player['score'])
      new_nb_dice_to_reroll = sum(player_roll[1])
      player['nb_roll'] += nb_roll

    if reroll_response != 'y':
      print()
      print("Vous avez décidé de ne pas rejouer, c'est au joueur suivant")
      isRerolling = False

    if nb_dice_to_reroll == new_nb_dice_to_reroll:
      print("Vous n'avez pas marqué sur votre nouveau lancé, CHEH !")
      print()
      player['score'] = 0
      break

    nb_dice_to_reroll = new_nb_dice_to_reroll

  return player['score']

def display_turn_finished(players_list):
  players_list = sort_players(players_list)

  for player in players_list:
    print(player['name'], " ==> ", player['score'])
  print()

def display_game_finished(players_list):
  players_list = sort_players(players_list)

  for i in range(len(players_list)):
    if i == 0:
      print(players_list[i]['name'], " WIN ! scoring ", players_list[i]['score'], ' points')
    else:
      print(players_list[i]['name'], " LOSE ! scoring ", players_list[i]['score'], ' points')

def main():
  turn_count = 1
  isFinished = False
  players_list = initialize_players()

  while isFinished == False:
    for index, player in enumerate(players_list):

      print("turn #",player['turn'], "--->", player['name'], "rank #",index+1 ,",score:", player['score'],"points")
      return_of_play_turn = play_turn(player)

      
      if return_of_play_turn != 0:
        player['score'] = return_of_play_turn

      isFinished = hasWon(player)
      if isFinished:
        break
    
    sorted_players = sort_players(players_list)
    print("Classement: ")
    for index, player in enumerate(sorted_players):
      print("-", index+1, player['name'] ," a un score de: ", player['score'])

  print()
  print("Voici le résultat de la partie")
  players_list = sort_players(players_list)
  for player in players_list:
    if player['score'] >= SCORE_TO_WIN:
      print(player['name'], " WIN ! scoring ", player['score'], " points avec", player['nb_bonus'] ,"bonus, en ", player['turn']," tours", "roll", player['nb_roll'])
    else:
      print(player['name'], " LOSE ! scoring ", player['score'], " points avec", player['nb_bonus'] ,"bonus, en ", player['turn']," tours", "roll", player['nb_roll'])
  return 0

main()
