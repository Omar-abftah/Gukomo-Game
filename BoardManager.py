
class Board:
    # Class constructor
    def __init__(self, dimension):
        self.dimension = dimension
        self.array = [[f'({j:02}, {i:02})' for i in range(dimension)] for j in range(dimension)]  #formating i and j with leading Zeros in case they are less than 10
        self.free_cells = dimension * dimension
        self.used_black_cells = {}
        self.used_white_cells = {}

    def get_dimension(self):
        return self.dimension
    # formating the grid
    def display(self):
        print("       | " * (self.dimension-1))
        for i in range(self.dimension-1):
            print("--- ", end="")
            for j in range(self.dimension-1):
                print(self.array[i][j], end=" ")
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
        self.free_cells -= 1
        if value == "B":
            self.used_black_cells[(x,y)] = 1
        else:
            self.used_white_cells[(x,y)] = 1

    def is_white(self, x, y):
        return (x, y) in self.used_white_cells.keys()

    def is_black(self, x, y):
        return (x, y) in self.used_black_cells.keys()

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
            if x-i < 0 or y+i >= self.dimension or self.array[x-i][y+i] != start:
                return False
        return True

    def check_win(self, current_char):
        for i in range(self.dimension):
            for j in range(self.dimension):
                start = self.array[i][j].strip()
                if start == current_char:
                    if self.check_row(i, j) or self.check_left_diag(i, j) or self.check_right_diag(i, j) or self.check_col(i, j):
                        return True
        return False

    def reset_move(self, x, y):
        self.array[x][y] = f'({x:02}, {y:02})'

    def check_draw(self):
        if self.free_cells == 0:
            print("Draw!")
            return True
        return False

    def generate_move(self, current_char, max_candidates=10):
        radius = 1
        candidates = set()

        occupied = list(self.used_black_cells.keys()) + list(self.used_white_cells.keys())

        if not occupied:
            # First move: take center
            center = self.dimension // 2
            return [(center, center)]

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

        def line_score(count, player):
            if count >= 5:
                return 100000
            elif count == 4:
                return 1000
            elif count == 3:
                return 100
            elif count == 2:
                return 10
            return 0

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for x in range(self.dimension):
            for y in range(self.dimension):
                cell = self.array[x][y].strip()
                if cell not in ["B", "W"]:
                    continue
                for dx, dy in directions:
                    count = 1
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < self.dimension and 0 <= ny < self.dimension and self.array[nx][ny].strip() == cell:
                        count += 1
                        nx += dx
                        ny += dy
                    scores[cell] += line_score(count, cell)

        if ai_char == "B":
            return scores["B"] - scores["W"]
        else:
            return scores["W"] - scores["B"]




