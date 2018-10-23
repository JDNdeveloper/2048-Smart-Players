#!/usr/bin/python

import unittest
import Player

NUM_ITERS = 10

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
      self.assertEquals(len(scores), NUM_ITERS)
      self.assertEquals(len(maxTiles), NUM_ITERS)
      self.assertEquals(len(numMoves), NUM_ITERS)

      # check scores
      verifyRanges(self, scores, ((100, 2000), (3000, 20000)))

      # check max tiles
      verifyRanges(self, maxTiles, ((64, 512), (128, 2048)))

      # check moves
      verifyRanges(self, numMoves, ((50, 300), (150, 1000)))

class BaselineRandomPlayerTest(unittest.TestCase):
   def setUp(self):
      self.p = Player.BaselineRandomPlayer()

   def testRun(self):
      """Check that it's performing as expected."""
      (scores, maxTiles, numMoves) = self.p.run(numIters=NUM_ITERS, printStats=True)
      self.assertEquals(len(scores), NUM_ITERS)
      self.assertEquals(len(maxTiles), NUM_ITERS)
      self.assertEquals(len(numMoves), NUM_ITERS)

      # check scores
      verifyRanges(self, scores, ((100, 2000), (1000, 10000)))

      # check max tiles
      verifyRanges(self, maxTiles, ((8, 128), (64, 1024)))

      # check moves
      verifyRanges(self, numMoves, ((20, 200), (100, 1000)))

if __name__ == '__main__':
   unittest.main()
