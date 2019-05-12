from gym_tetris._tetris_helpers import remove_complete_lines


class BoardStats:
    BOARDWIDTH = 10
    BOARDHEIGHT = 20

    def __init__(self, board, old_board=None, piece_position=None):
        self.board = [i[:] for i in board]
        self.features = []
        if old_board is not None:
            self.old_board = old_board[::-1]
        else:
            self.old_board = old_board
        # tuple with y0,x0,y1,x1 coordinates of piece
        self.piece_position = piece_position

    def calculate_features(self):
        self.features.append(self.row_transitions())
        self.features.append(self.column_transitions())
        h, rwh, hd = self.holes()
        self.features.append(h)
        self.features.append(self.board_wells())
        self.features.append(hd)
        self.features.append(rwh)

        return self.features

    def reset(self, old_board, board, piece_position):
        self.old_board = old_board
        self.board = [i[:] for i in board]
        self.piece_position = piece_position

    def set_board(self, board):
        self.board = board

    def holes(self):
        sum = 0
        rows = set()
        highest = {i: False for i in range(self.BOARDWIDTH)}
        depth = [0] * self.BOARDWIDTH
        holedepth = 0
        for x in range(self.BOARDHEIGHT - 2, -1, -1):
            for y in range(0, self.BOARDWIDTH):
                if highest[y]:
                    if self.board[x][y] == '.':
                        sum += 1
                        rows.add(x)
                        if self.board[x + 1][y] != '.':
                            holedepth += depth[y]
                            depth[y] = 0
                elif self.board[x][y] != '.':
                    depth[y] += 1
                    highest[y] = True
        return sum, len(rows), holedepth

    def rows_with_holes(self):
        sum = 0
        for x in range(0, self.BOARDHEIGHT - 1):
            for y in range(0, self.BOARDWIDTH):
                if self.board[x][y] == '.' and self.board[x + 1][y] != '.':
                    sum += 1
                    break
        return sum

    def highest_position(self, y):
        for x in range(self.BOARDHEIGHT - 1, 0, -1):
            if self.board[x][y] != '.':
                return self.BOARDHEIGHT - x
        return self.BOARDHEIGHT

    def hole_depth(self):
        sum = 0
        for y in range(0, self.BOARDWIDTH):
            for x in range(0, self.BOARDHEIGHT):
                if self.board[x][y] == '.':
                    for z in range(x + 1, self.BOARDHEIGHT):
                        if self.board[z][y] != '.':
                            sum += 1
                        else:
                            break

        return sum

    def board_wells(self):
        sum = 0
        for y in range(0, self.BOARDWIDTH):
            for x in range(0, self.BOARDHEIGHT - 1):
                if y == 0:
                    if self.board[x][y] == '.' and self.board[x][y + 1] != '.':
                        pts = self.found_well(x, y)
                        if pts != 0:
                            sum += pts
                            break
                elif y == self.BOARDWIDTH - 1:
                    if self.board[x][y] == '.' and self.board[x][y - 1] != '.':
                        pts = self.found_well(x, y)
                        if pts != 0:
                            sum += pts
                            break
                elif self.board[x][y] == '.' and self.board[x][y - 1] != '.' and self.board[x][y + 1] != '.':
                    pts = self.found_well(x, y)
                    if pts != 0:
                        sum += pts
                        break
        return sum

    def row_transitions(self):
        sum = 0
        highest = 0
        for i in range(0, self.BOARDWIDTH):
            temp = self.highest_position(i)
            if temp > highest:
                highest = temp
        for x in range(0, highest):
            for y in range(0, self.BOARDWIDTH):
                if y == 0 or y == self.BOARDWIDTH - 1:
                    if self.board[x][y] == '.':
                        sum += 1
                        continue
                elif ((self.board[x][y] != '.' and self.board[x][y + 1] == '.') or (
                        self.board[x][y] != '.' and self.board[x][y - 1] == '.')):
                    sum += 1
        return sum

    def column_transitions(self):
        sum = 0
        for x in range(0, self.BOARDHEIGHT):
            for y in range(0, self.BOARDWIDTH):
                if x == 0:
                    if self.board[x][y] == '.':
                        sum += 1
                        continue
                if x == self.BOARDHEIGHT - 1:
                    continue
                elif ((self.board[x][y] != '.' and self.board[x + 1][y] == '.') or (
                        self.board[x][y] != '.' and self.board[x - 1][y] == '.')):
                    sum += 1
        return sum

    def found_well(self, x, y):
        depth = 1
        for i in range(x + 1, self.BOARDHEIGHT):
            if self.board[i][y] != '.':
                return 0
        for i in range(x + 1, self.BOARDHEIGHT):
            if y == 0:
                if self.board[i][y + 1] != '.':
                    depth += 1
                else:
                    break
            elif y == self.BOARDWIDTH - 1:
                if self.board[i][y - 1] != '.':
                    depth += 1
                else:
                    break
            elif self.board[i][y - 1] != '.' and self.board[i][y + 1] != '.':
                depth += 1
            else:
                break

        return sum(range(1, depth + 1))

    def landing_height(self):
        return self.piece_position[2] + 1

    def eroded_piece_cells(self):
        eliminated_rows = 0
        eliminated_piece_parts = 0
        for i in range(self.piece_position[0], self.piece_position[2] + 1):
            row_cleared = True
            for x in range(self.BOARDWIDTH):
                if self.board[i][x] == '.':
                    row_cleared = False
                    break
            if row_cleared:
                eliminated_rows += 1
                for x in range(self.BOARDWIDTH):
                    if self.old_board[i][x] == '.' and self.board[i][x] != '.':
                        eliminated_piece_parts += 1

        return eliminated_rows * eliminated_piece_parts

    def calculate_r(self):
        self.features = []
        self.features.append(self.landing_height())
        self.features.append(self.eroded_piece_cells())
        return self.clear_filled_rows()

    def clear_filled_rows(self):
        return remove_complete_lines(self.board[::-1])
