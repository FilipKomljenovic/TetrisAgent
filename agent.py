class Agent:
    BOARDWIDTH = 10
    BOARDHEIGHT = 20

    def __init__(self, board, piece):
        self.board = board
        self.piece = piece

    def print_state(self):
        print(self.board)
        print(self.piece)

    def set_piece(self,piece):
        self.piece=piece

    def generate_configurations(self):
        return self.piece.fill_configurations(self.board)
        '''if shape=='O':
            print('tu sam shape 0')
            for x in range(0,self.BOARDHEIGHT):
                for y in range(0,self.BOARDWIDTH):
                    if(self.board[x][y]=='.'and self.board[x][y+1]=='.'and
                        self.board[x+1][y]=='.'and self.board[x+1][y+1]=='.' and is_under_filled(x,y)):
                        print('ispod ima nešto i mogu doc tu')
                        configurations.append((y,y+1))
        if shape=='I':
            print('tu sam shape I')
            for x in range(0,self.BOARDHEIGHT,2):
                for y in range(0,self.BOARDWIDTH,2):
                    if(self.board[y]=='.'and self.board[y+1]=='.'and
                        self.board[x]=='.'and self.board[x+1]=='.'):
                        configurations.append((x,y))
        '''
