from board.board_stats import BoardStats
import random


class Agent:
    BOARDWIDTH = 10
    BOARDHEIGHT = 20

    def __init__(self, board, piece=None):
        self.board = board[::-1]
        self.piece = piece
        self.configurations = []
        self.weights = [random.uniform(0, 1) for _ in range(8)]
        self.board_stats = BoardStats(board)
        self.r = 0

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
        rewards = []
        for conf in self.configurations:
            new_board = self.piece.generate_board(conf, self.board)
            piece_position = self.find_piece_position(self.board, new_board)
            reward = 0
            self.board_stats.piece_position = piece_position
            self.r += self.board_stats.calculate_r()
            self.board_stats.reset(new_board, piece_position)
            features = self.board_stats.calculate_features()
            self.board_stats.set_board(self.board)

            for i in range(0, len(features)):
                reward += self.weights[i] * features[i]
            rewards.append((reward, conf))
        rewards.sort()
        return max(rewards)

    def find_piece_position(self, board, new_board):
        positions = []
        for x in range(0, self.BOARDHEIGHT - 1):
            for y in range(0, self.BOARDWIDTH - 1):
                if not board[x][y] == new_board[x][y]:
                    positions.append((x, y))
        x0 = self.BOARDHEIGHT
        y0 = self.BOARDWIDTH
        x1 = 0
        y1 = 0
        for pos in positions:
            if pos[0] < x0:
                x0 = pos[0]
            if pos[1] < y0:
                y0 = pos[1]
            if pos[0] > x1:
                x1 = pos[0]
            if pos[1] > y1:
                y1 = pos[1]
        return x0, y0, x1, y1

    def make_decision(self):
        self.generate_configurations()
        best = self.calculate_reward()
        return self.piece.generate_actions(best[1][0], best[1])

    def set_board(self, board):
        self.board = board[::-1]
        self.board_stats.set_board(board)
