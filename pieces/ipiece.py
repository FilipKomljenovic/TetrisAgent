from pieces.piece import Piece
import copy


class IPiece(Piece):
    rotations = [0, 1]
    HEIGHT = 4
    WIDTH = 1

    def __init__(self, shape, board):
        super().__init__(shape, board)
        self.current_rotation = 0

    def fill_configurations(self, board):
        configurations = []
        # rotation 0 --> I
        for x in range(0, self.BOARDWIDTH - 2):
            configurations.append((x, x + 1, 'r0'))
        # rotation 1 --> ----
        for x in range(0, self.BOARDWIDTH - 5):
            configurations.append((x, x + 4, 'r1'))
        return configurations

    def generate_board(self, conf, board):
        new_board = copy.deepcopy(board)
        new_board = new_board[::-1]
        height = 0
        if not conf[2] == 'r0':
            self.HEIGHT = 1
            self.WIDTH = 4
        else:
            self.HEIGHT = 4
            self.WIDTH = 1

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

        else:
            pass
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
        if not self.current_rotation == conf[2]:
            actions.append(self.ROTATE_LEFT)
        if column > right:
            for i in range(right, column):
                actions.append(self.RIGHT)
        elif column < left:
            diff = left - column
            for i in range(0, diff):
                actions.append(self.LEFT)
        return actions

    def set_rotation(self, rotation):
        self.current_rotation = rotation
