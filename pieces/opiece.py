from pieces.piece import Piece


class OPiece(Piece):
    def __init__(self, shape, board):
        super().__init__(shape, board)

    def fill_configurations(self, board):
        configurations = []
        for x in range(0, self.BOARDWIDTH - 2):
            configurations.append(x)
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
