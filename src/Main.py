#!/usr/bin/python

import argparse
import time
#import yaml
import ExpectiMaxPlayer
import Model
import Player
import QLPlayer

DEFAULT_ITERS = 1
DEFAULT_DEPTH = 3
DEFAULT_PROB_CUTOFF = 1e-5
# EM <=> "EXPECTIMAX", QL <=> "Q-Learning"
PLAYER_NAMES = ['INTERACTIVE', 'GREEDY', 'CORNER', 'RANDOM', 'EM', 'QL']
DEFAULT_PLAYER_NAME = PLAYER_NAMES[0]
DEFAULT_SEQUENCES = [{}]

def generateSequenceParams(sequence, options):
   sequenceParams = {}
   for (key, defaultValue) in options:
      sequenceParams[key] = sequence[key] if key in sequence else defaultValue
   return sequenceParams

def main(sequences, playerNameArg, numItersArg, sizeArg, debugArg, depthArg,
         probCutoffArg, trainArg, loadArg, saveArg):
   """Primary test harness."""

   startTime = time.time()

   for i, sequence in enumerate(sequences):
      # setup parameters for sequence
      params = generateSequenceParams(sequence, [
         ('playerName', playerNameArg),
         ('numIters', numItersArg),
         ('size', sizeArg),
         ('debug', debugArg),
         ('depth', depthArg),
         ('probCutoff', probCutoffArg),
         ('train', trainArg),
         ('load', loadArg),
         ('save', saveArg),
      ])
      print "Running sequence %d: %s\n" % (i + 1, sequence)
      print "Full parameters: %s\n" % params

      Model.Model.SIZE = params['size']

      if params['playerName'] == PLAYER_NAMES[0]:
         # run the interactive player
         p = Player.InteractivePlayer(debug=params['debug'])
         p.run(numIters=params['numIters'])
      elif params['playerName'] == PLAYER_NAMES[1]:
         # run the baseline greedy player
         p = Player.BaselineGreedyPlayer(debug=params['debug'])
         p.run(numIters=params['numIters'], printStats=True,
               printAtCheckpoints=True)
      elif params['playerName'] == PLAYER_NAMES[2]:
         # run the baseline corner player
         p = Player.BaselineCornerPlayer(debug=params['debug'])
         p.run(numIters=params['numIters'], printStats=True,
               printAtCheckpoints=True)
      elif params['playerName'] == PLAYER_NAMES[3]:
         # run the baseline random player
         p = Player.BaselineRandomPlayer(debug=params['debug'])
         p.run(numIters=params['numIters'], printStats=True,
               printAtCheckpoints=True)
      elif params['playerName'] == PLAYER_NAMES[4]:
         # run the expectimax player
         p = ExpectiMaxPlayer.ExpectiMaxPlayer(debug=params['debug'],
                                               depth=params['depth'],
                                               probCutoff=params['probCutoff'])
         p.run(numIters=params['numIters'], printStats=True,
               printAtCheckpoints=True)
      elif params['playerName'] == PLAYER_NAMES[5]:
         # run the RL player
         p = QLPlayer.RLPlayer(debug=params['debug'], train=params['train'],
                               load=params['load'], save=params['save'])
         p.run(numIters=params['numIters'], printStats=True,
               printAtCheckpoints=True)

      runTime = time.time() - startTime
      print "\nTotal runtime after %d sequence(s): %.3f seconds" % (i + 1, runTime)

      if i != len(sequences) - 1:
         print "\n\n"

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
   parser.add_argument('--probCutoff', default=DEFAULT_PROB_CUTOFF,
                       help=('smallest exploration probability, default %f' %
                             DEFAULT_PROB_CUTOFF))
   parser.add_argument('--train', action='store_true',
                       help='runs player in training mode')
   parser.add_argument('--load', action='store_true',
                       help='loads player weights from weights.pkl')
   parser.add_argument('--save', action='store_true',
                       help='saves player weights to weights.pkl')
   parser.add_argument('--sequences',
                       help='runs custom sequences from given yaml file')
   args = parser.parse_args()

   sequences = DEFAULT_SEQUENCES
   if args.sequences:
      with open(args.sequences, 'r') as stream:
         sequences = yaml.load(stream)

   main(sequences, args.player.upper(), int(args.numIters), int(args.size),
        args.debug, int(args.depth), float(args.probCutoff), args.train, args.load,
        args.save)
