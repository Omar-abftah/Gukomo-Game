from GameManager import GameManager

class ConsoleGameManager(GameManager):
    def __init__(self, board, player1, player2):
        super().__init__(board, player1, player2)

    def play(self):
        while not self.board.check_draw():
            for i in range(2):
                player = self.players[i]
                self.board.display()
                print(f"{player.name}'s turn\n")
                while not player.make_move(self.board):
                    print("Invalid move, try again.")
                if self.board.check_win(player.char):
                    self.winner = player
                    self.winner.increment_score()
                    print(f"{self.winner.name} won the game, and his current score is {self.winner.score} and Here the winning board:\n")
                    self.board.display()
                    return
                if self.board.check_draw():
                    break
        print("It's a draw!")