#!/usr/bin/python

import numpy as np
import random
import Model

class Player(object):
   def __init__(self):
      self.m = Model.Model()

   def run(self, numIters=1, printStats=False):
      """Runs the game.

      Args:
      numIters: The number of times to run the game.
      printStats: If True, stats for scores are outputted.

      Returns:
      (scores, maxTiles): Scores and maxTiles lists from all runs.
      """
      scores = []
      maxTiles = []
      numMoves = []

      for i in range(numIters):
         self.m.reset()

         count = 0
         while not self.m.isGameOver():
            board, score = self.m.getState()
            move = self.getMove(board, score)
            self.m.makeMove(move)
            count += 1

         scores.append(self.m.score)
         maxTiles.append(self.m.maxTile())
         numMoves.append(count)

      if printStats:
         self._printScoreStats(scores)
         self._printMaxTileStats(maxTiles)
         self._printMoveStats(numMoves)

      return (scores, maxTiles, numMoves)

   def getMove(self, board, score):
      """Get the next move given current board and score."""
      raise NotImplementedError

   @staticmethod
   def _printStats(data, dataName):
      """Outputs stastics about the given data."""
      npData = np.array(data)
      print (dataName + ' ::: ' + ', '.join([
         "Total runs: %d",
         "Max: %d",
         "Min: %d",
         "Median: %d",
         "Average: %d",
         "Stdev: %d",
      ]) % (len(data),
            max(data),
            min(data),
            np.median(npData),
            npData.mean(),
            npData.std(),
      ))

   @staticmethod
   def _printScoreStats(scores):
      """Output basic statistics about the scores."""
      Player._printStats(scores, 'SCORES')

   @staticmethod
   def _printMaxTileStats(maxTiles):
      """Output stastics about the max tiles."""
      Player._printStats(maxTiles, 'MAX TILES')

   @staticmethod
   def _printMoveStats(numMoves):
      """Output stastics about the number of moves."""
      Player._printStats(numMoves, 'MOVES')

class BaselineGreedyPlayer(Player):
   def getMove(self, board, score):
      """Player chooses move that yields maximum points for that turn."""
      maxScore = 0
      maxMove = None
      validMoves = []

      for move in [Model.Move.UP, Model.Move.LEFT]:
         # choose move that maximizes score and would actually change the board
         (moveScore, boardChanged) = self.m.makeMove(move, modifyState=False)
         if boardChanged:
            validMoves.append(move)
            if moveScore > maxScore:
               maxMove = move
               maxScore = moveScore

      if maxMove:
         # if one or both of the scores were non-zero, return the max score move
         return maxMove

      if validMoves:
         # if there were no moves with non-zero score, just return a valid one
         return validMoves[0]

      for move in [Model.Move.DOWN, Model.Move.RIGHT]:
         # if up and left were not valid, return the first valid of down and right
         (moveScore, boardChanged) = self.m.makeMove(move, modifyState=False)
         if boardChanged:
            return move

class BaselineRandomPlayer(Player):
   def getMove(self, board, score):
      """Gives a random move."""
      return random.choice([
         Model.Move.UP,
         Model.Move.DOWN,
         Model.Move.LEFT,
         Model.Move.RIGHT,
      ])

class InteractivePlayer(Player):
   def getMove(self, board, score):
      print self.m
      print "Score: %d\n" % score

      moves = {
         '1': Model.Move.UP,
         '2': Model.Move.DOWN,
         '3': Model.Move.LEFT,
         '4': Model.Move.RIGHT,
      }
      move = None
      while move not in moves:
         move = raw_input("Enter move: 1=UP, 2=DOWN, 3=LEFT, 4=RIGHT: ")
      return moves[move]

if __name__ == '__main__':
   """Run interactive player."""
   p = InteractivePlayer()
   p.run()
