import copy

from pieces.piece import Piece


class TPiece(Piece):
    rotations = [0, 1, 2, 3]
    HEIGHT = 2
    WIDTH = 3
    LEFT_SIDE_FIRST = 5
    LEFT_SIDE_SEC = 4
    RIGHT_SIDE_FIRST = 5
    RIGHT_SIDE_SEC = 6
    rotations_0 = {'0': None, '1': (Piece.ROTATE_RIGHT,), '2': (Piece.ROTATE_RIGHT, Piece.ROTATE_RIGHT),
                   '3': (Piece.ROTATE_LEFT,)}
    rotations_1 = {'0': (Piece.ROTATE_LEFT,), '1': None, '2': (Piece.ROTATE_RIGHT,),
                   '3': (Piece.ROTATE_RIGHT, Piece.ROTATE_RIGHT)}
    rotations_2 = {'0': (Piece.ROTATE_RIGHT, Piece.ROTATE_RIGHT), '1': (Piece.ROTATE_RIGHT,), '2': None,
                   '3': (Piece.ROTATE_LEFT,)}
    rotations_3 = {'0': (Piece.ROTATE_RIGHT,), '1': (Piece.ROTATE_RIGHT, Piece.ROTATE_RIGHT), '2': (Piece.ROTATE_LEFT,),
                   '3': None}

    def __init__(self, shape, board):
        super().__init__(shape, board)

    def fill_configurations(self, board):
        if not len(self.configurations) == 0:
            return self.configurations
        # rotation 0 -->  _|_
        for x in range(0, self.BOARDWIDTH - 2):
            self.configurations.append((x, x + 2, '0'))
        # rotation 1 -->  |-
        for x in range(0, self.BOARDWIDTH - 1):
            self.configurations.append((x, x + 1, '1'))
        # rotation 2 -->  T
        for x in range(0, self.BOARDWIDTH - 2):
            self.configurations.append((x, x + 2, '2'))
        # rotation 3 -->  -|
        for x in range(0, self.BOARDWIDTH - 1):
            self.configurations.append((x, x + 1, '3'))

        return self.configurations

    def generate_board(self, conf, board):
        new_board = copy.deepcopy(board)
        height = 0
        if conf[2] == '0' or conf[2] == '2':
            self.HEIGHT = 2
            self.WIDTH = 3
        else:
            self.HEIGHT = 3
            self.WIDTH = 2

        for x in range(0, self.BOARDHEIGHT):
            flag = self.check_conf(x, conf[0], conf[2])
            if flag and self.can_fall(x, conf[0], conf[2]):
                height = x
                break

        if self.can_fall(height, conf[0], conf[2]):
            if conf[2] == '0':
                # change with color ID
                new_board[height][conf[0]] = '1'
                new_board[height][conf[0] + 1] = '1'
                new_board[height][conf[0] + 2] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
            elif conf[2] == '1':
                new_board[height][conf[0]] = '1'
                new_board[height + 1][conf[0]] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
                new_board[height + 2][conf[0]] = '1'
            elif conf[2] == '2':
                new_board[height][conf[0] + 1] = '1'
                new_board[height + 1][conf[0]] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
                new_board[height + 1][conf[0] + 2] = '1'
            else:
                new_board[height][conf[0] + 1] = '1'
                new_board[height + 1][conf[0]] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
                new_board[height + 2][conf[0] + 1] = '1'

        else:
            pass
        return new_board

    def check_conf(self, x, conf, rot):
        if rot == '0':
            if x + 1 < self.BOARDHEIGHT and conf + 2 < self.BOARDWIDTH and self.board[x][conf] == '.' \
                    and self.board[x][conf + 1] == '.' \
                    and self.board[x][conf + 2] == '.' \
                    and self.board[x + 1][conf + 1] == '.':
                return True
        elif rot == '1':
            if x + 2 < self.BOARDHEIGHT and conf + 1 < self.BOARDWIDTH and self.board[x][conf] == '.' \
                    and self.board[x + 1][conf] == '.' \
                    and self.board[x + 1][conf + 1] == '.' \
                    and self.board[x + 2][conf] == '.':
                return True
        elif rot == '2':
            if x + 1 < self.BOARDHEIGHT and conf + 2 < self.BOARDWIDTH \
                    and self.board[x][conf + 1] == '.' and self.board[x + 1][conf] == '.' \
                    and self.board[x + 1][conf + 1] == '.' and self.board[x + 1][conf + 2] == '.':
                return True
        elif rot == '3':
            if x + 2 < self.BOARDHEIGHT and conf + 1 < self.BOARDWIDTH and \
                    self.board[x][conf + 1] == '.' and self.board[x + 1][conf] == '.' \
                    and self.board[x + 1][conf + 1] == '.' \
                    and self.board[x + 2][conf + 1] == '.':
                return True
        return False

    def can_fall(self, height, column, rot):
        for x in range(height, self.BOARDHEIGHT - 2):
            if not self.check_conf(x, column, rot):
                return False
        return True

    def generate_actions(self, column, conf):
        if conf[2] == '0' or conf[2] == '2':
            self.HEIGHT = 2
            self.WIDTH = 3
        else:
            self.HEIGHT = 3
            self.WIDTH = 2
        left = self.LEFT_SIDE_FIRST if conf[2] == '1' else self.LEFT_SIDE_SEC
        right = self.RIGHT_SIDE_FIRST if conf[2] == '3' else self.RIGHT_SIDE_SEC

        actions = []
        if not self.current_rotation == int(conf[2]):
            if self.current_rotation == 0:
                for i in range(0, len(self.rotations_0.get(conf[2]))):
                    actions.append(self.rotations_0.get(conf[2])[i])
            elif self.current_rotation == 1:
                for i in range(0, len(self.rotations_1.get(conf[2]))):
                    actions.append(self.rotations_1.get(conf[2])[i])
            elif self.current_rotation == 2:
                for i in range(0, len(self.rotations_2.get(conf[2]))):
                    actions.append(self.rotations_2.get(conf[2])[i])
            elif self.current_rotation == 3:
                for i in range(0, len(self.rotations_3.get(conf[2]))):
                    actions.append(self.rotations_3.get(conf[2])[i])

        if column > right:
            for i in range(right, column + self.WIDTH - 1):
                actions.append(self.RIGHT)
        elif column < left:
            for i in range(0, left - column):
                actions.append(self.LEFT)
        elif left < column <= right:
            for i in range(left, left + (column - left)):
                actions.append(self.RIGHT)

        return actions
