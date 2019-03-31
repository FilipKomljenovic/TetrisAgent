from piece import Piece


class OPiece(Piece):
    def __init__(self, shape, board):
        self.shape = shape
        self.board = board

    def fill_configurations(self, board):
        configurations = []
        for x in range(0, self.BOARDHEIGHT - 1):
            if x > 0 and self.is_over(x, y):
                print(configurations)
                return configurations
            for y in range(0, self.BOARDWIDTH - 1):
                if (self.is_under_filled(x, y) and self.board[x][y] == '.' and self.board[x][y + 1] == '.' and
                        self.board[x + 1][y] == '.' and self.board[x + 1][y + 1] == '.'):
                    configurations.append((x, y))
        print(configurations)
        return configurations

    def is_under_filled(self, x, y):
        if x == 0:
            return True
        if self.board[x - 1][y] == '.' and self.board[x - 1][y + 1] == '.':
            return False
        return True

    def is_over(self, x, y):
        for i in range(0, self.BOARDWIDTH):
            if not self.board[x - 1][i] == '.':
                return False
        return True
