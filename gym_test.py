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
for i in range(1):
    env.reset()
    # print(env.env.game.falling_piece)
    # agent.generate_configurations()
    done = False
    step = 0
    while not done:
        for piece in pieces.values():
            piece.set_board(env.env.game.board)
        agent.set_board(env.env.game.board)
        if env.env.game.falling_piece is None:
            env.env.game.falling_piece = new_piece()
        piece = pieces[env.env.game.falling_piece['shape']]
        agent.set_piece(piece)
        # access to the game board
        # print(env.env.game.board)
        step += 1
        env.render('human')
        actions = agent.make_decision()
        for action in actions:
            state, reward, done, info = env.step(action)
            if done:
                break
print(step)
stop = timeit.default_timer()
print('Time: ', stop - start)
input('Press enter to stop')
