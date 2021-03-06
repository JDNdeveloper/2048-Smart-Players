import copy
import random

DEFAULT_SIZE = 4

class Move:
   UP = 1
   DOWN = 2
   LEFT = 3
   RIGHT = 4

class Model(object):
   """Board is 4x4."""
   SIZE = DEFAULT_SIZE
   """Fill values, using value repetition as a probability distribution."""
   FILL_VALUES = [2] * 9 + [4] * 1
   """All possible moves."""
   MOVES = (Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT)
   MOVE_NAMES = ('', 'UP', 'DOWN', 'LEFT', 'RIGHT')

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

   @staticmethod
   def makeBoardMove(board, move, modifyState=True, returnBoard=False):
      """Executes a move.

      Args:
      move: The move to execute.
      modifyState: If False the board is not updated with the move.
      returnBoard: Also returns the new board.

      Returns:
      moveScore: The points made from the given move.
      boardChanged: True if the move would/did make the board change.
      (optional) newBoard: Board with the move performed.
      """
      boardChanged = False
      moveScore = 0

      assert move in Model.MOVES

      if move == Move.UP:
         allRowColPairs = [zip(range(Model.SIZE), [i] * Model.SIZE)
                           for i in range(Model.SIZE)]
      elif move == Move.DOWN:
         allRowColPairs = [zip(list(reversed(range(Model.SIZE))), [i] * Model.SIZE)
                           for i in range(Model.SIZE)]
      elif move == Move.LEFT:
         allRowColPairs = [zip([i] * Model.SIZE, range(Model.SIZE))
                           for i in range(Model.SIZE)]
      elif move == Move.RIGHT:
         allRowColPairs = [zip([i] * Model.SIZE, list(reversed(range(Model.SIZE))))
                           for i in range(Model.SIZE)]

      if returnBoard:
         newBoard = copy.deepcopy(board)

      for rowColPairs in allRowColPairs:
         line = [board[row][col] for (row, col) in rowColPairs]
         (newLine, lineScore) = Model._compressLine(line)
         if newLine != line:
            boardChanged = True
            moveScore += lineScore
            if modifyState:
               for (val, (row, col)) in zip(newLine, rowColPairs):
                  board[row][col] = val
            if returnBoard:
               for (val, (row, col)) in zip(newLine, rowColPairs):
                  newBoard[row][col] = val

      if returnBoard:
         return (moveScore, boardChanged, newBoard)
      return (moveScore, boardChanged)

   def makeMove(self, move):
      """Performs move on the game board, performs random fill (if board changed),
      updates score."""
      (moveScore, boardChanged) = self.makeBoardMove(
         self.board, move, modifyState=True, returnBoard=False)

      if boardChanged:
         # if the move actually changed the game board,
         # we do a random fill
         self._randomFill()

      self.score += moveScore

      return (moveScore, boardChanged)

   @staticmethod
   def getBoardNumTiles(board):
      """Returns number of tiles on the board"""
      return sum(1 for row in board for val in row if val is not None)

   def numTiles(self):
      return self.getBoardNumTiles(self.board)

   @staticmethod
   def isBoardGameOver(board):
      """True if game is over."""
      if len(Model.getBoardOpenPositions(board)) > 0:
         return False

      for i in range(Model.SIZE):
         # check for consecutive numbers in all rows and cols
         prevRowVal = None
         prevColVal = None
         for j in range(Model.SIZE):
            # check row
            val = board[i][j]
            if val == prevRowVal:
               return False
            else:
               prevRowVal = val

            # check col
            val = board[j][i]
            if val == prevColVal:
               return False
            else:
               prevColVal = val

      return True

   def isGameOver(self):
      return self.isBoardGameOver(self.board)

   @staticmethod
   def getBoardMaxTile(board):
      """Returns value of maximum tile on the board."""
      return max(val for row in board for val in row)

   def maxTile(self):
      return self.getBoardMaxTile(self.board)

   def reset(self):
      """Resets the game."""
      self.board = [[None] * self.SIZE for _ in range(self.SIZE)]
      self.score = 0

      # add the initial two tiles
      self._randomFill()
      self._randomFill()

   @staticmethod
   def _compressLine(line):
      """Compresses line to the left.

      Args:
      line: The original line.

      Returns:
      newLine: The compressed line.
      lineScore: The points made from compressing this line.
      """
      newLine = []
      lineScore = 0
      prevVal = None
      for val in line:
         if val is None:
            continue

         if val == prevVal:
            newVal = 2 * val
            newLine[-1] = newVal
            lineScore += newVal
            prevVal = None
         else:
            newLine.append(val)
            prevVal = val

      if len(newLine) < Model.SIZE:
         newLine += [None] * (Model.SIZE - len(newLine))

      return (newLine, lineScore)

   @staticmethod
   def getBoardScore(board):
      """Get sum of elements on the board"""
      return sum([sum(filter(None, row)) for row in board])

   @staticmethod
   def getBoardOpenPositions(board):
      """Retrieve open positions.

      Returns:
      openPositions: List of open (row, col) positions.
      """
      return [(row, col) for row in range(Model.SIZE) for col in range(Model.SIZE)
              if board[row][col] == None]

   @staticmethod
   def getBoardSortedValues(board):
      """Return tile values sorted in descending order"""
      return list(reversed(sorted(val for row in board for val in row)))

   @staticmethod
   def getBoardRotated(board):
      """Return board rotated clockwise by 90 degrees"""
      return [list(row) for row in zip(*board[::-1])]

   @staticmethod
   def getBoardMirrored(board):
      """Return mirrored board"""
      return [row[::-1] for row in board]

   @staticmethod
   def doBoardRandomFill(board):
      """Randomly fill an open position on the board.

      The fill values and probability distribution is defined above.
      """
      openPositions = Model.getBoardOpenPositions(board)
      if openPositions:
         (row, col) = random.choice(openPositions)
         board[row][col] = random.choice(Model.FILL_VALUES)

   def _randomFill(self):
      self.doBoardRandomFill(self.board)

   @staticmethod
   def getBoardString(board):
      """Return string representation of the board."""
      rowBreak = '--------' * Model.SIZE + '-\n'

      s = ''
      for row in range(Model.SIZE):
         s += rowBreak
         for col in range(Model.SIZE):
            val = board[row][col]
            s += '| %s\t' % str(val if val is not None else '')
         s += '|\n'
      s += rowBreak
      return s

   def __str__(self):
      return self.getBoardString(self.board)
