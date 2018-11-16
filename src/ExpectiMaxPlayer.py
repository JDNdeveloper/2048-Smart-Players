from Player import Player
import random
import copy

########################################################################################################################
# TODO: implement heuristics
########################################################################################################################
class ExpectiMaxPlayer(Player):
    """Plays with an expectimax algorithm"""

    def __init__(self, depth=3):
        super(ExpectiMaxPlayer, self).__init__()
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
        return [(row, col) for row in range(self.m.SIZE) for col in range(self.m.SIZE) if board[row][col] == None]

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
            return self.m.makeMove(move, modifyState=False, returnBoard=True)[2]
        else: 
            row, col = move[1]
            val = move[0]
            board[row][col] = val
            return board
            


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
        #######################################
        def recurse(board, index, depth):
            ###################### Base cases
            if depth == 0: 
                return ("", self.evalFunction(board), index)
            if self.isGameOver(board):
                return ("", self.getScore(board), index)
            ######################
            # legalMoves = self.legalMoves_agent if index == 0 else [(2, random.choice(self.getOpenPos(board)))] + [(4, random.choice(self.getOpenPos(board)))]
            
            # if len(self.getOpenPos(board)) < 8 and index != 0:
            #     legalMoves = [(2, pos) for pos in self.getOpenPos(board)] + [(4, pos) for pos in self.getOpenPos(board)] #based on player vs. random gen
                
            # print legalMoves

            legalMoves = self.legalMoves_agent if index == 0 else [(2, pos) for pos in self.getOpenPos(board)] + [(4, pos) for pos in self.getOpenPos(board)]
            newBoards = [self.generateNextMove(board, index, move) for move in legalMoves]
            
            if index == 0: #agent case
                moveRewards = [recurse(newBoard, index+1, depth)[1] for newBoard in newBoards]
            else: #rand case
                moveRewards = [recurse(newBoard, 0, depth-1)[1] for newBoard in newBoards]
            
            if index == 0:
                maxIdx = moveRewards.index(max(moveRewards))
                return (legalMoves[maxIdx], max(moveRewards), index)
            else:
                return ("", (0.9*moveRewards[0] + 0.1*moveRewards[1]), index)
            assert False

        #######################################
        self.adjustLegalMoves(board)
        bestMove = recurse(self.m.getState()[0], 0, self.depth)
        self.lastMove = bestMove[0]
        # print board
        # print board[0][0]
        # print "BestMove: {}".format(bestMove[0])
        return self.lastMove
    
    def evalFunction(self, board): #Todo
        retVal = len(self.getOpenPos(board))
        if self.maxTile(board) == board[0][0]:
            retVal *= 1000
        elif not (self.maxTile(board) in [board[i][0] for i in range(len(board))]):
            retVal /= self.maxTile(board)
        return retVal #+0.2*self.getScore(board)
        
        
        
        
        
