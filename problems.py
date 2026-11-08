# '''
# This file will contain your the code for your problems. 
# '''

"""
problems.py

"""
import random

class TreasureHunt:
   

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

    def reset(self):  #Return the game to its starting condition

        self.agent_position = self.start_position
        self.moves = 0
        self.total_reward = 0
        self.game_over = False
        self.end_reason = ""

        return self.get_state()

    def get_state(self):  #Return the agent's current position.
       

        return self.agent_position

    def getLegalMoves(self):   #Return the actions currently available to the agent.
       

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

    def take_action(self, action): #Apply an action and return
        
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

    def display(self):  #Print the current game board.
        
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

    def get_result(self): #Return information about the current game.
       
        return {
            "position": self.agent_position,
            "moves": self.moves,
            "total_reward": self.total_reward,
            "game_over": self.game_over,
            "end_reason": self.end_reason
        }


#snake game


class SnakeGame: # grid-based Snake game implementation
    
    def __init__(self, board_size=4, max_moves=30):

        if board_size < 4:
            raise ValueError("The Snake board must be at least 4 by 4.")

        self.board_size = board_size
        self.max_moves = max_moves

        self.movements = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }

        self.opposite_directions = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        self.reset()

    def reset(self): #Return the game to its starting point
        
        center_row = self.board_size // 2
        center_column = self.board_size // 2

        # The first position is the head
        self.snake = [
            (center_row, center_column),
            (center_row, center_column - 1)
        ]

        self.direction = "RIGHT"
        self.moves = 0
        self.score = 0
        self.total_reward = 0
        self.game_over = False
        self.end_reason = ""

        self.food_position = self.place_food()

        return self.get_state()

    def get_state(self):
        
        return (
            tuple(self.snake),
            self.food_position,
            self.direction
        )

    def place_food(self):  #Return a random empty position for the food, or None if the board is full.
        

        empty_positions = []

        for row in range(self.board_size):
            for column in range(self.board_size):

                position = (row, column)

                if position not in self.snake:
                    empty_positions.append(position)

        if not empty_positions:
            return None

        return random.choice(empty_positions)

    def calculate_new_head(self, action): #Return the new head position after applying an action.
       

        row_change, column_change = self.movements[action]

        current_row, current_column = self.snake[0]

        new_head = (
            current_row + row_change,
            current_column + column_change
        )

        return new_head

    def hits_wall(self, position):  #return True if a position is outside the board.

        row, column = position

        return not (
            0 <= row < self.board_size
            and 0 <= column < self.board_size
        )

    def hits_body(self, position, eating_food=False): #return True if a position collides with the snake.
       
        if eating_food:
            body_positions = self.snake
        else:
            # The tail moves away during a normal move
            body_positions = self.snake[:-1]

        return position in body_positions

    def getLegalMoves(self):  #Return the moves currently available to the snake
        
        if self.game_over:
            return []

        possible_moves = []

        opposite_direction = self.opposite_directions[self.direction]

        for action in self.movements:

            # Prevent the snake from reversing directly into itself
            if action != opposite_direction:
                possible_moves.append(action)

        safe_moves = []

        for action in possible_moves:

            new_head = self.calculate_new_head(action)

            eating_food = new_head == self.food_position

            wall_collision = self.hits_wall(new_head)

            body_collision = self.hits_body(
                new_head,
                eating_food
            )

            if not wall_collision and not body_collision:
                safe_moves.append(action)

        # Exclude fatal moves whenever safe moves are available
        if safe_moves:
            return safe_moves

        # If every move is fatal, allow the agent to select one
        return possible_moves

    def take_action(self, action):
        """Apply one Snake action."""

        if self.game_over:
            raise RuntimeError(
                "The game is over. Call reset() to begin a new game."
            )

        legal_moves = self.getLegalMoves()

        if action not in legal_moves:
            raise ValueError(
                f"{action} is not a legal move."
            )

        self.direction = action
        self.moves += 1

        new_head = self.calculate_new_head(action)

        eating_food = new_head == self.food_position

        wall_collision = self.hits_wall(new_head)

        body_collision = self.hits_body(
            new_head,
            eating_food
        )

        if wall_collision:
            reward = -100
            self.game_over = True
            self.end_reason = "The snake hit a wall."

        elif body_collision:
            reward = -100
            self.game_over = True
            self.end_reason = "The snake hit its body."

        else:
            # Insert the new head at the beginning
            self.snake.insert(0, new_head)

            if eating_food:
                reward = 100
                self.score += 1

                self.food_position = self.place_food()

                if self.food_position is None:
                    self.game_over = True
                    self.end_reason = "The snake filled the board."

            else:
                reward = -1

                # Remove the tail during a normal move
                self.snake.pop()

            if not self.game_over and self.moves >= self.max_moves:
                self.game_over = True
                self.end_reason = "The snake reached the move limit."

        self.total_reward += reward

        return self.get_state(), reward, self.game_over

    def display(self):  #Print the Snake board.
    
    
        print()

        for row in range(self.board_size):

            for column in range(self.board_size):

                position = (row, column)

                if position == self.snake[0]:
                    symbol = "H"

                elif position in self.snake[1:]:
                    symbol = "o"

                elif position == self.food_position:
                    symbol = "F"

                else:
                    symbol = "."

                print(symbol, end=" ")

            print()

        print()

    def get_result(self): #Return information about the current game.
        

        return {
            "moves": self.moves,
            "score": self.score,
            "total_reward": self.total_reward,
            "game_over": self.game_over,
            "end_reason": self.end_reason
        }
