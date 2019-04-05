import gym_tetris
import timeit
from agent import Agent
from board.board_stats import BoardStats
from pieces.opiece import OPiece

env = gym_tetris.make("Tetris-v0")
start = timeit.default_timer()
for i in range(1):
    env.reset()
    opiece = OPiece(env.env.game.falling_piece.get('shape'), env.env.game.board)
    opiece.generate_board((2, 4), env.env.game.board)
    # agent = Agent(env.env.game.board, OPiece(env.env.game.falling_piece.get('shape'), env.env.game.board))
    # agent.print_state()
    # piece = env.env.game.falling_piece
    # boards = BoardStats(env.env.game.board, env.env.game.board, (0, 1, 2, 3))
    # boards.calculate_features()
    # # agent.print_state()
    # # print(env.env.game.falling_piece)
    # # agent.generate_configurations()
    # done = False
    # step = 0
    # for i in range(0, 300):
    #     # access to the game board
    #     # print(env.env.game.board)
    #     step += 1
    #     env.render('human')
    #     # if env.env.game.falling_piece and env.env.game.falling_piece.get('shape') == 'O':
    #     #     state, reward, done, info = env.step(opiece.generate_actions(2))
    #     # else:
    #     state, reward, done, info = env.step(env.action_space.sample())
#
# boards.set_board(env.env.game.board)
# boards.calculate_features()
# print(step)
stop = timeit.default_timer()
print('Time: ', stop - start)
input('Press enter to stop')
