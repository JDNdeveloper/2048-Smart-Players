#!/usr/bin/python

import Player

def main():
   """Primary test harness."""

   # run the baseline random player
   p = Player.BaselineRandomPlayer()
   p.run(numIters=100, printStats=True)

if __name__ == '__main__':
   main()
