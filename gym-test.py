import gym_tetris
import timeit
from agent import Agent
from opiece import OPiece

env = gym_tetris.make("Tetris-v0")
start = timeit.default_timer()
for i in range(1000):
    env.reset()
    agent = Agent(env.env.game.board, OPiece(env.env.game.falling_piece.get('shape'),env.env.game.board))
    piece = env.env.game.falling_piece
    if not env.env.game.falling_piece.get('shape') == 'O':
        continue
    # agent.print_state()
    # print(env.env.game.falling_piece)
    agent.generate_configurations()
    done = False
    step = 0
    while not done:
        # access to the game board
        # print(env.env.game.board)
        step += 1
        env.render('human')
        state, reward, done, info = env.step(env.action_space.sample())
print(step)
stop = timeit.default_timer()
print('Time: ', stop - start)
