from board.board_stats import BoardStats
import random


class Agent:
    BOARDWIDTH = 10
    BOARDHEIGHT = 20

    def __init__(self, board, piece):
        self.board = board[::-1]
        self.piece = piece
        self.configurations = []
        self.weights = [random.uniform(0, 1) for _ in range(8)]
        self.board_stats = BoardStats(board)

    def print_state(self):
        print(self.board)
        print(self.piece)
        print(self.weights)

    def set_piece(self, piece):
        self.piece = piece

    def generate_configurations(self):
        self.configurations = self.piece.fill_configurations(self.board)
        return self.configurations

    def calculate_reward(self):
        for conf in self.configurations:
            new_board = self.piece.generate_board(conf, self.board)
            piece_position = conf[0], conf[1], conf[2], conf[3]
            self.board_stats.reset(new_board, piece_position)

    def make_decision(self):
        pass
