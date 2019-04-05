from pieces.piece import Piece
import copy


class TPiece(Piece):
    rotations = [0, 1, 2, 3]
    HEIGHT = 2
    WIDTH = 3

    def __init__(self, shape, board):
        super().__init__(shape, board)

    def fill_configurations(self, board):
        configurations = []
        # rotation 0 --> T
        for x in range(0, self.BOARDWIDTH - 3):
            configurations.append((x, x + 3, '0'))
        # rotation 1 --> _|_
        for x in range(0, self.BOARDWIDTH - 3):
            configurations.append((x, x + 3, '1'))
        # rotation 2 --> -|
        for x in range(0, self.BOARDWIDTH - 2):
            configurations.append((x, x + 2, '2'))
        # rotation 3 --> |-
        for x in range(0, self.BOARDWIDTH - 2):
            configurations.append((x, x + 2, '3'))

        return configurations

    def generate_board(self, conf, board):
        new_board = copy.deepcopy(board)
        new_board = new_board[::-1]
        height = 0
        if conf[2] == '0' or conf[2] == '1':
            self.HEIGHT = 2
            self.WIDTH = 3
        else:
            self.HEIGHT = 3
            self.WIDTH = 2

        for x in range(0, self.BOARDHEIGHT):
            flag = True
            if conf[2] == '0':
                if self.board[x][conf[0] + 1] != '.' and self.board[x + 1][conf[0]] != '.' \
                        and self.board[x + 1][conf[0] + 1] != '.' and self.board[x + 1][conf[0] + 2] != '.':
                    flag = False
            elif conf[2] == '1':
                if self.board[x][conf[0]] != '.' and self.board[x][conf[0] + 1] != '.' \
                        and self.board[x][conf[0] + 2] != '.' \
                        and self.board[x + 1][conf[0] + 1] != '.':
                    flag = False
            elif conf[2] == '2':
                if self.board[x][conf[0] + 1] != '.' and self.board[x + 1][conf[0]] != '.' \
                        and self.board[x + 1][conf[0] + 1] != '.' \
                        and self.board[x + 2][conf[0] + 1] != '.':
                    flag = False
            elif conf[2] == '3':
                if self.board[x][conf[0] + 1] != '.' and self.board[x + 1][conf[0]] != '.' \
                        and self.board[x + 1][conf[0] + 1] != '.' \
                        and self.board[x + 2][conf[0]] != '.':
                    flag = False
            if flag:
                height = x
                break

        if self.can_fall(height, conf[0]):
            if conf[2] == '0':
                # change with color ID
                new_board[height][conf[0] + 1] = '1'
                new_board[height + 1][conf[0]] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
                new_board[height + 1][conf[0] + 2] = '1'
            elif conf[2] == '1':
                new_board[height][conf[0]] = '1'
                new_board[height][conf[0] + 1] = '1'
                new_board[height][conf[0] + 2] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
            elif conf[2] == '2':
                new_board[height][conf[0] + 1] = '1'
                new_board[height + 1][conf[0]] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
                new_board[height + 2][conf[0] + 1] = '1'
            else:
                new_board[height][conf[0] + 1] = '1'
                new_board[height + 1][conf[0]] = '1'
                new_board[height + 1][conf[0] + 1] = '1'
                new_board[height + 2][conf[0]] = '1'

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
        left = 5 - (self.WIDTH // 2)
        right = 5 + (self.WIDTH // 2)
        actions = []
        if not self.current_rotation == conf[2]:
            if conf[2] == '1':
                actions.append(self.ROTATE_LEFT)
                actions.append(self.ROTATE_LEFT)
            elif conf[2] == '2':
                actions.append(self.ROTATE_RIGHT)
            elif conf[2] == '3':
                actions.append(self.ROTATE_LEFT)

        if column > right:
            for i in range(right, column):
                actions.append(self.RIGHT)
        else:
            diff = right - column
            for i in range(0, diff):
                actions.append(self.LEFT)

        return actions
