import timeit

import gym_tetris
from agent import Agent
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

step = 0
for i in range(10):
    agent = Agent(env.env.game.board)
    env.reset()
    next_piece = env.env.game.falling_piece
    done = False
    while not env.env.game.is_game_over:
        board = env.env.game.board
        for piece in pieces.values():
            piece.set_board(board)
        agent.set_board(board)
        piece = pieces[next_piece['shape']]
        piece.current_rotation = next_piece['rotation']
        agent.set_piece(piece)
        # access to the game board
        # print(env.env.game.board)
        step += 1
        actions = agent.make_decision()
        if len(actions) == 0:
            state, reward, done, info = env.env.game.step(0)
        for action in actions:
            state, reward, done, info = env.env.game.step(action)
            env.render('human')
            if done:
                break
        while env.env.game.falling_piece is not None and not done:
            state, reward, done, info = env.env.game.step(0)
            env.render('human')
        next_piece = env.env.game.next_piece
    step = 0
    print(agent.r)
print(step)
stop = timeit.default_timer()
print('Time: ', stop - start)
input('Press enter to stop')
