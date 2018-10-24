#!/usr/bin/python

import argparse
import Model
import Player

DEFAULT_ITERS = 1
PLAYER_NAMES = ['INTERACTIVE', 'GREEDY', 'CORNER', 'RANDOM']
DEFAULT_PLAYER_NAME = PLAYER_NAMES[0]

def main(playerName, numIters, size):
   """Primary test harness."""

   # set the board size
   Model.Model.SIZE = size

   if playerName == PLAYER_NAMES[0]:
      # run the interactive player
      p = Player.InteractivePlayer()
      p.run(numIters=numIters)
   elif playerName == PLAYER_NAMES[1]:
      # run the baseline greedy player
      p = Player.BaselineGreedyPlayer()
      p.run(numIters=numIters, printStats=True, printAtCheckpoints=True)
   elif playerName == PLAYER_NAMES[2]:
      # run the baseline corner player
      p = Player.BaselineCornerPlayer()
      p.run(numIters=numIters, printStats=True, printAtCheckpoints=True)
   elif playerName == PLAYER_NAMES[3]:
      # run the baseline random player
      p = Player.BaselineRandomPlayer()
      p.run(numIters=numIters, printStats=True, printAtCheckpoints=True)

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('numIters', nargs='?', default=DEFAULT_ITERS,
                       help=('number of simulation runs, default %d' %
                             DEFAULT_ITERS))
   parser.add_argument('--player', default=DEFAULT_PLAYER_NAME,
                       help=('player type: %s, default %s' %
                             (' or '.join(PLAYER_NAMES), DEFAULT_PLAYER_NAME)))
   parser.add_argument('--size', default=Model.DEFAULT_SIZE,
                       help=('dimension of board, default %d' % Model.DEFAULT_SIZE))
   args = parser.parse_args()

   main(args.player.upper(), int(args.numIters), int(args.size))
