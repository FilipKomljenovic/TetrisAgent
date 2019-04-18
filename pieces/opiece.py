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
        if not len(self.configurations) == 0:
            return self.configurations
        for x in range(0, self.BOARDWIDTH - 1):
            self.configurations.append((x, x + 1))

        return self.configurations

    def generate_board(self, conf, board):
        new_board = copy.deepcopy(board)
        height = 0
        for x in range(0, self.BOARDHEIGHT):
            flag = False
            for i in range(conf[0], conf[1] + 1):
                if conf[1] + 1 <= self.BOARDWIDTH and self.board[x][i] == '.':
                    if self.can_fall(x, conf[0]):
                        flag = True
                        break
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

        return new_board

    def can_fall(self, height, column):
        for x in range(height, self.BOARDHEIGHT):
            for y in range(column, column + self.WIDTH):
                if self.board[x][y] != '.':
                    return False
        return True

    def generate_actions(self, column, conf):
        left = 4
        right = 5
        actions = []
        if column > right:
            for i in range(right, column + self.WIDTH - 1):
                actions.append(self.RIGHT)
        elif column < left:
            for i in range(0, left - column):
                actions.append(self.LEFT)
        elif column > left and column <= right:
            for i in range(left, left + (column - left)):
                actions.append(self.RIGHT)

        return actions
