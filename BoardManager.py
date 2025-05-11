from colorama import Fore, Back, Style
class Board:
    # Class constructor
    def __init__(self, dimension):
        self.dimension = dimension
        self.array = [[f'({j:02}, {i:02})' for i in range(dimension)] for j in range(dimension)]  #formating i and j with leading Zeros in case they are less than 10
        self.last_move = None
        self.free_cells = (dimension - 1) * (dimension - 1)
        self.used_black_cells = set()
        self.used_white_cells = set()

    def get_dimension(self):
        return self.dimension

    @staticmethod
    def print_data_of_grid(data, end=""):
        if data.strip() == "B":
            print(Fore.BLACK + data + Style.RESET_ALL, end=end)
        elif data.strip() == "W":
            print(Fore.LIGHTWHITE_EX + data + Style.RESET_ALL, end=end)
        else:
            print(Fore.GREEN + data + Style.RESET_ALL, end=end)

    # formating the grid
    def display(self):
        print("       | " * (self.dimension-1))
        for i in range(self.dimension-1):
            print("--- ", end="")
            for j in range(self.dimension-1):
                self.print_data_of_grid(self.array[i][j], end=" ")
            print("---", end="")
            print()
        print("       | " * (self.dimension-1))
        print("-" * ((self.dimension * 9) - 2))
    # validating if the desired Position is a good position or not
    def is_valid(self, x, y, value):
        if value not in ["B", "W"]:
            print("Invalid value, Please try again")
            return False
        if x < 0 or x >= self.dimension or y < 0 or y >= self.dimension:
            return False
        if self.array[x][y].strip() in ["B", "W"]:
            return False
        return True
    # updating the grid
    def update(self, x, y, value):
        self.array[x][y] = f"   {value}    "
        self.last_move = (x, y)
        self.free_cells -= 1
        if value == "B":
            self.used_black_cells.add((x,y))
        else:
            self.used_white_cells.add((x,y))

    def is_white(self, x, y):
        return (x, y) in self.used_white_cells

    def is_black(self, x, y):
        return (x, y) in self.used_black_cells

    def check_row(self, x, y):
        start = self.array[x][y]
        for i in range(1, 5):
            if y+i >= self.dimension or self.array[x][y+i] != start:
                return False
        return True

    def check_col(self, x, y):
        start = self.array[x][y]
        for i in range(1, 5):
            if x+i >= self.dimension or self.array[x+i][y] != start:
                return False
        return True

    def check_right_diag(self, x, y):
        start = self.array[x][y].strip()
        for i in range(1, 5):
            if x+i >= self.dimension or y+i >= self.dimension or self.array[x+i][y+i].strip() != start:
                return False
        return True

    def check_left_diag(self, x, y):
        start = self.array[x][y]
        for i in range(1, 5):
            if x+i >= self.dimension or y-i <0 or self.array[x+i][y-i] != start:
                return False
        return True

    def check_win(self, current_char):
        x, y = self.last_move[0], self.last_move[1]
        start = self.array[x][y]
        if start.strip() != current_char:
            return False
        return self.check_row(x, y) or self.check_col(x, y) or self.check_right_diag(x, y) or self.check_left_diag(x, y)


    def reset_move(self, x, y):
        self.array[x][y] = f'({x:02}, {y:02})'
        self.free_cells += 1
        if self.is_white(x, y):
            self.used_white_cells.remove((x,y))
        else:
            self.used_black_cells.remove((x,y))

    def check_draw(self):
        if self.free_cells == 0:
            return True
        return False

    def generate_move(self, current_char, max_candidates=100):
        radius = 1
        candidates = set()

        occupied = list(self.used_black_cells) + list(self.used_white_cells)

        if not occupied:
            center = self.dimension // 2
            return [(center-1, center-1)]

        for (x, y) in occupied:
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    nx, ny = x + dx, y + dy
                    if self.is_valid(nx, ny, current_char):
                        candidates.add((nx, ny))

        def move_score(pos):
            x, y = pos
            score = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.dimension and 0 <= ny < self.dimension:
                        neighbor = self.array[nx][ny].strip()
                        if neighbor == current_char:
                            score += 2
                        elif neighbor in ["B", "W"]:
                            score += 1
            return -score

        if self.free_cells >= self.dimension * self.dimension - 4:
            center = self.dimension // 2
            sorted_candidates = sorted(
                candidates, key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center)
            )
        else:
            sorted_candidates = sorted(candidates, key=move_score)

        return sorted_candidates[:max_candidates]


    def evaluate_board(self, ai_char="B"):
        scores = {
            "B": 0,
            "W": 0
        }

        def evaluate_line(count, open_ends, player):
            """Improved evaluation considering line openness"""
            if count >= 5:
                return 100000  # Immediate win
            elif count == 4:
                if open_ends == 2: return 10000  # Open four (can win next move)
                if open_ends == 1: return 1000   # Semi-open four
            elif count == 3:
                if open_ends == 2: return 500    # Open three (potential to make open four)
                if open_ends == 1: return 100    # Semi-open three
            elif count == 2:
                if open_ends == 2: return 50     # Open two
                if open_ends == 1: return 10     # Semi-open two
            return 0

        # Only need to check 4 directions to avoid double counting
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for x in range(self.dimension):
            for y in range(self.dimension):
                cell = self.array[x][y].strip()
                if cell not in ["B", "W"]:
                    continue

                for dx, dy in directions:
                    # Check if we're at the start of a potential line
                    prev_x, prev_y = x - dx, y - dy
                    if (0 <= prev_x < self.dimension and 0 <= prev_y < self.dimension and
                            self.array[prev_x][prev_y].strip() == cell):
                        continue  # Skip if not the start of a line

                    count = 1
                    open_ends = 0

                    # Check space before the line
                    if not (0 <= prev_x < self.dimension and 0 <= prev_y < self.dimension) or \
                            self.array[prev_x][prev_y].strip() == " ":
                        open_ends += 1

                    # Count consecutive stones
                    nx, ny = x + dx, y + dy
                    while (0 <= nx < self.dimension and 0 <= ny < self.dimension and
                           self.array[nx][ny].strip() == cell):
                        count += 1
                        nx += dx
                        ny += dy

                    # Check space after the line
                    if not (0 <= nx < self.dimension and 0 <= ny < self.dimension) or \
                            self.array[nx][ny].strip() == " ":
                        open_ends += 1

                    # Only evaluate lines of length < 5 (5 is handled in win check)
                    if count < 5:
                        scores[cell] += evaluate_line(count, open_ends, cell)

        # Add positional bonuses (center control)
        center = self.dimension // 2
        for x in range(self.dimension):
            for y in range(self.dimension):
                cell = self.array[x][y].strip()
                if cell in ["B", "W"]:
                    distance_to_center = abs(x - center) + abs(y - center)
                    scores[cell] += (self.dimension - distance_to_center) * 2

        if ai_char == "B":
            return scores["B"] - scores["W"]
        else:
            return scores["W"] - scores["B"]


