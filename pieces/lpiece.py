from pieces.piece import Piece
import copy


class LPiece(Piece):
    rotations = [0, 1, 2, 3]
    HEIGHT = 3
    WIDTH = 2

    def __init__(self, shape, board):
        super().__init__(shape, board)
        self.current_rotation = 0

    def fill_configurations(self, board):
        configurations = []
        for x in range(0, self.BOARDWIDTH - 3):
            # rotation 0 --> L
            configurations.append((x, x + 2, 'r0'))
        for x in range(0, self.BOARDWIDTH - 4):
            # rotation 1 --> i''
            configurations.append((x, x + 3, 'r1'))
        for x in range(0, self.BOARDWIDTH - 3):
            # rotation 2 --> '|
            configurations.append((x, x + 2, 'r2'))
        for x in range(0, self.BOARDWIDTH - 4):
            # rotation 3 --> __'
            configurations.append((x, x + 3, 'r3'))
        print(configurations)
        return configurations

    def generate_board(self, conf, board):
        new_board = copy.deepcopy(board)
        height = 0
        if conf[3] == 'r1' or conf[3] == 'r3':
            self.HEIGHT = 2
            self.WIDTH = 3
        else:
            self.HEIGHT = 3
            self.WIDTH = 2

        for x in range(0, self.BOARDHEIGHT - 1):
            # change
            flag = True
            if conf[3] == 'r0':
                if self.board[x][conf[0]] != '.' and self.board[x][conf[0] + 1] != '.' \
                        and self.board[x + 1][conf[0]] != '.' and self.board[x + 2][conf[0]] != '.':
                    flag = False
            elif conf[3] == 'r1':
                if self.board[x][conf[0]] != '.' and self.board[x + 1][conf[0] + 1] != '.' \
                        and self.board[x + 1][conf[0] + 2] != '.' \
                        and self.board[x + 1][conf[0] + 1] != '.':
                    flag = False
            elif conf[3] == 'r2':
                if self.board[x][conf[0] + 1] != '.' and self.board[x + 1][conf[0] + 1] != '.' \
                        and self.board[x + 2][conf[0]] != '.' \
                        and self.board[x + 2][conf[0] + 1] != '.':
                    flag = False
            elif conf[3] == 'r3':
                if self.board[x][conf[0]] != '.' and self.board[x][conf[0] + 1] != '.' \
                        and self.board[x][conf[0] + 2] != '.' \
                        and self.board[x + 1][conf[0] + 2] != '.':
                    flag = False
            if flag:
                height = x
                break

        if self.can_fall(height, conf[0]):
            if conf[3] == 'r0':
                # change with color ID
                new_board[height][conf[0]] = '1'
                new_board[height][conf[0] + 1] = '1'
                new_board[height + 1][conf[0]] = '1'
                new_board[height + 2][conf[0]] = '1'
            elif conf[3] == 'r1':
                new_board[height][conf[0]] = '1'
                new_board[height + 1][conf[0]] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
                new_board[height + 1][conf[0] + 2] = '1'
            elif conf[3] == 'r2':
                new_board[height][conf[0] + 1] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
                new_board[height + 2][conf[0]] = '1'
                new_board[height + 2][conf[0] + 1] = '1'
            else:
                new_board[height][conf[0]] = '1'
                new_board[height][conf[0] + 1] = '1'
                new_board[height][conf[0] + 2] = '1'
                new_board[height + 1][conf[0] + 2] = '1'

        else:
            pass
        return new_board

    def can_fall(self, height, column):
        for x in range(height, self.BOARDHEIGHT - 1):
            for y in range(column, column + self.WIDTH):
                if self.board[x][y] != '.':
                    return False

    def generate_actions(self, column, conf):
        left = 5 - (self.WIDTH // 2)
        right = 5 + (self.WIDTH // 2)
        actions = []
        if not self.current_rotation == conf[3]:
            if conf[3] == 'r1':
                actions.append(self.ROTATE_RIGHT)
            elif conf[3] == 'r2':
                actions.append(self.ROTATE_RIGHT)
                actions.append(self.ROTATE_RIGHT)
            elif conf[3] == 'r3':
                actions.append(self.ROTATE_LEFT)

        if column > right:
            for i in range(right, column):
                actions.append(self.RIGHT)
        elif column < left:
            diff = left - column
            for i in range(0, diff):
                actions.append(self.LEFT)
        print(actions)
        return actions
