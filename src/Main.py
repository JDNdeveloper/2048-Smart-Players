#!/usr/bin/python

import argparse
import Player

DEFAULT_ITERS = 100

def main(numIters=DEFAULT_ITERS):
   """Primary test harness."""

   # run the baseline random player
   p = Player.BaselineRandomPlayer()
   p.run(numIters=numIters, printStats=True)

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('numIters', nargs='?', default=DEFAULT_ITERS,
                       help=('number of simulation runs, default %d' %
                             DEFAULT_ITERS))
   args = parser.parse_args()

   main(numIters=int(args.numIters))
