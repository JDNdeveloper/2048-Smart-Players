import copy
import ctypes
import random
from Model import Model
from Player import Player

cLib = ctypes.cdll.LoadLibrary('./libExpectiMaxPlayer.so')

class CExpectiMaxPlayer(object):
    def __init__(self, size, debug, depth):
        self.size = size
        self.debug = debug
        self.depth = depth
        self.obj = cLib.ExpectiMaxPlayer_new(self.debug, self.depth)
        self.board = cLib.Board_new(size)

    def _setBoard(self, board, score):
        cLib.Board_setScore(self.board, score)
        for (row, rowList) in enumerate(board):
            for (col, val) in enumerate(rowList):
                cLib.Board_setPos(self.board, row, col, val)

    def getMove(self, board, score):
        self._setBoard(board, score)
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
        self.cPlayer = CExpectiMaxPlayer(Model.SIZE, self.debug, self.depth)

    def getMove(self, board, score):
        """
        Runs an expectimax algorithm to try and get the next best move
        [More to follow]
        """
        return self.cPlayer.getMove(board, score)
