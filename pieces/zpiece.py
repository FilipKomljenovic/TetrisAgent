from pieces.piece import Piece
import copy


class ZPiece(Piece):
    rotations = [0, 1]
    HEIGHT = 3
    WIDTH = 2

    def __init__(self, shape, board):
        super().__init__(shape, board)

    def fill_configurations(self, board):
        if not len(self.configurations) == 0:
            return self.configurations
        for x in range(0, self.BOARDWIDTH - 2):
            # rotation 0 --> z
            self.configurations.append((x, x + 2, '0'))
        for x in range(0, self.BOARDWIDTH - 1):
            # rotation 1 --> .-'
            self.configurations.append((x, x + 1, '1'))

        return self.configurations

    def generate_board(self, conf, board):
        new_board = copy.deepcopy(board)
        new_board = new_board[::-1]
        height = 0
        if conf[2] == '0':
            self.HEIGHT = 2
            self.WIDTH = 3
        else:
            self.HEIGHT = 3
            self.WIDTH = 2

        for x in range(0, self.BOARDHEIGHT):
            flag = True
            if conf[2] == '0':
                if self.board[x + 1][conf[0]] != '.' and self.board[x + 1][conf[0] + 1] != '.' \
                        and self.board[x][conf[0] + 1] != '.' and self.board[x][conf[0] + 2] != '.':
                    flag = False
            elif conf[2] == '1':
                if self.board[x][conf[0]] != '.' and self.board[x + 1][conf[0]] != '.' \
                        and self.board[x + 1][conf[0] + 1] != '.' \
                        and self.board[x + 2][conf[0] + 1] != '.':
                    flag = False
            if flag:
                height = x
                break

        if self.can_fall(height, conf[0]):
            if conf[2] == '0':
                # change with color ID
                new_board[height + 1][conf[0]] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
                new_board[height][conf[0] + 1] = '1'
                new_board[height][conf[0] + 2] = '1'
            elif conf[2] == '1':
                new_board[height][conf[0]] = '1'
                new_board[height + 1][conf[0]] = '1'
                new_board[height + 2][conf[0] + 1] = '1'
                new_board[height + 1][conf[0] + 1] = '1'

        else:
            pass
        return new_board

    def can_fall(self, height, column):
        for x in range(height, self.BOARDHEIGHT):
            for y in range(column, column + self.WIDTH):
                if self.board[x][y] != '.':
                    return False
        return True

    def generate_actions(self, column, conf):
        if conf[2] == '0':
            self.HEIGHT = 2
            self.WIDTH = 3
        else:
            self.HEIGHT = 3
            self.WIDTH = 2
        left = 4
        right = 5 if self.WIDTH == 2 else 6
        actions = []
        if not self.current_rotation == int(conf[2]):
            actions.append(self.ROTATE_LEFT)

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
