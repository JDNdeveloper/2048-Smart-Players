#!/usr/bin/python

import unittest
import Player

class BaselineRandomPlayerTest(unittest.TestCase):
   def setUp(self):
      self.p = Player.BaselineRandomPlayer()

   def testRun(self):
      """Check that it's performing as expected."""
      (scores, maxTiles) = self.p.run(numIters=10, printStats=True)

      # check scores
      assert len(scores) == 10
      assert min(scores) > 0
      assert max(scores) < 20000

      # check max tiles
      assert len(maxTiles) == 10
      assert min(maxTiles) >= 4
      assert max(maxTiles) < 2048

if __name__ == '__main__':
   unittest.main()
