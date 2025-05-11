from Player import Player

class AIPlayer(Player):
    def __init__(self, name, score, char):
        super().__init__(name, score, char)

    def make_move(self, board, *args):
        return self.run(board)

    def run(self, board):
        best_move = self.find_best_move(board)
        if best_move:
            board.update(best_move[0], best_move[1], self.char)
        return best_move

    def find_best_move(self, board):
        pass