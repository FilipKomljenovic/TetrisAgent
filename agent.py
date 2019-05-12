from board.board_stats import BoardStats


class Agent:
    BOARDWIDTH = 10
    BOARDHEIGHT = 20

    def __init__(self, board=[], piece=None):
        self.board = board[::-1]
        self.piece = piece
        self.configurations = []
        self.weights = [i for i in range(0, 8)]
        # [-12.63,6.6,-9.22,-19.77,-13.08,-10.49,-1.61,-24.04]
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

            self.board_stats.reset(self.board, new_board, piece_position)
            r = self.board_stats.calculate_r()
            features = self.board_stats.calculate_features()
            self.board_stats.set_board(self.board)

            for i in range(0, len(features)):
                reward += self.weights[i] * features[i]
            rewards.append((reward, conf, r))
        rewards.sort()
        return max(rewards)

    def find_piece_position(self, board, new_board):
        positions = []
        for y in range(0, self.BOARDHEIGHT):
            for x in range(0, self.BOARDWIDTH):
                if not board[y][x] == new_board[y][x]:
                    positions.append((y, x))
        x0 = self.BOARDWIDTH
        y0 = self.BOARDHEIGHT
        x1 = 0
        y1 = 0
        for pos in positions:
            if pos[0] < y0:
                y0 = pos[0]
            if pos[1] < x0:
                x0 = pos[1]
            if pos[0] > y1:
                y1 = pos[0]
            if pos[1] > x1:
                x1 = pos[1]
        return y0, x0, y1, x1

    def make_decision(self):
        self.generate_configurations()
        best = self.calculate_reward()
        self.r += best[2]
        return self.piece.generate_actions(best[1][0], best[1])

    def set_board(self, board):
        self.board = board[::-1]
        self.board_stats.set_board(board)
