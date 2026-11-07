# import problems as prb
# import algorithms as alg

# '''
# This file will contain the code needed to run a demonstration of your project. 

# For the progress report, it should contain code that shows a brief demonstration of random agents attempting to solve each problem. 

# For the final report, it should contain code that shows a brief demonstration of each algorithm attempting to solve each problem. 

# In both cases, to make sure we can grade these all in time, please ensure that each demonstration is just long enough to show some
# meaningful behavior. If your problem is chess playing, for example, you might show 5 moves from each player, where one player uses one 
# algorithm and one player uses another. If your problem is snake, you might show game long enough for the player to eat two apples or die
# (whichever comes first).
# '''

# demoGame = prb.Game(prb.TicTacToe(),alg.RandomAgent(),alg.RandomAgent())
# demoGame.playGame()

from problems import TreasureHunt
from algorithms import RandomAgent


def run_demo():
    game = TreasureHunt()
    agent = RandomAgent()

    print("TREASURE HUNT")
    print("A = Agent")
    print("T = Treasure")
    print("# = Obstacle")
    print("X = Harmful space")
    print(". = Open space")

    game.display()

    while not game.game_over:
        action = agent.choose_move(game)

        print(f"Move {game.moves + 1}: {action}")

        state, reward, game_over = game.take_action(action)

        print(f"Current state: {state}")
        print(f"Reward: {reward}")

        game.display()

    print("Game finished.")
    print(f"Total moves: {game.moves}")
    print(f"Total reward: {game.total_reward}")


if __name__ == "__main__":
    run_demo()