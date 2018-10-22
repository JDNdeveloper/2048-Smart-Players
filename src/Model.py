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
   """Fill values, using value repetition as a probability distribution."""
   FILL_VALUES = [2] * 9 + [4] * 1
   """All possible moves."""
   MOVES = (Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT)

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

   def makeMove(self, move, modifyState=True):
      """Executes a move.

      Args:
      move: The move to execute.
      modifyState: If False the board and score are not updated with the move.

      Returns:
      moveScore: The points made from the given move.
      boardChanged: True if the move would/did make the board change.
      """
      boardChanged = False
      moveScore = 0

      # execute the move
      def compressLine(linePositions):
         """Compresses line to the left.

         Sets boardChanged to True if compressed line is different
         than original line.

         Args:
         linePositions: List of (row, col) position indices.

         Returns:
         lineScore: The points made from compressing this line.
         lineChanged: True if move would/did make the line change.
         """
         # attempt to compress to the left
         lineScore = 0
         lineChanged = False
         index = 0
         prevVal = None
         for (row, col) in linePositions:
            val = self.board[row][col]

            if val is None:
               continue

            if val == prevVal:
               index -= 1
               newVal = 2 * val
               lineScore += newVal
               prevVal = None
            else:
               newVal = val
               prevVal = val

            (newRow, newCol) = linePositions[index]
            if self.board[newRow][newCol] != newVal:
               lineChanged = True
               if modifyState:
                  self.board[newRow][newCol] = newVal

            index += 1

         # pad with "None's" at the end if needed
         while index < self.SIZE:
            (newRow, newCol) = linePositions[index]
            if modifyState:
               self.board[newRow][newCol] = None
            index += 1

         return (lineScore, lineChanged)

      if move in [Move.UP, Move.LEFT]:
         lineIndices = range(self.SIZE)
      elif move in [Move.DOWN, Move.RIGHT]:
         lineIndices = list(reversed(range(self.SIZE)))

      if move in [Move.UP, Move.DOWN]:
         for col in range(self.SIZE):
            (lineScore, lineChanged) = compressLine(
               zip(lineIndices, [col] * self.SIZE))
            moveScore += lineScore
            if lineChanged:
               boardChanged = True
      elif move in [Move.LEFT, Move.RIGHT]:
         for row in range(self.SIZE):
            (lineScore, lineChanged) = compressLine(
               zip([row] * self.SIZE, lineIndices))
            moveScore += lineScore
            if lineChanged:
               boardChanged = True

      if modifyState:
         if boardChanged:
            # if the move actually changed the game board,
            # we do a random fill
            self._randomFill()
         self.score += moveScore

      return (moveScore, boardChanged)

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
      rowBreak = '---------------------------------\n'

      s = ''
      for row in range(self.SIZE):
         s += rowBreak
         for col in range(self.SIZE):
            val = self.board[row][col]
            s += '| %s\t' % str(val if val is not None else '')
         s += '|\n'
      s += rowBreak
      return s
