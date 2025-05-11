from AIPlayer import AIPlayer
from sys import maxsize
class AlphaBetaPruningAI(AIPlayer):
    def __init__(self, name, score, char, max_depth=4):
        super().__init__(name, score, char)
        self.opponent_char = 'W' if self.char == 'B' else 'B'
        self.max_depth = max_depth

    def run(self, board):
        best_move = self.find_the_best_move(board)
        if best_move:
            board.update(best_move[0], best_move[1], self.char)
            return True
        return False

    def alpha_beta_pruning(self, board, depth, is_maximizing, alpha, beta):
        if board.check_win(self.char):
            return float('inf')
        if board.check_win(self.opponent_char):
            return -float('inf')
        if board.check_draw():
            return 0
        if depth == 0:
            return board.evaluate_board(self.char)

        current_char = self.char if is_maximizing else self.opponent_char
        moves = board.generate_move(current_char, max_candidates=100)

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
                board.update(x, y, self.opponent_char)
                score = self.alpha_beta_pruning(board, depth-1, True, alpha, beta)
                board.reset_move(x, y)
                best_value = min(best_value, score)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value

    def find_the_best_move(self, board):
        for x, y in board.generate_move(self.char, max_candidates=30):
            board.update(x, y, self.char)
            if board.check_win(self.char):
                board.reset_move(x, y)
                return x, y
            board.reset_move(x, y)
        best_score = -maxsize
        best_move = None
        moves = board.generate_move(self.char, max_candidates=100)
        for x, y in moves:
            board.update(x, y, self.char)
            score = self.alpha_beta_pruning(board, self.max_depth-1, False, -maxsize, maxsize)
            board.reset_move(x, y)
            if score > best_score or best_move is None:
                best_score = score
                best_move = (x, y)
        return best_move if best_move else (board.dimension//2, board.dimension//2)