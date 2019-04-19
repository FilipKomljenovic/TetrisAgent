from pieces.piece import Piece
import copy


class IPiece(Piece):
    rotations = [0, 1]
    HEIGHT = 4
    WIDTH = 1
    LEFT_SIDE_FIRST = 3
    LEFT_SIDE_SEC = 5
    RIGHT_SIDE_FIRST = 6
    RIGHT_SIDE_SEC = 5

    def __init__(self, shape, board):
        super().__init__(shape, board)

    def fill_configurations(self, board):
        if not len(self.configurations) == 0:
            return self.configurations
        # rotation 0 --> I
        for x in range(0, self.BOARDWIDTH):
            self.configurations.append((x, x, '0'))
        # rotation 1 --> ----
        for x in range(0, self.BOARDWIDTH - 3):
            self.configurations.append((x, x + 3, '1'))
        return self.configurations

    def generate_board(self, conf, board):
        new_board = copy.deepcopy(board)
        height = 0
        if not conf[2] == '0':
            self.HEIGHT = 1
            self.WIDTH = 4
        else:
            self.HEIGHT = 4
            self.WIDTH = 1

        for x in range(0, self.BOARDHEIGHT - 1):
            flag = False
            for i in range(conf[0], conf[1] + 1):
                if conf[1] < self.BOARDWIDTH and self.board[x][i] == '.':
                    if self.can_fall(x, conf[0]):
                        flag = True
            if flag:
                height = x
                break

        if self.can_fall(height, conf[0]):
            max_height = height + self.HEIGHT
            if max_height > self.BOARDHEIGHT:
                max_height = self.BOARDHEIGHT
            for x in range(height, max_height):
                for y in range(conf[0], conf[1] + 1):
                    # change with color ID
                    new_board[x][y] = '1'

        else:
            pass
        return new_board

    def can_fall(self, height, column):
        for x in range(height, self.BOARDHEIGHT - 1):
            for y in range(column, column + self.WIDTH):
                if y < self.BOARDWIDTH and self.board[x][y] != '.':
                    return False
        return True

    def generate_actions(self, column, conf):
        if not conf[2] == '0':
            self.HEIGHT = 1
            self.WIDTH = 4
        else:
            self.HEIGHT = 4
            self.WIDTH = 1
        left = self.LEFT_SIDE_FIRST if conf[2] == '1' else self.LEFT_SIDE_SEC
        right = self.RIGHT_SIDE_FIRST if conf[2] == '1' else self.RIGHT_SIDE_SEC

        actions = []
        if not self.current_rotation == int(conf[2]):
            actions.append(self.ROTATE_LEFT)
            if conf[2] == '1':
                left = 3
                right = 6
        if column > right:
            for i in range(right, column):
                actions.append(self.RIGHT)
        elif column < left:
            for i in range(0, left - column):
                actions.append(self.LEFT)
        elif left < column <= right:
            for i in range(left, left + (column - left)):
                actions.append(self.RIGHT)
        return actions

    def set_rotation(self, rotation):
        self.current_rotation = rotation
