import time
import timeit

import gym_tetris
from agent import Agent
from gym_tetris._tetris_helpers import new_piece
from pieces.ipiece import IPiece
from pieces.jpiece import JPiece
from pieces.lpiece import LPiece
from pieces.opiece import OPiece
from pieces.spiece import SPiece
from pieces.tpiece import TPiece
from pieces.zpiece import ZPiece
import copy

env = gym_tetris.make("Tetris-v0")
env.reset()
opiece = OPiece("O", env.env.game.board)
ipiece = IPiece("I", env.env.game.board)
jpiece = JPiece("J", env.env.game.board)
lpiece = LPiece("L", env.env.game.board)
spiece = SPiece("S", env.env.game.board)
zpiece = ZPiece("Z", env.env.game.board)
tpiece = TPiece("T", env.env.game.board)
pieces = {"O": opiece, "I": ipiece, "J": jpiece, "L": lpiece, "S": spiece, "Z": zpiece, "T": tpiece}

agent = Agent(env.env.game.board)

start = timeit.default_timer()

step = 0
for i in range(1):
    env.reset()
    # print(env.env.game.falling_piece)
    # agent.generate_configurations()
    done = False
    while not env.env.game.is_game_over:
        board = copy.deepcopy(env.env.game.board)
        for piece in pieces.values():
            piece.set_board(board)
        agent.set_board(board)
        falling_piece = env.env.game.falling_piece
        if env.env.game.falling_piece is None:
            env.env.game.falling_piece = new_piece()
        piece = pieces[env.env.game.falling_piece['shape']]
        piece.current_rotation=env.env.game.falling_piece['rotation']
        agent.set_piece(piece)
        # access to the game board
        # print(env.env.game.board)
        step += 1
        actions = agent.make_decision()
        for action in actions:
            state, reward, done, info = env.env.game.step(action)
            env.render('human')
            time.sleep(0.1)
            if done:
                break
        while env.env.game.falling_piece is not None:
            env.env.game._fall()
            env.render('human')
print(step)
stop = timeit.default_timer()
print('Time: ', stop - start)
input('Press enter to stop')
