from BoardManager import Board

import Player

class HumanPlayer(Player):
    def __init__(self, name, score, char):
        super().__init__(self, name, score, char)

    def make_move(self, board):
        board.display_board()
        x,y = input("Enter the coordinates of your move separated by a space: ").split()
        if board.is_valid(x, y, self.char):
            board.update_board(x, y, self.char)
            return True
        else:
            return False