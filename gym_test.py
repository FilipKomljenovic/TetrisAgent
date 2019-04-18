import timeit

from gym_tetris._tetris_helpers import new_piece

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
        while next_piece['shape'] != 'I':
            next_piece = new_piece()
        board = env.env.game.board
        # board = board[::-1]
        # board[0][1] = 1
        # board[0][2] = 1
        # board[0][3] = 1
        # board[0][4] = 1
        # board[0][5] = 1
        # board[0][6] = 1
        # board[1][0] = 1
        # board[1][2] = 1
        # board[1][3] = 1
        # board[1][5] = 1
        # board[1][6] = 1
        # board[1][7] = 1
        # board[1][8] = 1
        # board[1][9] = 1
        # board[2][0] = 1
        # board[2][1] = 1
        # board[2][2] = 1
        # board[2][3] = 1
        # board[2][5] = 1
        # board[2][6] = 1
        # board[2][7] = 1
        # board[3][1] = 1
        # board[3][2] = 1
        # board[3][4] = 1
        # board[3][5] = 1
        # board[3][6] = 1
        # board[3][7] = 1
        # board[3][9] = 1
        # board[4][1] = 1
        # board[4][2] = 1
        # board[4][4] = 1
        # board[4][6] = 1
        # board[4][8] = 1
        # board[4][9] = 1
        # board[5][0] = 1
        # board[5][1] = 1
        # board[5][2] = 1
        # board[5][3] = 1
        # board[5][4] = 1
        # board[5][5] = 1
        # board[5][6] = 1
        # board[5][8] = 1
        # board[6][0] = 1
        # board[6][1] = 1
        # board[6][3] = 1
        # board[6][4] = 1
        # board[6][6] = 1
        # board[6][7] = 1
        # board[6][8] = 1
        # board[6][9] = 1
        # board[7][1] = 1
        # board[7][2] = 1
        # board[7][3] = 1
        # board[7][4] = 1
        # board[7][5] = 1
        # board[7][7] = 1
        # board[7][8] = 1
        # board[7][9] = 1
        # board[8][1] = 1
        # board[8][2] = 1
        # board[8][3] = 1
        # board[8][5] = 1
        # board[8][6] = 1
        # board[8][7] = 1
        # board[8][8] = 1
        # board[8][9] = 1
        # board[9][0] = 1
        # board[9][1] = 1
        # board[9][2] = 1
        # board[9][3] = 1
        # board[9][5] = 1
        # board[9][6] = 1
        # board[9][7] = 1
        # board[9][8] = 1
        # board[9][9] = 1
        # board[10][1] = 1
        # board[10][2] = 1
        # board[10][3] = 1
        # board[10][6] = 1
        # board[10][7] = 1
        # board[10][9] = 1
        # # board[11][7] = 1
        # # board[11][9] = 1
        # # board[12][9] = 1
        # # board[13][9] = 1
        #
        # board[9][0] = 1
        # board[11][0] = 1
        # board[11][1] = 1
        # board[11][2] = 1
        # board[11][3] = 1
        # board[11][5] = 1
        # board[11][6] = 1
        # board[11][7] = 1
        # board[11][8] = 1
        # board[11][9] = 1
        #
        # board[12][2] = 1
        # board[12][3] = 1
        # board[12][6] = 1
        # board[12][7] = 1
        # board[12][8] = 1
        # board[12][9] = 1
        # board[13][7] = 1
        # board[13][9] = 1
        # board[14][9] = 1
        # board[15][9] = 1
        # board = board[::-1]
        env.render('human')
        env.env.game.step(0)
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
            if env.env.game.is_game_over:
                break
            state, reward, done, info = env.env.game.step(action)
            env.render('human')
            if done:
                break
        if env.env.game.is_game_over:
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
