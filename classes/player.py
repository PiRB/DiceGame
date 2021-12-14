# from ..utils.constant import NB_OF_PLAYERS
from methods import roll_dice_set, analyse_score

class Player(object):

  def __init__(self, name):
    self._name = name
    self._score = 0

  def _get_name(self):
    return self._name
  
  def _set_name(self, new_name):
    self._name = new_name
  
  def _get_score(self):
    return self._score
  
  def _set_score(self, new_score):
    self._score = new_score

  def _play_turn(self):
    user_result = analyse_score(roll_dice_set(5))
    sum_occurrences = sum(user_result['occurrences'])
    can_roll_dices = self._reroll()
    score = user_result['score']
    user_lose = False
    while can_roll_dices and sum_occurrences > 0:
      reroll_result = analyse_score(roll_dice_set(sum_occurrences))
      sum_reroll_occurrences = sum(reroll_result['occurrences'])
      if sum_occurrences == sum_reroll_occurrences:
        score = 0
        user_lose = True
        break
      sum_occurrences = sum_reroll_occurrences
      score += reroll_result['score']
      can_roll_dices = self._reroll()
    self._set_score(score)

    
  def _reroll(self):
    print('Tu veux relancer ? y/n')
    user_input = input()
    roll_again = False
    if user_input == 'y':
      roll_again = True
    elif user_input == 'n':
      roll_again = False
    else:
      self._reroll()
    return roll_again
  
  name = property(_get_name, _set_name, _get_score, _set_score)
