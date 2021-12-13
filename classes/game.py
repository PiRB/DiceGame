from methods import roll_dice_set, analyse_score, no_value_dices

class Game:

  def start_game(players):
    user_result = analyse_score(roll_dice_set(5))
    user_lose = False
    roll_again = False
    user_no_scored_values = no_value_dices(user_result["occurences"])
    print('Tu veux relancer ? y/n')
    user_input = input()
    if user_input == 'y':
      roll_again = True
    else:
      roll_again = False
    while user_lose == False or len(user_no_scored_values) > 0 and roll_again == True:
      user_result = analyse_score(roll_dice_set(len(user_no_scored_values)))

