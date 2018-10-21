#!/usr/bin/python

import unittest
import Player

class BaselineRandomPlayerTest(unittest.TestCase):
   def setUp(self):
      self.p = Player.BaselineRandomPlayer()

   def testRun(self):
      scores = self.p.run(numIters=10)
      assert len(scores) == 10
      assert min(scores) > 0
      assert max(scores) < 20000

if __name__ == '__main__':
   unittest.main()
