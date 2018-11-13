import Player

class SmartPlayer(Player.Player):
   def getMove(self, board, score):
      """Returns the AI Agent's move given the board state and score."""
      def recurse(board, move, depth):

