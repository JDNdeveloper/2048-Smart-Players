import Player
import Model

import atexit
import csv
import collections, random, math
from collections import defaultdict
import copy
import itertools
import pickle

#Algorithm
class QLearningAgent():
	def __init__(self, actions, discount, featureExtractor,
                     explorationProb=0.2, debug=False):
		self.actions = actions
		self.discount = discount
		self.featureExtractor = featureExtractor
		self.explorationProb = explorationProb
		self.debug = debug
		self.weights = {}
		self.numIters = 1
		self.overallUpdateVal = 0

	def saveWeights(self):
		if self.debug:
			print "SAVING WEIGHTS"
		with open('weights.pkl', 'wb') as outfile:
			pickle.dump(self.weights, outfile, pickle.HIGHEST_PROTOCOL)

	def loadWeights(self):
		if self.debug:
			print "LOADING WEIGHTS"
		with open('weights.pkl', 'r') as infile:
			self.weights = pickle.load(infile)

	def getQ(self, state, action):
		score = 0
		for f in self.featureExtractor(state, action):
			if f in self.weights:
				score += self.weights[f][0]
		return score

	def getAction(self, state):
		self.numIters += 1
		explorationProb = self.explorationProb
		if random.random() < self.explorationProb:
			return random.choice(self.actions())
		else:
			return max((self.getQ(state, action), action)
                                   for action in self.actions())[1]

	def getStepSize(self):
		return 1.0 / math.sqrt(self.numIters / self.numIters)

	def incorporateFeedback(self, state, action, reward, newState):
		if newState == None:
			return
		else:
			vOpt = max([self.getQ(newState, a) for a in self.actions()])
			qOpt = self.getQ(state, action)
			try:
				updateVal = math.sqrt(
                                        self.getStepSize() *
                                        (qOpt - (reward + self.discount * vOpt)))
			except:
				updateVal = -1 * math.sqrt(
                                        -1 * self.getStepSize() *
                                        (qOpt - (reward + self.discount * vOpt)))
			for f in self.featureExtractor(state, action):
				if f in self.weights:
					self.weights[f][0] -= (
                                                updateVal /
                                                math.sqrt(self.weights[f][1]))
					self.weights[f][1] += 1
				else:
					self.weights[f] = [-1 * updateVal, 1]

def featureExtractor(state, action):
	features = []
	verticalFeatures = [["ver", action, j == 0 or j == 3]
                            for j in range(len(state[0]))]
	horizontalFeatures = []
	colapsableTilesFeatures = []

	for i, row in enumerate(state):
		horizontalFeatures.append(["hor", action, i == 0 or i == 3] + row)
		for j, tile in enumerate(row):
			verticalFeatures[j].append(tile)

	for f in verticalFeatures:
		features.append(tuple(f))

	for f in horizontalFeatures:
		features.append(tuple(f))

	squareFeaturesV = [["squareV", action, s[0], s[1]]
                           for s in itertools.product(range(len(state) - 2),
                                                      range(len(state[0]) - 1))]
	squareFeaturesH = [["squareH", action, s[0], s[1]]
                           for s in itertools.product(range(len(state) - 1),
                                                      range(len(state[0]) - 2))]

	for s in squareFeaturesV:
		features.append(tuple(s + [state[s[2]][s[3]],
                                           state[s[2]][s[3] + 1],
                                           state[s[2] + 1][s[3]],
                                           state[s[2] + 1][s[3] + 1],
                                           state[s[2] + 2][s[3]],
                                           state[s[2] + 2][s[3] + 1]]))
	for s in squareFeaturesH:
		features.append(tuple(s + [state[s[2]][s[3]],
                                           state[s[2]][s[3] + 1],
                                           state[s[2] + 1][s[3]],
                                           state[s[2] + 1][s[3] + 1],
                                           state[s[2] ][s[3] + 2],
                                           state[s[2] + 1][s[3] + 2]]))

	return features

class RLPlayer(Player.Player):
	def __init__(self, debug=False, train=True, save=True):
		Player.Player.__init__(self, debug=debug)
		self.train = train
		self.save = save
		self.previousAction = None
		self.previousState = None
		self.previousScore = None
		self.rlAgent = QLearningAgent(self.getPossibleActions, 1,
					      featureExtractor, explorationProb=0,
					      debug=self.debug)
		self.totalMoves = 0
		self.bannedActions = []

		if not self.train:
			self.rlAgent.loadWeights()

		atexit.register(self._cleanup)

        def _cleanup(self):
		if self.train and self.save:
			self.rlAgent.saveWeights()

	def getMoveAndTrainModel(self, state, score):
		if self.previousState != None and self.previousAction != None:
			reward = 0
			if str(self.previousState) != str(state):
				if score - self.previousScore < 1:
					reward = (score - self.previousScore)
				else:
					reward = (score - self.previousScore)
				self.bannedActions = []

			else:
				self.bannedActions.append(self.previousAction)

			self.rlAgent.incorporateFeedback(self.previousState,
                                                         self.previousAction,
                                                         reward, state)

		action = self.rlAgent.getAction(state)
		self.previousScore = score
		self.previousAction = action
		self.previousState = copy.deepcopy(state)
		return action

	def getMoveFromTrainedModel(self, state, score):
		if (self.previousState != None and
                    str(self.previousState) != str(state)):
			self.bannedActions = []
		else:
			self.bannedActions.append(self.previousAction)
		self.previousState = copy.deepcopy(state)
		action = self.rlAgent.getAction(state)
		self.previousAction = action
		return action

	def getMove(self, state, score):
		if self.train:
			return self.getMoveAndTrainModel(state, score)
		else:
			return self.getMoveFromTrainedModel(state, score)

	def getPossibleActions(self):
		return list(set([
                	Model.Move.UP,
                	Model.Move.DOWN,
                	Model.Move.LEFT,
                	Model.Move.RIGHT
                ]) - set(self.bannedActions))
