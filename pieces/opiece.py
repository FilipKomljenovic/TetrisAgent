from pieces.piece import Piece
import copy


class OPiece(Piece):
    HEIGHT = 2
    WIDTH = 2
    LEFT = 1
    RIGHT = 2

    # add piece color and setter

    def __init__(self, shape, board):
        super().__init__(shape, board)

    def fill_configurations(self, board):
        configurations = []
        for x in range(0, self.BOARDWIDTH - 2):
            configurations.append((x, x + self.WIDTH))

        return configurations

    def generate_board(self, conf, board):
        new_board = copy.deepcopy(board)
        new_board = new_board[::-1]
        height = 0
        for x in range(0, self.BOARDHEIGHT - 1):
            flag = True
            for i in range(conf[0], conf[1]):
                if self.board[x][i] != '.':
                    flag = False
            if flag:
                height = x
                break

        if self.can_fall(height, conf[0]):
            for x in range(height, height + self.HEIGHT):
                for y in range(conf[0], conf[1]):
                    # change with color ID
                    new_board[x][y] = '1'

        return new_board

    def can_fall(self, height, column):
        for x in range(height, self.BOARDHEIGHT - 1):
            for y in range(column, column + self.WIDTH):
                if self.board[x][y] != '.':
                    return False
        return True

    def generate_actions(self, column, conf):
        left = 5 - (self.WIDTH // 2)
        right = 5 + (self.WIDTH // 2)
        actions = []
        if column > right:
            for i in range(right, column):
                actions.append(self.RIGHT)
        elif column < left:
            diff = left - column
            for i in range(0, diff):
                actions.append(self.LEFT)

        return actions
