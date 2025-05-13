class BoardEvaluator:
    def __init__(self, dimension):
        self.dimension = dimension
        self.pattern_values = {
            # Player patterns
            (5,): float('inf'),             # Win
            (4, 2): 10000,                  # Open four
            (4, 1): 1000,                   # Semi-open four
            (3, 2): 500,                    # Open three
            (3, 1): 100,                    # Semi-open three
            (2, 2): 50,                     # Open two
            (2, 1): 10,                     # Semi-open two
            # Opponent patterns (negative)
            (5, '_opponent'): -float('inf'),
            (4, 2, '_opponent'): -10000,
            (4, 1, '_opponent'): -1000,
            (3, 2, '_opponent'): -500,
            (3, 1, '_opponent'): -100,
            (2, 2, '_opponent'): -50,
            (2, 1, '_opponent'): -10
        }

    def evaluate(self, board_state, ai_char):
        total_score = 0
        total_score += self._calculate_center_control(board_state, ai_char)
        total_score += self._evaluate_patterns(board_state, ai_char)
        total_score += self._calculate_mobility(board_state, ai_char)
        return total_score

    def _calculate_center_control(self, board_state, ai_char):
        center = self.dimension // 2
        score = 0
        for x in range(max(0, center - 2), min(self.dimension, center + 3)):
            for y in range(max(0, center - 2), min(self.dimension, center + 3)):
                if (x, y) in board_state.occupied_cells:
                    cell_char = board_state.get_cell(x, y)
                    distance = abs(x - center) + abs(y - center)
                    score += (5 - distance) * (2 if cell_char == ai_char else -2)
        return score

    def _evaluate_patterns(self, board_state, ai_char):
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        visited = set()

        for x in range(self.dimension):
            for y in range(self.dimension):
                cell = board_state.get_cell(x, y)
                if cell not in ['B', 'W']:
                    continue

                for dx, dy in directions:
                    key = (x, y, dx, dy)
                    if key in visited:
                        continue
                    visited.add(key)
                    pattern = self._detect_pattern(board_state, x, y, dx, dy, cell)
                    if pattern:
                        pattern_key = pattern + (('_opponent',) if cell != ai_char else ())
                        score += self.pattern_values.get(pattern_key, 0)
        return score

    def _detect_pattern(self, board_state, x, y, dx, dy, cell_char):
        length = 1
        open_ends = 0
        dimension = self.dimension
        get_cell = board_state.get_cell

        # Forward
        nx, ny = x + dx, y + dy
        while 0 <= nx < dimension and 0 <= ny < dimension:
            if get_cell(nx, ny) == cell_char:
                length += 1
                nx += dx
                ny += dy
            else:
                if get_cell(nx, ny) not in ['B', 'W']:
                    open_ends += 1
                break

        nx, ny = x - dx, y - dy
        while 0 <= nx < dimension and 0 <= ny < dimension:
            if get_cell(nx, ny) == cell_char:
                length += 1
                nx -= dx
                ny -= dy
            else:
                if get_cell(nx, ny) not in ['B', 'W']:
                    open_ends += 1
                break

        if length < 2:
            return None

        return (length, open_ends)

    def _calculate_mobility(self, board_state, ai_char):
        opponent_char = 'W' if ai_char == 'B' else 'B'
        ai_moves = len(self._get_potential_moves(board_state, ai_char))
        opponent_moves = len(self._get_potential_moves(board_state, opponent_char))
        return (ai_moves - opponent_moves) * 0.5

    def _get_potential_moves(self, board_state, player_char):
        moves = set()
        radius = 1
        for (x, y) in board_state.occupied_cells:
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.dimension and 0 <= ny < self.dimension and
                            (nx, ny) not in board_state.occupied_cells and
                            board_state.get_cell(nx, ny) not in ["B", "W"]):
                        moves.add((nx, ny))
        return moves
