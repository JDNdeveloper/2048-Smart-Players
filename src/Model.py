import copy
import random

class Move:
   UP = 1
   DOWN = 2
   LEFT = 3
   RIGHT = 4

class Model(object):
   """Board is 4x4."""
   SIZE = 4
   """Fill values, using value repetition as a probability distribution"""
   FILL_VALUES = [2] * 9 + [4] * 1

   def __init__(self):
      self.board = None
      self.score = None
      self.reset()

   def getState(self):
      """Retrieves current state.

      Returns:
      (board, score): Current board and score.
      """
      return (self.board, self.score)

   def makeMove(self, move):
      """Executes a move.

      Args:
      move: The move to execute.
      """
      boardChanged = [False]

      # execute the move
      def compressLine(linePositions):
         """Compresses line to the left.

         Sets boardChanged to True if compressed line is different
         than original line.

         Args:
         linePositions: List of (row, col) position indices.
         """
         # attempt to compress to the left
         index = 0
         prevVal = None
         for (row, col) in linePositions:
            val = self.board[row][col]

            if val is None:
               continue

            if val == prevVal:
               index -= 1
               newVal = 2 * val
               self.score += newVal
               prevVal = None
            else:
               newVal = val
               prevVal = val

            (newRow, newCol) = linePositions[index]
            if self.board[newRow][newCol] != newVal:
               boardChanged[0] = True
               self.board[newRow][newCol] = newVal

            index += 1

         # pad with "None's" at the end if needed
         while index < self.SIZE:
            (newRow, newCol) = linePositions[index]
            self.board[newRow][newCol] = None
            index += 1

      if move in [Move.UP, Move.LEFT]:
         lineIndices = range(self.SIZE)
      elif move in [Move.DOWN, Move.RIGHT]:
         lineIndices = list(reversed(range(self.SIZE)))

      if move in [Move.UP, Move.DOWN]:
         for col in range(self.SIZE):
            compressLine(zip(lineIndices, [col] * self.SIZE))
      elif move in [Move.LEFT, Move.RIGHT]:
         for row in range(self.SIZE):
            compressLine(zip([row] * self.SIZE, lineIndices))

      # if the move actually changed the game board,
      # we do a random fill
      if boardChanged[0]:
         self._randomFill()

   def isGameOver(self):
      """True if game is over."""
      if len(self._getOpenPositions()) > 0:
         return False

      for i in range(self.SIZE):
         # check for consecutive numbers in all rows and cols
         prevRowVal = None
         prevColVal = None
         for j in range(self.SIZE):
            # check row
            val = self.board[i][j]
            if val == prevRowVal:
               return False
            else:
               prevRowVal = val

            # check col
            val = self.board[j][i]
            if val == prevColVal:
               return False
            else:
               prevColVal = val

      return True

   def maxTile(self):
      """Returns value of maximum tile on the board."""
      return max(val for row in self.board for val in row)

   def reset(self):
      """Resets the game."""
      self.board = [[None] * self.SIZE for _ in range(self.SIZE)]
      self.score = 0

      # add the initial two tiles
      self._randomFill()
      self._randomFill()

   def _getOpenPositions(self):
      """Retrieve open positions.

      Returns:
      openPositions: List of open (row, col) positions.
      """
      return [(row, col) for row in range(self.SIZE) for col in range(self.SIZE)
              if self.board[row][col] == None]

   def _randomFill(self):
      """Randomly fill an open position on the board.

      The fill values and probability distribution is defined above.
      """
      (row, col) = random.choice(self._getOpenPositions())
      self.board[row][col] = random.choice(self.FILL_VALUES)

   def __str__(self):
      """Return string representation of the board."""
      s = ''
      for row in range(self.SIZE):
         for col in range(self.SIZE):
            val = self.board[row][col]
            s += '%s\t' % str(val if val is not None else 0)
         s += '\n'
      return s
