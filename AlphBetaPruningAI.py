from AIPlayer import AIPlayer
from sys import maxsize
class AlphaBetaPruningAI(AIPlayer):
    def __init__(self, name, score, char):
        super().__init__(name, score, char)

    def run(self, board):
        (x, y) = self.find_the_best_move(board)
        board.update(x, y, self.char)
        return True

    def alpha_beta_pruning(self, board, depth, is_maximizing, alpha, beta):
        if depth == 0 or board.check_draw():
            return board.evaluate_board()
        if self.char == "B":
            human_player = 'W'
        else:
            human_player = 'B'
        moves = board.generate_move(self.char if is_maximizing else human_player, max_candidates=10)
        if is_maximizing:
            best_value = -maxsize
            for (x, y) in moves:
                board.update(x, y, self.char)
                score = self.alpha_beta_pruning(board, depth-1, False, alpha, beta)
                board.reset_move(x, y)
                best_value = max(best_value, score)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = maxsize
            for (x, y) in moves:
                board.update(x, y, human_player)
                score = self.alpha_beta_pruning(board, depth-1, True, alpha, beta)
                board.reset_move(x, y)
                best_value = min(best_value, score)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value

    def find_the_best_move(self, board):
        best_score = -maxsize
        best_move = None
        for (x, y) in board.generate_move(self.char, max_candidates=100):
            board.update(x, y, self.char)
            score = self.alpha_beta_pruning(board, 3, False, -maxsize, maxsize)
            board.reset_move(x, y)
            if score > best_score:
                best_score = score
                best_move = (x, y)
        return best_move