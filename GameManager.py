from BoardManager import Board
class GameManager:
    def __init__(self, board, player1, player2):
        self.board = board
        self.players = [player1, player2]
        self.winner = None

    def play(self):
        while not self.board.check_draw():
            for i in range(2):
                player = self.players[i]
                while not player.make_move(self.board):
                    print("Invalid move, try again.")
                self.board.display()
                if self.board.check_win(player.char):
                    self.winner = player
                    self.winner.increment_score()
                    self.board.display()
                    print(f"{self.winner.name} won the game, and his current score is {self.winner.score}")
                    return
                if self.board.check_draw():
                    break
        print("It's a draw!")