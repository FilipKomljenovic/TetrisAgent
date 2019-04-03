from pieces.piece import Piece


class JPiece(Piece):
    rotations = [0, 1, 2, 3]

    def __init__(self, shape, board):
        super().__init__(shape, board)

    def fill_configurations(self, board):
        configurations = []
        for x in range(0, self.BOARDWIDTH - 3):
            configurations.append((x, x + 2, 'r0'))
        for x in range(0, self.BOARDWIDTH - 4):
            configurations.append((x, x + 3, 'r1'))
        for x in range(0, self.BOARDWIDTH - 3):
            configurations.append((x, x + 2, 'r2'))
        for x in range(0, self.BOARDWIDTH - 4):
            configurations.append((x, x + 3, 'r3'))
        print(configurations)
        return configurations
    #
    # def is_under_filled(self, x, y):
    #     if x == 0:
    #         return True
    #     if self.board[x - 1][y] == '.' and self.board[x - 1][y + 1] == '.':
    #         return False
    #     return True
    #
    # def is_over(self, x, y):
    #     for i in range(0, self.BOARDWIDTH):
    #         if not self.board[x - 1][i] == '.':
    #             return False
    #     return True
