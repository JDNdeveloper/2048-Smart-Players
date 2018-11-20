#!/usr/bin/python

import unittest
import ExpectiMaxPlayer
import Player
import QLPlayer

NUM_ITERS = 10
DEPTH = 1
TRAIN = True
SAVE = False

def verifyRanges(obj, data, ranges):
   """Check that results are within expected ranges."""
   ((minLower, minUpper), (maxLower, maxUpper)) = ranges
   obj.assertGreaterEqual(min(data), minLower)
   obj.assertLess(min(data), minUpper)
   obj.assertGreaterEqual(max(data), maxLower)
   obj.assertLess(max(data), maxUpper)

class BaselineGreedyPlayerTest(unittest.TestCase):
   def setUp(self):
      self.p = Player.BaselineGreedyPlayer()

   def testRun(self):
      """Check that it's performing as expected."""
      (scores, maxTiles, numMoves) = self.p.run(numIters=NUM_ITERS, printStats=True)
      print ''
      self.assertEquals(len(scores), NUM_ITERS)
      self.assertEquals(len(maxTiles), NUM_ITERS)
      self.assertEquals(len(numMoves), NUM_ITERS)

      # check scores
      verifyRanges(self, scores, ((100, 4000), (3000, 20000)))

      # check max tiles
      verifyRanges(self, maxTiles, ((64, 512), (128, 2048)))

      # check moves
      verifyRanges(self, numMoves, ((50, 300), (150, 1000)))

class BaselineCornerPlayerTest(unittest.TestCase):
   def setUp(self):
      self.p = Player.BaselineCornerPlayer()

   def testRun(self):
      """Check that it's performing as expected."""
      (scores, maxTiles, numMoves) = self.p.run(numIters=NUM_ITERS, printStats=True)
      print ''
      self.assertEquals(len(scores), NUM_ITERS)
      self.assertEquals(len(maxTiles), NUM_ITERS)
      self.assertEquals(len(numMoves), NUM_ITERS)

      # check scores
      verifyRanges(self, scores, ((100, 2000), (3000, 15000)))

      # check max tiles
      verifyRanges(self, maxTiles, ((16, 256), (128, 2048)))

      # check moves
      verifyRanges(self, numMoves, ((30, 200), (150, 1000)))

class BaselineRandomPlayerTest(unittest.TestCase):
   def setUp(self):
      self.p = Player.BaselineRandomPlayer()

   def testRun(self):
      """Check that it's performing as expected."""
      (scores, maxTiles, numMoves) = self.p.run(numIters=NUM_ITERS, printStats=True)
      print ''
      self.assertEquals(len(scores), NUM_ITERS)
      self.assertEquals(len(maxTiles), NUM_ITERS)
      self.assertEquals(len(numMoves), NUM_ITERS)

      # check scores
      verifyRanges(self, scores, ((100, 2000), (1000, 10000)))

      # check max tiles
      verifyRanges(self, maxTiles, ((8, 128), (64, 1024)))

      # check moves
      verifyRanges(self, numMoves, ((20, 200), (100, 1000)))

class ExpectiMaxPlayerTest(unittest.TestCase):
   def setUp(self):
      self.p = ExpectiMaxPlayer.ExpectiMaxPlayer(depth=DEPTH)

   def testRun(self):
      """Check that it's performing as expected."""
      (scores, maxTiles, numMoves) = self.p.run(numIters=NUM_ITERS, printStats=True)
      print ''
      self.assertEquals(len(scores), NUM_ITERS)
      self.assertEquals(len(maxTiles), NUM_ITERS)
      self.assertEquals(len(numMoves), NUM_ITERS)

      # check scores
      verifyRanges(self, scores, ((100, 1000), (1000, 10000)))

      # check max tiles
      verifyRanges(self, maxTiles, ((8, 128), (64, 1024)))

      # check moves
      verifyRanges(self, numMoves, ((20, 200), (100, 1000)))

class QLPlayerTest(unittest.TestCase):
   def setUp(self):
      self.p = QLPlayer.RLPlayer(train=TRAIN, save=SAVE)

   def testRun(self):
      """Check that it's performing as expected."""
      (scores, maxTiles, numMoves) = self.p.run(numIters=NUM_ITERS, printStats=True)
      print ''
      self.assertEquals(len(scores), NUM_ITERS)
      self.assertEquals(len(maxTiles), NUM_ITERS)
      self.assertEquals(len(numMoves), NUM_ITERS)

      # check scores
      verifyRanges(self, scores, ((100, 2000), (700, 5000)))

      # check max tiles
      verifyRanges(self, maxTiles, ((8, 128), (32, 512)))

      # check moves
      verifyRanges(self, numMoves, ((20, 200), (80, 500)))

if __name__ == '__main__':
   unittest.main()
