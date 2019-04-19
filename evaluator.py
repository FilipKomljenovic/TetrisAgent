import timeit

import gym_tetris
from pieces.ipiece import IPiece
from pieces.jpiece import JPiece
from pieces.lpiece import LPiece
from pieces.opiece import OPiece
from pieces.spiece import SPiece
from pieces.tpiece import TPiece
from pieces.zpiece import ZPiece


class Evaluator:
    def __init__(self, id, agent=None):
        self.agent = agent
        self.id = id
        self.games_num = 1

    def set_agent(self, agent):
        self.agent = agent

    def set_games_num(self, n):
        self.games_num = n

    def evaluate(self):
        env = gym_tetris.make("Tetris-v0")
        try:
            env.reset()
            opiece = OPiece("O", env.env.game.board)
            ipiece = IPiece("I", env.env.game.board)
            jpiece = JPiece("J", env.env.game.board)
            lpiece = LPiece("L", env.env.game.board)
            spiece = SPiece("S", env.env.game.board)
            zpiece = ZPiece("Z", env.env.game.board)
            tpiece = TPiece("T", env.env.game.board)
            pieces = {"O": opiece, "I": ipiece, "J": jpiece, "L": lpiece, "S": spiece, "Z": zpiece, "T": tpiece}
            start = timeit.default_timer()
            step = 0
            for i in range(self.games_num):
                env.reset()
                next_piece = env.env.game.falling_piece
                done = False
                while not env.env.game.is_game_over:
                    board = env.env.game.board
                    self.agent.set_board(board)
                    piece = pieces[next_piece['shape']]
                    piece.current_rotation = next_piece['rotation']
                    piece.set_board(board)
                    self.agent.set_piece(piece)
                    step += 1
                    actions = self.agent.make_decision()
                    if len(actions) == 0:
                        state, reward, done, info = env.env.game.step(0)
                    else:
                        env.env.game.steps(actions)
                    # for action in actions:
                    #     state, reward, done, info = env.env.game.step(action)
                    #     if done:
                    #         break
                    while env.env.game.falling_piece is not None and not done:
                        env.env.game._fall()

                    next_piece = env.env.game.next_piece
                print("steps:", step)
                print("r:", self.agent.r)

            print("id:", self.id)
            stop = timeit.default_timer()
            print('Time: ', stop - start)
            print('\n')
        finally:
            env.env.close()
            return self.agent.r, self.agent.weights
