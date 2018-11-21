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

    def getMove(self, board, score):
        """
        Runs an expectimax algorithm to try and get the next best move
        [More to follow]
        """

        movePlayed = ['', 'UP', 'DOWN', 'LEFT', 'RIGHT']
        #######################################
        lookup = {}
        def recurse(board, index, depth):
            state = (str(board), index, depth)
            if state in lookup:
                return lookup[state]
            result = None
            ###################### Base cases
            if depth == 0:
                result = ("", self.evalFunction(board), index)
            elif self.m.isBoardGameOver(board):
                result = ("", self.m.getBoardScore(board), index)
            else:
                ######################
                legalMoves = (self.legalMoves_agent
                              if index == 0
                              else ([(2, pos) for pos in
                                     self.m.getBoardOpenPositions(board)] +
                                   [(4, pos) for pos in
                                    self.m.getBoardOpenPositions(board)]))

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
                    result = (legalMoves[maxIdx], max(moveRewards), index)
                else:
                    result = ("", 0.9*sum(moveRewards_2) + 0.1*sum(moveRewards_4),
                              index)
            assert result is not None
            lookup[state] = result
            return result

        #######################################
        self.adjustLegalMoves(board)
        bestMove = recurse(self.m.getState()[0], 0, self.depth)
        self.lastMove = bestMove[0]
        if self.debug:
            print "BestMove: {}".format(movePlayed[bestMove[0]])
            print self.m.getBoardString(board)
        return self.lastMove

    def evalFunction(self, board):
        score = self.m.getBoardScore(board)
        return score
        # TODO fix the advanced heuristic
        # numNone = len(self.m.getBoardOpenPositions(board))**2
        # maxTilePosCorrect = (100 if self.m.getBoardMaxTile(board) == board[0][0]
        #                      else -10)
        # maxTileColCorrect = (10 if self.m.getBoardMaxTile(board) in board[0]
        #                      else 0)
        # topRowDecreasing = sum([(len(board[0]) - i)*10 for i in range(len(board[0]))
        #                         if board[0][i] > board[0][(i+1)%len(board[0])]])
        # phi = [score, numNone, maxTilePosCorrect, maxTileColCorrect,
        #        topRowDecreasing]
        # weights = [0, 1.4, 2, 0, 2]
        # return sum([weights[i]*phi[i] for i in range(len(phi))])
