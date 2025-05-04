from Player import Player

class AIPlayer(Player):
    def __init__(self, name, score, char):
        super().__init__(name, score, char)

    def run(self, board):
        pass


    def make_move(self, board):
        if self.run(board):
            return True
        else:
            return False
