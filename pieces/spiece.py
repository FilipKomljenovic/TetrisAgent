from pieces.piece import Piece


class SPiece(Piece):
    rotations = [0, 1]
    HEIGHT = 2
    WIDTH = 3
    LEFT_SIDE_FIRST = 5
    LEFT_SIDE_SEC = 4
    RIGHT_SIDE = 6

    def __init__(self, shape, board):
        super().__init__(shape, board)

    def fill_configurations(self, board):
        if not len(self.configurations) == 0:
            return self.configurations
        for x in range(0, self.BOARDWIDTH - 2):
            # rotation 0 --> s
            self.configurations.append((x, x + 2, '0'))
        for x in range(0, self.BOARDWIDTH - 1):
            # rotation 1 --> 4
            self.configurations.append((x, x + 1, '1'))

        return self.configurations

    def generate_board(self, conf, board):
        new_board = [i[:] for i in board]
        height = 0
        if conf[2] == '0':
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
            if conf[2] == '0' and height + 1 < self.BOARDHEIGHT:
                # change with color ID
                new_board[height][conf[0]] = '1'
                new_board[height][conf[0] + 1] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
                new_board[height + 1][conf[0] + 2] = '1'
            elif conf[2] == '1' and height + 2 < self.BOARDHEIGHT:
                new_board[height][conf[0] + 1] = '1'
                new_board[height + 1][conf[0]] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
                new_board[height + 2][conf[0]] = '1'

        else:
            pass
        return new_board

    def can_fall(self, height, column, rot):
        for x in range(height, self.BOARDHEIGHT - 2):
            if not self.check_conf(x, column, rot):
                return False
        return True

    def check_conf(self, x, conf, rot):
        if rot == '0':
            if x + 1 < self.BOARDHEIGHT and conf + 2 < self.BOARDWIDTH and self.board[x][conf] == '.' and \
                    self.board[x][conf + 1] == '.' \
                    and self.board[x + 1][conf + 1] == '.' and self.board[x + 1][conf + 2] == '.':
                return True
        elif rot == '1':
            if x + 2 < self.BOARDHEIGHT and conf + 1 < self.BOARDWIDTH and self.board[x][conf + 1] == '.' \
                    and self.board[x + 1][conf] == '.' \
                    and self.board[x + 1][conf + 1] == '.' \
                    and self.board[x + 2][conf] == '.':
                return True
        return False

    def generate_actions(self, column, conf):
        if conf[2] == '0':
            self.HEIGHT = 2
            self.WIDTH = 3
        else:
            self.HEIGHT = 3
            self.WIDTH = 2
        left = self.LEFT_SIDE_FIRST if self.WIDTH == 2 else self.LEFT_SIDE_SEC
        right = self.RIGHT_SIDE

        actions = []
        if not self.current_rotation == int(conf[2]):
            actions.append(self.ROTATE_RIGHT)
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
