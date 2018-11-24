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
        self.lastBoard = None
        self.lastMove = None

    def generateNextMove(self, board, index, move):
        """Simulate next move for agent or rand"""
        if index == 0:
            (_, boardChanged, newBoard) = self.m.makeMove(move, modifyState=False,
                                                          returnBoard=True)
            if boardChanged:
                return (newBoard, move)
            else:
                return None
        else:
            row, col = move[1]
            val = move[0]
            new_board = copy.deepcopy(board)
            new_board[row][col] = val
            return (new_board, move[0])

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
                legalMoves = (self.m.MOVES
                              if index == 0
                              else ([(2, pos) for pos in
                                     self.m.getBoardOpenPositions(board)] +
                                   [(4, pos) for pos in
                                    self.m.getBoardOpenPositions(board)]))

                newBoards = [nextMoveResult
                             for move in legalMoves
                             for nextMoveResult in [self.generateNextMove(
                                     board, index, move)]
                             if nextMoveResult is not None]
                if index == 0: #agent case
                    moveRewards = [(recurse(newBoard[0], index+1, depth)[1],
                                    newBoard[1])
                                   for newBoard in newBoards]
                else: #rand case
                    moveRewards_2 = [recurse(newBoard[0], 0, depth-1)[1]
                                     for newBoard in newBoards if newBoard[1] == 2]
                    moveRewards_4 = [recurse(newBoard[0], 0, depth-1)[1]
                                     for newBoard in newBoards if newBoard[1] == 4]
                if index == 0:
                    (maxReward, maxMove) = max(moveRewards)
                    result = (maxMove, maxReward, index)
                else:
                    result = ("", (0.9*sum(moveRewards_2) + 0.1*sum(moveRewards_4) /
                                   (len(newBoards) / 2.0)),
                              index)
            assert result is not None
            lookup[state] = result
            return result

        #######################################
        bestMove = recurse(self.m.getState()[0], 0, self.depth)
        self.lastMove = bestMove[0]
        if self.debug:
            print "BestMove: {}".format(movePlayed[self.lastMove])
            print self.m.getBoardString(board)
        return self.lastMove

    def evalFunction(self, board):
        score = self.m.getBoardScore(board)
        maxTile = self.m.getBoardMaxTile(board) ** 2
        numNone = len(self.m.getBoardOpenPositions(board))**2
        maxTilePosCorrect = (100 if maxTile == board[0][0]
                             else -10)
        maxTileRowCorrect = (10 if maxTile in board[0]
                             else 0)
        topRowDecreasing = sum([(len(board[0]) - i)*10 for i in range(len(board[0]))
                                if board[0][i] > board[0][(i+1)%len(board[0])]])
        weights = {
            score: 1.0,
            maxTile: 1.0,
            numNone: 0.3,
            maxTilePosCorrect: 0.0,
            maxTileRowCorrect: 0.0,
            topRowDecreasing: 0.0,
        }
        return sum(feature * weight for (feature, weight) in weights.iteritems())
