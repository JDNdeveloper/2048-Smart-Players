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
      return (copy.deepcopy(self.board), self.score)

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
         line = [self.board[row][col] for (row, col) in linePositions]         
         cLine = []
         prevVal = None
         for val in line:
            if val is None:
               continue
            if val == prevVal:
               newVal = 2 * val
               cLine[-1] = newVal
               self.score += newVal
               prevVal = None
            else:
               cLine.append(val)
               prevVal = val
         # pad with "None's" at the end if needed
         cLine.extend([None] * (len(line) - len(cLine)))

         if line != cLine:
            # if line changed, update the row in the board
            boardChanged[0] = True
            for ((row, col), newVal) in zip(linePositions, cLine):
               self.board[row][col] = newVal

      pos = range(self.SIZE)
      rPos = list(reversed(pos))

      if move in [Move.UP, Move.DOWN]:
         for col in range(self.SIZE):
            if move == Move.UP:
               rows = pos
            elif move == Move.DOWN:
               rows = rPos
            compressLine(zip(rows, [col] * self.SIZE))
      elif move in [Move.LEFT, Move.RIGHT]:
         for row in range(self.SIZE):
            if move == Move.LEFT:
               cols = pos
            elif move == Move.RIGHT:
               cols = rPos
            compressLine(zip([row] * self.SIZE, cols))

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
