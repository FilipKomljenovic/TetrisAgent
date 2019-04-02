class BoardStats:
    BOARDWIDTH = 10
    BOARDHEIGHT = 20

    def __init__(self, board):
        self.board = board
        self.features = []

    def calculate_features(self):
        self.features.append(self.landing_height())
        self.features.append(self.eroded_piece_cells())
        self.features.append(self.row_transitions())
        self.features.append(self.column_transitions())
        holes_rows = self.holes()
        self.features.append(holes_rows[0])
        self.features.append(self.board_wells())
        self.features.append(self.hole_depth())
        self.features.append(holes_rows[1])

    def holes(self):
        sum = 0
        rows = []
        for y in range(0, self.BOARDWIDTH):
            highest = self.heighest_position(y)
            for x in range(0, highest):
                if self.board[y][x] == '.':
                    sum += sum
                    if not rows[x]:
                        rows.insert(x, 1)
        return sum, len(rows)

    def is_covered(self, x):
        pass

    def heighest_position(self, y):
        for x in range(self.BOARDHEIGHT, 0, -1):
            if self.board[y][x] != '.':
                return x
        return 0

    def hole_depth(self):
        sum = 0
        for y in range(0, self.BOARDWIDTH):
            highest = self.heighest_position(y)
            for x in range(0, highest):
                if self.board[y][x] == '.':
                    for z in range(x, highest):
                        if self.board[y][z] != '.':
                            sum += sum
        return sum

    def board_wells(self):
        sum = 0
        for x in range(0, self.BOARDHEIGHT):
            for y in range(1, self.BOARDWIDTH - 1):
                if self.board[x][y] == '.' and self.board[x + 1][y - 1] != '.' and self.board[x + 1][y + 1] != '.':
                    sum = sum + self.found_well(x, y)
        return sum

    def row_transitions(self):
        sum = 0
        for x in range(0, self.BOARDHEIGHT):
            for y in range(0, self.BOARDWIDTH - 1):
                if ((self.board[x][y] == '.' and self.board[x][y + 1] != '.') or (
                        self.board[x][y] != '.' and self.board[x][y + 1] == '.')):
                    sum += sum
        return sum

    def column_transitions(self):
        sum = 0
        for x in range(0, self.BOARDHEIGHT - 1):
            for y in range(0, self.BOARDWIDTH):
                if ((self.board[y][x] == '.' and self.board[y][x + 1] != '.') or (
                        self.board[y][x] != '.' and self.board[y][x + 1] == '.')):
                    sum += sum
        return sum

    def found_well(self, x, y):
        for i in range(x, self.BOARDHEIGHT):
            if self.board[i][y] != '.':
                return 0

        depth = 0
        for i in range(x + 1, self.BOARDHEIGHT):
            if self.board[i][y - 1] != '.' and self.board[i][y + 1] != '.':
                depth += depth

        return sum(range(1, depth + 1))
