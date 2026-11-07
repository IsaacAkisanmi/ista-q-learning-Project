# '''
# This file will contain your the code for your problems. 
# '''

# import numpy as np
# import cv2

# class Game:
#     def __init__(self, problem, pZero, pOne,verbose=True):
#       self.problem = problem      
#       self.players = [pZero,pOne]   
#       self.verbose = verbose   
#       if self.verbose:
#          self.problem.showState()               
#     def playGame(self):
#       pCur=0
#       while self.problem.isTerminal()==False:           
#          move = self.players[pCur].getMove(self.problem)           
#          self.problem.doMove(move)
#          if self.verbose:
#             self.problem.showState()
#             print(f"Move {self.problem.ticks}:")
#             print(self.problem.state)
#          pCur = np.abs(pCur-1)
        
#       wIndex = self.problem.getWinner()
#       winner = self.players[wIndex]
#       if wIndex == -1:
#          winner = "DRAW"
#       #display final state
#       print(f"The Winner is {winner} ({wIndex})!")
#       if self.verbose:
#          self.problem.showState(4000)
#       return wIndex
              
# class TicTacToe:
#    def __init__(self):
#       self.state = np.zeros((3,3))      
#       self.ticks=-1      
#    def getLegalMoves(self, state=None):
#       if state is None:
#          state = self.state
#       moves = []
#       mark = 1
#       if np.sum(np.abs(state))%2!=0:
#          mark = -1       
#       for i in range(state.shape[0]):
#          for j in range(state.shape[1]):
#             if state[i,j]==0:
#                moves.append((mark,(i,j)))
#       return moves             
#    def getSuccessor(self, move, state):
#       mark = move[0]
#       loc = move[1]
#       state[loc] = mark
#       return state
#    def doMove(self,move):
#       self.state = self.getSuccessor(move,self.state)
#       self.ticks+=1
#    def isTerminal(self, state=None):
#       if state is None:
#          state = self.state         
#       terminal = False
#       val = self.evalTerminal(state)      
#       if val ==0 and np.sum(np.abs(state))==9:
#          terminal = True
#       if val!=0:
#          terminal = True
#       return terminal
#    def evalTerminal(self, state=None):
#       if state is None:
#          state = self.state
#       val = 0      
      
#       pZeroWins = [np.max(np.sum(state,0))==3,np.max(np.sum(state,1))==3,np.trace(state)==3,np.trace(state[:,::-1])==3]
#       pOneWins = [np.min(np.sum(state,0))==-3,np.min(np.sum(state,1))==-3,np.trace(state)==-3,np.trace(state[:,::-1])==-3]

#       if np.any(pZeroWins):
#          val = 1
#       if np.any(pOneWins):
#          val = -1
#       return val
#    def getWinner(self, state=None):
#       if state is None:
#          state = self.state
#       val = self.evalTerminal(state)
#       if val==1:
#          return 0 
#       elif val==-1:
#          return 1
#       else:
#          return -1
#    def showState(self, ms = 1000,state=None):
#       if state is None:
#          state = self.state  

#       screen = np.zeros((150,150)).astype(np.uint8)         
#       screen = cv2.line(screen,(0,49),(149,49),255) 
#       screen = cv2.line(screen,(0,99),(149,99),255)
#       screen = cv2.line(screen,(49,0),(49,149),255) 
#       screen = cv2.line(screen,(99,0),(99,149),255)

#       for i in range(state.shape[0]):
#          for j in range(state.shape[1]):
#             if state[i,j]==1:
#                screen = cv2.line(screen,(5 +j*50,5+i*50),(44+j*50,44+i*50),255,2,cv2.LINE_AA) 
#                screen = cv2.line(screen,(44+j*50,5+i*50),(5 +j*50,44+i*50),255,2,cv2.LINE_AA) 
#             if state[i,j]==-1:
#                screen = cv2.circle(screen, (25 +j*50,25+i*50), 20, 255, 2,cv2.LINE_AA) 
               
#       cv2.imshow('TicTacToe',screen)
#       cv2.waitKey(ms)

"""
problems.py

Contains the problem environments used in the project.
"""

class TreasureHunt:
    """A grid-based Treasure Hunt game."""

    def __init__(
        self,
        board_size=5,
        max_moves=20,
        obstacles=None,
        harmful_spaces=None
    ):
        # Store the game settings
        self.board_size = board_size
        self.max_moves = max_moves

        # Set the starting and treasure positions
        self.start_position = (0, 0)
        self.treasure_position = (
            board_size - 1,
            board_size - 1
        )

        # Use default obstacles if none are provided
        if obstacles is None:
            self.obstacles = {
                (0, 2),
                (1, 2),
                (3, 2)
            }
        else:
            self.obstacles = set(obstacles)

        # Use default harmful spaces if none are provided
        if harmful_spaces is None:
            self.harmful_spaces = {
                (1, 3),
                (3, 1)
            }
        else:
            self.harmful_spaces = set(harmful_spaces)

        # Create the first game episode
        self.reset()

    def reset(self):
        """Return the game to its starting condition."""

        self.agent_position = self.start_position
        self.moves = 0
        self.total_reward = 0
        self.game_over = False
        self.end_reason = ""

        return self.get_state()

    def get_state(self):
        """Return the agent's current position."""

        return self.agent_position

    def getLegalMoves(self):
        """Return the actions currently available to the agent."""

        movements = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }

        legal_moves = []

        current_row, current_column = self.agent_position

        for move, movement in movements.items():

            row_change, column_change = movement

            new_row = current_row + row_change
            new_column = current_column + column_change

            new_position = (new_row, new_column)

            # Check whether the new position is inside the board
            inside_board = (
                0 <= new_row < self.board_size
                and 0 <= new_column < self.board_size
            )

            # Check whether the new position contains an obstacle
            obstacle_free = new_position not in self.obstacles

            if inside_board and obstacle_free:
                legal_moves.append(move)

        return legal_moves

    def take_action(self, action):
        """
        Apply an action and return:

        current state, reward, and game status
        """

        if self.game_over:
            raise RuntimeError(
                "The game is over. Call reset() to begin a new game."
            )

        legal_moves = self.getLegalMoves()

        if action not in legal_moves:
            raise ValueError(
                f"{action} is not a legal move."
            )

        movements = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }

        row_change, column_change = movements[action]

        current_row, current_column = self.agent_position

        # Update the agent's position
        self.agent_position = (
            current_row + row_change,
            current_column + column_change
        )

        self.moves += 1

        # A normal move receives a small penalty
        reward = -1

        # Check whether the treasure was found
        if self.agent_position == self.treasure_position:
            reward = 100
            self.game_over = True
            self.end_reason = "Treasure found"

        # Check whether the agent entered a harmful space
        elif self.agent_position in self.harmful_spaces:
            reward = -100
            self.game_over = True
            self.end_reason = "Entered a harmful space"

        # Check whether the move limit was reached
        elif self.moves >= self.max_moves:
            self.game_over = True
            self.end_reason = "Move limit reached"

        self.total_reward += reward

        return self.get_state(), reward, self.game_over

    def display(self):
        """Print the current game board."""

        print()

        for row in range(self.board_size):

            for column in range(self.board_size):

                position = (row, column)

                if position == self.agent_position:
                    symbol = "A"

                elif position == self.treasure_position:
                    symbol = "T"

                elif position in self.obstacles:
                    symbol = "#"

                elif position in self.harmful_spaces:
                    symbol = "X"

                else:
                    symbol = "."

                print(symbol, end=" ")

            print()

        print()

    def get_result(self):
        """Return information about the current game."""

        return {
            "position": self.agent_position,
            "moves": self.moves,
            "total_reward": self.total_reward,
            "game_over": self.game_over,
            "end_reason": self.end_reason
        }
