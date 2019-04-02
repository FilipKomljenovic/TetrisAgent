class BoardStats:
    BOARDWIDTH = 10
    BOARDHEIGHT = 20

    def __init__(self, board, new_board, piece_position):
        self.board = board
        self.features = []
        self.new_board = new_board
        # tuple with y0,x0,y1,x1 coordinates of piece
        self.piece_position = piece_position

    def calculate_features(self):
        self.features = []
        self.features.append(self.landing_height())
        self.features.append(self.eroded_piece_cells())
        self.features.append(self.row_transitions())
        self.features.append(self.column_transitions())
        holes_rows = self.holes()
        self.features.append(holes_rows[0])
        self.features.append(self.board_wells())
        self.features.append(self.hole_depth())
        self.features.append(holes_rows[1])

        print(self.features)

    def set_board(self, board):
        self.board = self.new_board
        self.board = board

    def holes(self):
        sum = 0
        rows = set()
        for y in range(0, self.BOARDWIDTH):
            highest = self.heighest_position(y)
            for x in range(0, highest):
                if self.board[x][y] == '.':
                    sum += 1
            for x in range(0, self.BOARDHEIGHT):
                if self.board[x][y] == '.':
                    rows.add(x)
        return sum, len(rows)

    def heighest_position(self, y):
        for x in range(self.BOARDHEIGHT - 1, 0, -1):
            if self.board[x][y] != '.':
                return x
        return 0

    def hole_depth(self):
        sum = 0
        for y in range(0, self.BOARDWIDTH):
            highest = self.heighest_position(y)
            for x in range(0, highest):
                if self.board[x][y] == '.':
                    for z in range(x, highest):
                        if self.board[z][y] != '.':
                            sum += 1
        return sum

    def board_wells(self):
        sum = 0
        for x in range(0, self.BOARDHEIGHT - 1):
            for y in range(1, self.BOARDWIDTH - 2):
                if self.board[x][y] == '.' and self.board[x + 1][y - 1] != '.' and self.board[x + 1][y + 1] != '.':
                    sum = sum + self.found_well(x, y)
        return sum

    def row_transitions(self):
        sum = 0
        for x in range(0, self.BOARDHEIGHT):
            for y in range(0, self.BOARDWIDTH - 1):
                if ((self.board[x][y] == '.' and self.board[x][y + 1] != '.') or (
                        self.board[x][y] != '.' and self.board[x][y + 1] == '.')):
                    sum += 1
        return sum

    def column_transitions(self):
        sum = 0
        for x in range(0, self.BOARDHEIGHT):
            for y in range(0, self.BOARDWIDTH - 1):
                if ((self.board[x][y] == '.' and self.board[x][y + 1] != '.') or (
                        self.board[x][y] != '.' and self.board[x][y + 1] == '.')):
                    sum += 1
        return sum

    def found_well(self, x, y):
        for i in range(x, self.BOARDHEIGHT):
            if self.board[i][y] != '.':
                return 0

        depth = 0
        for i in range(x + 1, self.BOARDHEIGHT):
            if self.board[i][y - 1] != '.' and self.board[i][y + 1] != '.':
                depth += 1

        return sum(range(1, depth + 1))

    def landing_height(self):
        return self.piece_position[0]

    def eroded_piece_cells(self):
        eliminated_rows = 0
        eliminated_piece_parts = 0
        for i in range(self.piece_position[0], self.piece_position[2]):
            for x in range(self.BOARDWIDTH):
                if self.board[i][x] == '.':
                    break
            eliminated_rows += 1
            for x in range(self.BOARDWIDTH):
                if self.board[i][x] == '.' and self.new_board[i][x] != '.':
                    eliminated_piece_parts += 1

        return eliminated_rows * eliminated_piece_parts
