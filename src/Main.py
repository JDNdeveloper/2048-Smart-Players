#!/usr/bin/python

import argparse
import Model
import Player
import ExpectiMaxPlayer

DEFAULT_ITERS = 1
DEFAULT_DEPTH = 3
PLAYER_NAMES = ['INTERACTIVE', 'GREEDY', 'CORNER', 'RANDOM', 'EXPECTIMAX']
DEFAULT_PLAYER_NAME = PLAYER_NAMES[0]

def main(playerName, numIters, size, debug, depth):
   """Primary test harness."""

   # set the board size
   Model.Model.SIZE = size

   if playerName == PLAYER_NAMES[0]:
      # run the interactive player
      p = Player.InteractivePlayer(debug=debug)
      p.run(numIters=numIters)
   elif playerName == PLAYER_NAMES[1]:
      # run the baseline greedy player
      p = Player.BaselineGreedyPlayer(debug=debug)
      p.run(numIters=numIters, printStats=True, printAtCheckpoints=True)
   elif playerName == PLAYER_NAMES[2]:
      # run the baseline corner player
      p = Player.BaselineCornerPlayer(debug=debug)
      p.run(numIters=numIters, printStats=True, printAtCheckpoints=True)
   elif playerName == PLAYER_NAMES[3]:
      # run the baseline random player
      p = Player.BaselineRandomPlayer(debug=debug)
      p.run(numIters=numIters, printStats=True, printAtCheckpoints=True)
   elif playerName == PLAYER_NAMES[4]:
      # run the expectimax player
      p = ExpectiMaxPlayer.ExpectiMaxPlayer(debug=debug, depth=depth)
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
   parser.add_argument('--debug', action='store_true',
                       help='enables debug output')
   parser.add_argument('--depth', default=DEFAULT_DEPTH,
                       help=('depth of search for expectimax, default %d' %
                             DEFAULT_DEPTH))
   args = parser.parse_args()

   main(args.player.upper(), int(args.numIters), int(args.size), args.debug,
        int(args.depth))
