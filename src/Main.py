#!/usr/bin/python

import argparse
import Player

DEFAULT_ITERS = 100
PLAYER_NAMES = ['GREEDY', 'RANDOM']
DEFAULT_PLAYER_NAME = PLAYER_NAMES[0]

def main(playerName, numIters):
   """Primary test harness."""

   if playerName == PLAYER_NAMES[0]:
      # run the baseline greedy player
      p = Player.BaselineGreedyPlayer()
      p.run(numIters=numIters, printStats=True)
   elif playerName == PLAYER_NAMES[1]:
      # run the baseline random player
      p = Player.BaselineRandomPlayer()
      p.run(numIters=numIters, printStats=True)

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('numIters', nargs='?', default=DEFAULT_ITERS,
                       help=('number of simulation runs, default %d' %
                             DEFAULT_ITERS))
   parser.add_argument('--player', default='greedy',
                       help=('player type: %s, default: %s' %
                             (' or '.join(PLAYER_NAMES), DEFAULT_PLAYER_NAME)))
   args = parser.parse_args()

   main(args.player.upper(), int(args.numIters))
