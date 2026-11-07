'''
This file will contain implementations of each algorithm/agent type.
'''
import random

# class RandomAgent:
#   def __str__(self):
#     return "Random Agent"
#   def getMove(self, problem):
#     moves = problem.getLegalMoves()
#     return moves[random.randrange(len(moves))]

class RandomAgent:  #define a class for agent
    def choose_move(self, game):
        legal_moves = game.getLegalMoves() #ask for all legal moves from the game
        return random.choice(legal_moves) #return a random action from the list




#References:
#youtube video - https://www.youtube.com/shorts/WMmhbltlDGc - I was able to get an idea of how the game would look like.