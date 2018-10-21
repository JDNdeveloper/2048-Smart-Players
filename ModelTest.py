#!/usr/bin/python

import unittest
import Model

class ModelTest(unittest.TestCase):
   def setUp(self):
      self.m = Model.Model()

   def testReset(self):
      print "Testing Reset"

if __name__ == '__main__':
   unittest.main()
