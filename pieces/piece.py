from abc import abstractmethod, ABC


class Piece(ABC):
    BOARDWIDTH = 10
    BOARDHEIGHT = 20
    LEFT = 1
    RIGHT = 2
    ROTATE_LEFT = 4
    ROTATE_RIGHT = 5

    @abstractmethod
    def __init__(self, shape, board):
        self.shape = shape
        self.board = board[::-1]
        self.current_rotation = 0
        self.configurations = []

    @abstractmethod
    def fill_configurations(self, board):
        pass

    # conf contains x0, x1 coordinates and rotation
    @abstractmethod
    def generate_board(self, conf, board):
        pass

    @abstractmethod
    def generate_actions(self, column, conf):
        pass

    def set_board(self, board):
        self.board = board[::-1]
