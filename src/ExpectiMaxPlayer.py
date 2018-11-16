from Player import Player
import random
import copy

##########################################################################
# TODO: implement heuristics
##########################################################################
class ExpectiMaxPlayer(Player):
    """Plays with an expectimax algorithm"""

    def __init__(self, debug=False, depth=3):
        super(ExpectiMaxPlayer, self).__init__(debug)
        self.depth = depth
        self.legalMoves_agent = self.m.MOVES
        self.lastBoard = None
        self.lastMove = None

    def isGameOver(self, board):
        """Check if Game is over"""
        if len(self.getOpenPos(board)) > 0:
            return False
        for i in range(self.m.SIZE):
            # check for consecutive numbers in all rows and cols
            prevRowVal = None
            prevColVal = None
            for j in range(self.m.SIZE):
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

    def getScore(self, board):
        """Get Current sum of elements on the board"""
        return sum([sum(filter(None, list)) for list in board])

    def getOpenPos(self, board):
        return [(row, col) for row in range(self.m.SIZE)
                for col in range(self.m.SIZE) if board[row][col] == None]

    def randomFill(self, board, move):
        """Randomly fill an open position on the board.
        The fill values and probability distribution is defined above.
        """
        openPos = self.getOpenPos(board)
        if len(openPos) == 0: return board
        (row, col) = random.choice(openPos)
        board[row][col] = move
        return board

    def generateNextMove(self, board, index, move):
        """Simulate next move for agent or rand"""
        if index == 0:
            return (self.m.makeMove(move, modifyState=False, returnBoard=True)[2],
                    move)
        else:
            row, col = move[1]
            val = move[0]
            new_board = copy.deepcopy(board)
            new_board[row][col] = val
            return (new_board, move[0])

    def adjustLegalMoves(self, board):
        """Disallows forbidden moves"""
        if self.lastBoard == board:
            moves = list(self.legalMoves_agent)
            moves.remove(self.lastMove)
            self.legalMoves_agent = tuple(moves)
        else:
            self.lastBoard = copy.deepcopy(board)
            self.legalMoves_agent = self.m.MOVES
        return

    def maxTile(self, board):
      """Returns value of maximum tile on the board."""
      return max(val for row in board for val in row)

    def getMove(self, board, score):
        """
        Runs an expectimax algorithm to try and get the next best move
        [More to follow]
        """

        movePlayed = ['', 'UP', 'DOWN', 'LEFT', 'RIGHT']
        #######################################
        def recurse(board, index, depth):
            ###################### Base cases
            if depth == 0:
                return ("", self.evalFunction(board), index)
            if self.isGameOver(board):
                return ("", self.getScore(board), index)
            ######################
            legalMoves = (self.legalMoves_agent
                          if index == 0
                          else ([(2, pos) for pos in self.getOpenPos(board)] +
                               [(4, pos) for pos in self.getOpenPos(board)]))

            newBoards = [self.generateNextMove(board, index, move)
                         for move in legalMoves]
            if index == 0: #agent case
                moveRewards = [recurse(newBoard[0], index+1, depth)[1]
                               for newBoard in newBoards]
            else: #rand case
                moveRewards_2 = [recurse(newBoard[0], 0, depth-1)[1]
                                 for newBoard in newBoards if newBoard[1] == 2]
                moveRewards_4 = [recurse(newBoard[0], 0, depth-1)[1]
                                 for newBoard in newBoards if newBoard[1] == 4]
            if index == 0:
                maxIdx = moveRewards.index(max(moveRewards))
                return (legalMoves[maxIdx], max(moveRewards), index)
            else:
                return ("", (0.9*sum(moveRewards_2) +
                             0.1*sum(moveRewards_4))/len(moveRewards_2), index)
            assert False

        #######################################
        self.adjustLegalMoves(board)
        bestMove = recurse(self.m.getState()[0], 0, self.depth)
        self.lastMove = bestMove[0]
        if self.debug:
            print "BestMove: {}".format(movePlayed[bestMove[0]])
            self.printBoard(board)
        return self.lastMove

    def evalFunction(self, board): #Todo
        score = self.getScore(board)
        numNone = len(self.getOpenPos(board))**2
        maxTilePosCorrect = 100 if self.maxTile(board) == board[0][0] else -10
        maxTileColCorrect = 10 if self.maxTile(board) in board[0] else 0
        topRowDecreasing = sum([(len(board[0]) - i)*10 for i in range(len(board[0]))
                                if board[0][i] > board[0][(i+1)%len(board[0])]])
        phi = [score, numNone, maxTilePosCorrect, maxTileColCorrect,
               topRowDecreasing]
        weights = [0, 1.4, 2, 0, 2]
        return sum([weights[i]*phi[i] for i in range(len(phi))])

    def printBoard(self, board):
      """Return string representation of the board."""
      rowBreak = '--------' * self.m.SIZE + '-\n'

      s = ''
      for row in range(self.m.SIZE):
         s += rowBreak
         for col in range(self.m.SIZE):
            val = board[row][col]
            s += '| %s\t' % str(val if val is not None else '')
         s += '|\n'
      s += rowBreak
      print s
