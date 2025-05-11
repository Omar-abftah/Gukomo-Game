class MoveGenerator:
    def __init__(self, dimension):
        self.dimension = dimension

    def generate_moves(self, board_state, current_char, max_candidates=50):
        if not board_state.occupied_cells:
            center = self.dimension // 2
            return [(center, center)]

        candidates = set()

        for (x, y) in board_state.occupied_cells:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if self._is_valid_move(board_state, nx, ny):
                        candidates.add((nx, ny))

        return self._prioritize_moves(board_state, candidates, current_char, max_candidates)

    def _is_valid_move(self, board_state, x, y):
        return (0 <= x < self.dimension and
                0 <= y < self.dimension and
                (x, y) not in board_state.occupied_cells)

    def _prioritize_moves(self, board_state, candidates, current_char, max_candidates):
        opponent_char = "W" if current_char == "B" else "B"
        scored_moves = []

        for pos in candidates:
            offensive_score = self._evaluate_move_potential(board_state, pos, current_char)
            defensive_score = self._evaluate_move_potential(board_state, pos, opponent_char)

            if defensive_score >= 10000:  # block immediate win
                total_score = defensive_score * 2
            else:
                total_score = offensive_score + defensive_score

            scored_moves.append((total_score, pos))

        return [pos for (score, pos) in sorted(scored_moves, reverse=True)][:max_candidates]

    def _evaluate_move_potential(self, board_state, pos, char):
        x, y = pos
        score = 0
        for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1),
                       (-1, 0), (0, -1), (-1, -1), (-1, 1)]:
            score += self._check_direction(board_state, x, y, dx, dy, char)
        return score

    def _check_direction(self, board_state, x, y, dx, dy, char):
        count = 1
        open_ends = 0
        array = board_state.array

        i = 1
        while True:
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < self.dimension and 0 <= ny < self.dimension:
                val = array[nx][ny].strip()
                if val == char:
                    count += 1
                elif val in ["B", "W"]:
                    break
                else:
                    open_ends += 1
                    break
            else:
                break
            i += 1

        i = 1
        while True:
            nx, ny = x - dx * i, y - dy * i
            if 0 <= nx < self.dimension and 0 <= ny < self.dimension:
                val = array[nx][ny].strip()
                if val == char:
                    count += 1
                elif val in ["B", "W"]:
                    break
                else:
                    open_ends += 1
                    break
            else:
                break
            i += 1

        if count >= 5:
            return 100000
        elif count == 4 and open_ends == 2:
            return 10000
        elif count == 4 and open_ends == 1:
            return 1000
        elif count == 3 and open_ends == 2:
            return 500
        elif count == 3 and open_ends == 1:
            return 100
        elif count == 2 and open_ends == 2:
            return 50
        elif count == 2 and open_ends == 1:
            return 10
        elif count == 1 and open_ends == 2:
            return 5
        return 0
