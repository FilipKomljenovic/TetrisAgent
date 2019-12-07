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

#weights from training
WEIGHTS1 = [-12.63, 6.6, -9.22, -19.77, -13.08, -10.49, -1.61, -24.04]
WEIGHTS2 = [-1, 1, -1, -1, -4, -1, 0, 0]
WEIGHTS3 = [-13.318163804976432, 7.95160617283945, -3.6283161669334527, -10.029501634364504, -20.94470047692427,
            -5.889031489897001, -4.155242773142343, -20.541278814222448]
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
agent.weights = WEIGHTS3
start = timeit.default_timer()

step = 0
for i in range(10):
    env.reset()
    next_piece = env.env.game.falling_piece
    done = False
    while not env.env.game.is_game_over:
        board = env.env.game.board
        env.render('human')
        agent.set_board(board)
        piece = pieces[next_piece['shape']]
        piece.set_board(board)
        piece.current_rotation = next_piece['rotation']
        agent.set_piece(piece)

        step += 1
        actions = agent.make_decision()
        a = timeit.default_timer()
        env.env.game.steps(actions)

        env.render('human')
        if env.env.game.is_game_over:
            break
        state, reward, done, info = env.env.game.step(0)
        if done:
            break
        while env.env.game.falling_piece is not None and not done:
            state, reward, done, info = env.env.game.step(0)
            env.render('human')
        b = timeit.default_timer()
        next_piece = env.env.game.next_piece
    step = 0
    print(agent.r)
print(step)
stop = timeit.default_timer()
print('Time: ', stop - start)
input('Press enter to stop')
