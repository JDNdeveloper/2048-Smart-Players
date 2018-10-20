import copy

class Move:
   UP = 1
   DOWN = 2
   LEFT = 3
   RIGHT = 4

class Model(object):
   """Board is 4x4."""
   SIZE = 4
   """Fill values with their probabilities."""
   FILL_VALUES = [(2, 0.9), (4, 0.1)]

   def __init__(self):
      self.board = None
      self.score = None
      self.reset()

   def reset(self):
      """Resets the game."""
      self.board = [[None] * SIZE for _ in range(SIZE)]
      self.score = 0

   def getState(self):
      """Retrieves current state.

      Returns:
      (board, score): Current board and score.
      """
      return (copy.deepcopy(self.board), self.score)

   def makeMove(self, move):
      """Executes a move.

      Args:
      move: The move to execute.
      """
      if move == Move.UP:
         pass
      elif move == Move.DOWN:
         pass
      elif move == Move.LEFT:
         pass
      elif move == Move.RIGHT:
         pass
