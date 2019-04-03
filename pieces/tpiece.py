from pieces.piece import Piece


class TPiece(Piece):
    rotations = [0, 1, 2, 3]

    def __init__(self, shape, board):
        super().__init__(shape, board)

    def fill_configurations(self, board):
        configurations = []
        # rotation 0 --> T
        for x in range(0, self.BOARDWIDTH - 4):
            configurations.append((x, x + 3, 'r0'))
        # rotation 1 --> _|_
        for x in range(0, self.BOARDWIDTH - 4):
            configurations.append((x, x + 3, 'r1'))
        # rotation 2 --> -|
        for x in range(0, self.BOARDWIDTH - 3):
            configurations.append((x, x + 2, 'r2'))
        # rotation 3 --> |-
        for x in range(0, self.BOARDWIDTH - 3):
            configurations.append((x, x + 2, 'r3'))

        print(configurations)
        return configurations

# def is_under_filled(self, x, y):
#     if x == 0:
#         return True
#     if self.board[x - 1][y] == '.':
#         return False
#     return True
#
#
# def is_over(self, x, y):
#     for i in range(0, self.BOARDWIDTH):
#         if not self.board[x - 1][i] == '.':
#             return False
#     return True
