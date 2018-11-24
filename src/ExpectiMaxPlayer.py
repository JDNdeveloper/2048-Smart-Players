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
        def maxDescendingAndSnakingScore(board):
            """Check if descending sorted values snake across
            the board (left to right, top to bottom).

            100,000 * (10 ^ N) reward where N is the number of
            fully-formed snaked rows (if N is zero then reward zero).
            """
            values = self.m.getBoardSortedValues(board)
            snakingRows = 0
            for i, row in enumerate(board):
                start = i * self.m.SIZE
                end = start + self.m.SIZE
                if values[start:end] == (row if i % 2 == 0 else row[::-1]):
                    snakingRows += 1
                else:
                    break
            return 100000 * (10 ** snakingRows) if snakingRows > 0 else 0

        # board state
        score = self.m.getBoardScore(board)
        maxTile = self.m.getBoardMaxTile(board)
        openPositions = self.m.getBoardOpenPositions(board)

        # state heuristics
        scoreScore = score ** 1.2
        maxTileScore = maxTile ** 1.3
        numEmptyTiles = len(openPositions) ** 1.2

        # positional heuristics
        snaking = 0
        maxTilePosCorrect = 0
        maxTileRowCorrect = 0

        # try for all four rotations of the board, and both mirrored versions
        invertedBoard = board
        for _ in range(2):
            for _ in range(4):
                # update positional heuristics if inverted board yields higher value
                snaking = max(snaking,
                              maxDescendingAndSnakingScore(invertedBoard))
                maxTilePosCorrect = max(maxTilePosCorrect,
                                        1000 if maxTile == invertedBoard[0][0]
                                        else 0)
                maxTileRowCorrect = max(maxTileRowCorrect,
                                        100 if maxTile in invertedBoard[0]
                                        else 0)

                # rotate the board
                invertedBoard = self.m.getBoardRotated(invertedBoard)
            # mirror the board
            invertedBoard = self.m.getBoardMirrored(invertedBoard)

        featureValues = {
            'score': scoreScore,
            'maxTile': maxTile,
            'numEmptyTiles': numEmptyTiles,
            'snaking': snaking,
            'maxTilePosCorrect': maxTilePosCorrect,
            'maxTileRowCorrect': maxTileRowCorrect,
        }
        weights = {
            'score': 1.0,
            'maxTile': 1.0,
            'numEmptyTiles': 1.0,
            'snaking': 1.0,
            'maxTilePosCorrect': 1.0,
            'maxTileRowCorrect': 1.0,
        }
        return sum(featureValues[feature] * weights[feature]
                   for feature in featureValues.iterkeys())
