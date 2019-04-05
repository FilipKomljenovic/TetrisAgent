class Piece:
    BOARDWIDTH = 10
    BOARDHEIGHT = 20
    LEFT = 1
    RIGHT = 2
    ROTATE_LEFT = 4
    ROTATE_RIGHT = 5

    def __init__(self, shape, board):
        self.shape = shape
        self.board = board[::-1]
        self.current_rotation = 0

    def fill_configurations(self, board):
        pass

    # conf contains x0, x1 coordinates and rotation
    def generate_board(self, conf, board):
        pass

    def generate_actions(self, column, conf):
        pass

    def set_board(self, board):
        self.board = board[::-1]
