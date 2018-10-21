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
      """
      scores = []

      for i in range(numIters):
         self.m.reset()
         
         while not self.m.isGameOver():
            board, score = self.m.getState()
            move = self.getMove(board, score)
            self.m.makeMove(move)

         scores.append(self.m.score)

      if printStats:
         self._printScoreStats(scores)
         
      return scores

   def getMove(board, score):
      """Get the next move given current board and score."""
      raise NotImplementedError

   @staticmethod
   def _printScoreStats(scores):
      """Output basic statistics about the scores."""
      npScores = np.array(scores)
      print (', '.join([
         "Total runs: %d",
         "Max score: %d",
         "Min score: %d",
         "Average score: %d",
         "Stdev: %d",
      ]) % (len(scores),
            max(scores),
            min(scores),
            npScores.mean(),
            npScores.std(),
      ))

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
