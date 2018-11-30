import copy
import ctypes
import random
from Model import Model
from Player import Player

cLib = ctypes.cdll.LoadLibrary('./libExpectiMaxPlayer.so')

class CExpectiMaxPlayer(object):
    def __init__(self, size, debug):
        self.size = size
        self.debug = debug
        self.obj = cLib.ExpectiMaxPlayer_new(self.debug)
        self.board = cLib.Board_new(size)

    def _setBoard(self, board):
        for (row, rowList) in enumerate(board):
            for (col, val) in enumerate(rowList):
                cLib.Board_setPos(self.board, row, col, val)

    def getMove(self, board):
        self._setBoard(board)
        return cLib.ExpectiMaxPlayer_getMove(self.obj, self.board)

    def __del__(self):
        # Always good to avoid memory leaks!
        cLib.ExpectiMaxPlayer_delete(self.obj)
        cLib.Board_delete(self.board)

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
        self.cPlayer = CExpectiMaxPlayer(Model.SIZE, self.debug)

        self.getMoveRecurseLookup = {}
        self.generateNextMoveLookup = {}

    def generateNextMove(self, board, index, move):
        """Simulate next move for agent or rand"""
        state = (str(board), index, move)
        if state in self.generateNextMoveLookup:
            return self.generateNextMoveLookup[state]
        result = None
        if index == 0:
            (_, boardChanged, newBoard) = self.m.makeBoardMove(
                board, move, modifyState=False, returnBoard=True)
            if boardChanged:
                result = (newBoard, move)
            else:
                result = None
        else:
            row, col = move[1]
            val = move[0]
            new_board = copy.deepcopy(board)
            new_board[row][col] = val
            result = (new_board, move[0])
        self.generateNextMoveLookup[state] = result
        return result

    def getMove(self, board, score):
        """
        Runs an expectimax algorithm to try and get the next best move
        [More to follow]
        """

        # TODO return this call once finished implementing
        return self.cPlayer.getMove(board)

        #######################################
        def recurse(board, index, depth):
            state = (str(board), index, depth)
            if state in self.getMoveRecurseLookup:
                return self.getMoveRecurseLookup[state]
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
                    result = ("", ((0.9*sum(moveRewards_2) + 0.1*sum(moveRewards_4))
                                   / (len(newBoards) / 2.0)),
                              index)
            assert result is not None
            self.getMoveRecurseLookup[state] = result
            return result

        #######################################
        bestMove = recurse(self.m.getState()[0], 0, self.depth)
        self.lastMove = bestMove[0]
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
        numEmptyTiles = len(openPositions) ** 2.0

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
                                        10000000 if maxTile == invertedBoard[0][0]
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
            'maxTile': 0.0,
            'numEmptyTiles': 1.0,
            'snaking': 1.0,
            'maxTilePosCorrect': 1.0,
            'maxTileRowCorrect': 0.0,
        }
        return sum(featureValues[feature] * weights[feature]
                   for feature in featureValues.iterkeys())
