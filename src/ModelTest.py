#!/usr/bin/python

import copy
import unittest
import Model

class ModelTest(unittest.TestCase):
   def setUp(self):
      self.m = Model.Model()

   def testReset(self):
      # fill the board and score with junk
      self.board = [range(self.m.SIZE) for _ in range(self.m.SIZE)]
      self.score = 1234

      # reset
      self.m.reset()

      # check that there are only two values in the board
      # and the score is reset
      #
      # run enough times to make sure we see all 2 and 4 combos
      # and verify we did see all of them by the end and that we
      # see more (2,2) than (2,4) than (4,4) (due to the probabilities)
      expectedFilledValues = [set([2,2]), set([2,4]), set([4,4])]
      occurrences = [0, 0, 0]
      for _ in range(5000):
         self.m.reset()
         filledValues = [self.m.board[row][col]
                         for row in range(self.m.SIZE)
                         for col in range(self.m.SIZE)
                         if self.m.board[row][col] is not None]
         assert set(filledValues) in expectedFilledValues
         occurrences[expectedFilledValues.index(set(filledValues))] += 1
         assert len(filledValues) == 2
         assert self.m.score == 0
      assert (occurrences[0] > occurrences[1] and
              occurrences[1] > occurrences[2] and
              occurrences[2] > 0)

   def testMakeMove(self):
      ## Direction Tests

      diagonalBoard = [[2 if row == col else None
                        for col in range(self.m.SIZE)]
                       for row in range(self.m.SIZE)]

      def verifyBoard(fixedRowColValues=None,
                      fixedRowValues=None,
                      fixedColValues=None,
                      randomFillExpected=True):
         randomFillFound = not randomFillExpected

         for row in range(self.m.SIZE):
            for col in range(self.m.SIZE):
               val = self.m.board[row][col]

               if fixedRowColValues and (row, col) in fixedRowColValues:
                  assert val == fixedRowColValues[(row, col)]
               elif fixedRowValues and row in fixedRowValues:
                  assert val == fixedRowValues[row]
               elif fixedColValues and col in fixedColValues:
                  assert val == fixedColValues[col]
               else:
                  if val is not None:
                     assert not randomFillFound
                     randomFillFound = True

         assert randomFillFound

      # UP
      self.m.board = copy.deepcopy(diagonalBoard)
      self.m.makeMove(Model.Move.UP)
      verifyBoard(fixedRowValues={0: 2})
      assert self.m.score == 0

      # DOWN
      self.m.board = copy.deepcopy(diagonalBoard)
      self.m.makeMove(Model.Move.DOWN)
      verifyBoard(fixedRowValues={self.m.SIZE - 1: 2})
      assert self.m.score == 0

      # LEFT
      self.m.board = copy.deepcopy(diagonalBoard)
      self.m.makeMove(Model.Move.LEFT)
      verifyBoard(fixedColValues={0: 2})
      assert self.m.score == 0

      # RIGHT
      self.m.board = copy.deepcopy(diagonalBoard)
      self.m.makeMove(Model.Move.RIGHT)
      verifyBoard(fixedColValues={self.m.SIZE - 1: 2})
      assert self.m.score == 0

      ## Merging Tests

      # two items
      twoMergeBoard = [[2 if row in [0, 1] else None
                        for col in range(self.m.SIZE)]
                       for row in range(self.m.SIZE)]
      self.m.reset()
      self.m.board = copy.deepcopy(twoMergeBoard)
      self.m.makeMove(Model.Move.UP)
      verifyBoard(fixedRowValues={0: 4})
      assert self.m.score == 4 * self.m.SIZE

      # four items
      fourMergeBoard = [[2 if row in [0, 1, 2, 3] else None
                         for col in range(self.m.SIZE)]
                        for row in range(self.m.SIZE)]
      self.m.reset()
      self.m.board = copy.deepcopy(fourMergeBoard)
      self.m.makeMove(Model.Move.UP)
      verifyBoard(fixedRowValues={0: 4, 1: 4})
      assert self.m.score == 2 * (4 * self.m.SIZE)

      # three items (third item should not merge)
      threeMergeBoard = [[2 if row in [0, 1, 2] else None
                         for col in range(self.m.SIZE)]
                        for row in range(self.m.SIZE)]
      self.m.reset()
      self.m.board = copy.deepcopy(threeMergeBoard)
      self.m.makeMove(Model.Move.UP)
      verifyBoard(fixedRowValues={0: 4, 1: 2})
      assert self.m.score == 4 * self.m.SIZE

      ## Edge Case Tests

      # moving UP should not change the board
      upFixedBoard = [[2 if row in [0] else None
                       for col in range(self.m.SIZE)]
                      for row in range(self.m.SIZE)]
      self.m.reset()
      self.m.board = copy.deepcopy(upFixedBoard)
      self.m.makeMove(Model.Move.UP)
      verifyBoard(fixedRowValues={0: 2}, randomFillExpected=False)
      assert self.m.score == 0

   def testIsGameOver(self):
      # verify new board is not game over
      assert not self.m.isGameOver()

      # verify full board with possible up/down compression
      # is not game over
      self.m.board = [[2 ** (col + 1)
                       for col in range(self.m.SIZE)]
                      for row in range(self.m.SIZE)]
      assert not self.m.isGameOver()

      # verify full board with possible left/right compression
      # is not game over
      self.m.board = [[2 ** (row + 1)
                       for col in range(self.m.SIZE)]
                      for row in range(self.m.SIZE)]
      assert not self.m.isGameOver()

      # verify full board with no compression is game over
      self.m.board = [[2 ** ((row + col) % 2 + 1)
                       for col in range(self.m.SIZE)]
                      for row in range(self.m.SIZE)]
      assert self.m.isGameOver()

if __name__ == '__main__':
   unittest.main()
