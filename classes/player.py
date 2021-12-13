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
  
  name = property(_get_name, _set_name)
  oui