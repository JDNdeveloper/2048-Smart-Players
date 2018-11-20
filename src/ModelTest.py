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
         self.assertIn(set(filledValues), expectedFilledValues)
         occurrences[expectedFilledValues.index(set(filledValues))] += 1
         self.assertEquals(len(filledValues), 2)
         self.assertEquals(self.m.score, 0)
      self.assertGreater(occurrences[0], occurrences[1])
      self.assertGreater(occurrences[1], occurrences[2])
      self.assertGreater(occurrences[2], 0)

   def testMakeMove(self):
      ## Direction Tests

      diagonalBoard = [[2 if row == col else None
                        for col in range(self.m.SIZE)]
                       for row in range(self.m.SIZE)]

      def verifyBoard(fixedRowColValues=None,
                      fixedRowValues=None,
                      fixedColValues=None,
                      randomFillExpected=1):
         """Verifies board has expected values."""
         randomFillFound = 0

         for row in range(self.m.SIZE):
            for col in range(self.m.SIZE):
               val = self.m.board[row][col]

               if fixedRowColValues and (row, col) in fixedRowColValues:
                  self.assertEqual(val, fixedRowColValues[(row, col)])
               elif fixedRowValues and row in fixedRowValues:
                  self.assertEqual(val, fixedRowValues[row])
               elif fixedColValues and col in fixedColValues:
                  self.assertEqual(val, fixedColValues[col])
               else:
                  if val is not None:
                     randomFillFound += 1

         self.assertEquals(randomFillFound, randomFillExpected)

      def verifyMove(initialBoard, move, expectedScore,
                     expectedMoveScore=None, reset=True,
                     expectedBoardToChange=True,
                     modifyState=True):
         """Sets up initial board and verifies move and resulting state."""
         if reset:
            self.m.reset()
         if expectedMoveScore is None:
            expectedMoveScore = expectedScore

         self.m.board = copy.deepcopy(initialBoard)
         (moveScore, boardChanged) = self.m.makeMove(
            move, modifyState=modifyState)

         self.assertEqual(moveScore, expectedMoveScore)
         self.assertEqual(boardChanged, expectedBoardToChange)
         self.assertEqual(self.m.score, expectedScore)

      # UP
      verifyMove(diagonalBoard, Model.Move.UP, 0)
      verifyBoard(fixedRowValues={0: 2})

      # DOWN
      verifyMove(diagonalBoard, Model.Move.DOWN, 0)
      verifyBoard(fixedRowValues={self.m.SIZE - 1: 2})

      # LEFT
      verifyMove(diagonalBoard, Model.Move.LEFT, 0)
      verifyBoard(fixedColValues={0: 2})

      # RIGHT
      verifyMove(diagonalBoard, Model.Move.RIGHT, 0)
      verifyBoard(fixedColValues={self.m.SIZE - 1: 2})

      ## Merging Tests

      # two items
      twoMergeBoard = [[2 if row in [0, 1] else None
                        for col in range(self.m.SIZE)]
                       for row in range(self.m.SIZE)]
      expectedTwoMergeScore = 4 * self.m.SIZE
      verifyMove(twoMergeBoard, Model.Move.UP, expectedTwoMergeScore)
      verifyBoard(fixedRowValues={0: 4})

      # two items without changing state
      verifyMove(twoMergeBoard, Model.Move.UP, 0,
                 expectedMoveScore=expectedTwoMergeScore, modifyState=False)
      verifyBoard(fixedRowValues={0: 2, 1: 2}, randomFillExpected=0)

      # four items
      fourMergeBoard = [[2 if row in [0, 1, 2, 3] else None
                         for col in range(self.m.SIZE)]
                        for row in range(self.m.SIZE)]
      expectedFourMergeScore = 2 * expectedTwoMergeScore
      verifyMove(fourMergeBoard, Model.Move.UP, expectedFourMergeScore)
      verifyBoard(fixedRowValues={0: 4, 1: 4})

      # three items (third item should not merge)
      threeMergeBoard = [[2 if row in [0, 1, 2] else None
                         for col in range(self.m.SIZE)]
                        for row in range(self.m.SIZE)]
      expectedThreeMergeScore = expectedTwoMergeScore
      verifyMove(threeMergeBoard, Model.Move.UP, expectedThreeMergeScore)
      verifyBoard(fixedRowValues={0: 4, 1: 2})

      ## Edge Case Tests

      # moving UP should not change the board
      upFixedBoard = [[2 if row in [0] else None
                       for col in range(self.m.SIZE)]
                      for row in range(self.m.SIZE)]
      verifyMove(upFixedBoard, Model.Move.UP, 0, expectedBoardToChange=False)
      verifyBoard(fixedRowValues={0: 2}, randomFillExpected=0)

      # two moves in a row, both with merges
      verifyMove(fourMergeBoard, Model.Move.UP, expectedFourMergeScore)
      verifyBoard(fixedRowValues={0: 4, 1: 4})
      verifyMove(self.m.board, Model.Move.UP, 2 * expectedFourMergeScore,
                 expectedMoveScore=expectedFourMergeScore, reset=False)
      verifyBoard(fixedRowValues={0: 8}, randomFillExpected=2)

      # verify score for up/down and left/right are the same
      sameScoreBoard = [
         [2, None, None, None],
         [None, None, None, 2],
         [None, None, None, 2],
         [None, None, 4, 2],
      ]
      verifyMove(sameScoreBoard, Model.Move.UP, 4)
      verifyMove(sameScoreBoard, Model.Move.DOWN, 4)
      verifyMove(sameScoreBoard, Model.Move.LEFT, 0)
      verifyMove(sameScoreBoard, Model.Move.RIGHT, 0)

      # test a 5x5 board
      Model.Model.SIZE = 5
      fiveBoard = [[2 if row in [0, 1, 2, 3] else None
                    for col in range(self.m.SIZE)]
                   for row in range(self.m.SIZE)]
      expectedFiveBoardScore = 2 * 4 * self.m.SIZE
      verifyMove(fiveBoard, Model.Move.UP, expectedFiveBoardScore)
      verifyBoard(fixedRowValues={0: 4, 1: 4})
      # set size back to default
      Model.Model.SIZE = Model.DEFAULT_SIZE

   def testIsGameOver(self):
      # verify new board is not game over
      self.assertFalse(self.m.isGameOver())

      # verify full board with possible up/down compression
      # is not game over
      self.m.board = [[2 ** (col + 1)
                       for col in range(self.m.SIZE)]
                      for row in range(self.m.SIZE)]
      self.assertFalse(self.m.isGameOver())

      # verify full board with possible left/right compression
      # is not game over
      self.m.board = [[2 ** (row + 1)
                       for col in range(self.m.SIZE)]
                      for row in range(self.m.SIZE)]
      self.assertFalse(self.m.isGameOver())

      # verify full board with no compression is game over
      self.m.board = [[2 ** ((row + col) % 2 + 1)
                       for col in range(self.m.SIZE)]
                      for row in range(self.m.SIZE)]
      self.assertTrue(self.m.isGameOver())

   def testMaxTile(self):
      # test empty board
      self.m.board = [[None for _ in range(self.m.SIZE)]
                      for _ in range(self.m.SIZE)]
      self.assertEqual(self.m.maxTile(), None)

      # test normal board
      self.m.board = [
         [2, None, None, None],
         [None, None, None, 2],
         [None, None, None, 2],
         [None, None, 4, 2],
      ]
      self.assertEqual(self.m.maxTile(), 4)

      # test full board with duplicate max's
      self.m.board = [
         [2, 8, 16, 256],
         [8, 32, 4, 2],
         [2, 256, 64, 2],
         [16, 8, 4, 2],
      ]
      self.assertEqual(self.m.maxTile(), 256)

   def testNumTiles(self):
      # test empty board
      self.m.board = [[None for _ in range(self.m.SIZE)]
                      for _ in range(self.m.SIZE)]
      self.assertEqual(self.m.numTiles(), 0)

      # test board with two tiles
      self.m.board = [
         [2, None, None, None],
         [None, 4, None, None],
         [None, None, None, None],
         [None, None, None, None],
      ]
      self.assertEqual(self.m.numTiles(), 2)

      # test board with five tiles
      self.m.board = [
         [2, None, None, None],
         [None, None, None, 2],
         [None, None, None, 2],
         [None, None, 4, 2],
      ]
      self.assertEqual(self.m.numTiles(), 5)

      # test full board
      self.m.board = [
         [2, 8, 16, 256],
         [8, 32, 4, 2],
         [2, 4, 64, 2],
         [16, 8, 4, 2],
      ]
      self.assertEqual(self.m.numTiles(), 16)

if __name__ == '__main__':
   unittest.main()
