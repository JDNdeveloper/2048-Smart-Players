from Player import Player
import random
import copy

########################################################################################################################
# TODO: change tile spawning to consider all possible spawns
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
        if len([(row, col) for row in range(self.m.SIZE) for col in range(self.m.SIZE) if board[row][col] == None]) > 0:
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

    def randomFill(self, board, move):
        """Randomly fill an open position on the board.
        The fill values and probability distribution is defined above.
        """
        openPos = [(row, col) for row in range(self.m.SIZE) for col in range(self.m.SIZE) if board[row][col] == None]
        if len(openPos) == 0: return board
        (row, col) = random.choice(openPos)
        board[row][col] = move
        return board

    def generateNextMove(self, board, index, move):
        """Simulate next move for agent or rand"""
        if index == 0:
            return self.m.makeMove(move, modifyState=False, returnBoard=True)[2]
        else: 
            return self.randomFill(board, move)


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

            legalMoves = self.legalMoves_agent if index == 0 else [2, 4] #based on player vs. random gen
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
        return self.lastMove
    
    def evalFunction(self, board): #Todo
        return self.getScore(board)
        
        
        
        
        
