
from Player import Player

class HumanPlayer(Player):
    def __init__(self, name,score, char):
        super().__init__(name, score, char)

    def make_move(self, board):
        x,y = input("Enter the coordinates of your move separated by a space: ").split()
        x = int(x)
        y = int(y)
        if board.is_valid(x, y, self.char):
            board.update(x, y, self.char)
            board.display()
            return True
        else:
            return False