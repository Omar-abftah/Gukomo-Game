from colorama import Fore, Style
class Board:
    # Class constructor
    def __init__(self, dimension):
        self.dimension = dimension
        self.array = [[f'({j:02}, {i:02})' for i in range(dimension + 1)] for j in range(dimension + 1)]  #formating i and j with leading Zeros in case they are less than 10
        self.last_move = None
        self.free_cells = dimension * dimension
        self.used_black_cells = set()
        self.used_white_cells = set()
        self.occupied_cells = set()

    def get_dimension(self):
        return self.dimension

    def get_cell(self, x, y):
        return self.array[x][y]

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
        print("       | " * (self.dimension))
        for i in range(self.dimension):
            print("--- ", end="")
            for j in range(self.dimension-1):
                self.print_data_of_grid(self.array[i][j], end=" ")
            print("---", end="")
            print()
        print("       | " * (self.dimension))
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
        self.occupied_cells.add((x,y))
    def is_white(self, x, y):
        return (x, y) in self.used_white_cells

    def is_black(self, x, y):
        return (x, y) in self.used_black_cells

    def reset(self):
        self.array = [[f'({j:02}, {i:02})' for i in range(self.dimension + 1)] for j in range(self.dimension + 1)]
        self.last_move = None
        self.free_cells = self.dimension * self.dimension
        self.used_black_cells = set()
        self.used_white_cells = set()
        self.occupied_cells = set()
    def check_row(self, x, y):
        start = self.array[x][y].strip()
        count = 1
        for i in range(1, 5):
            if y + i < self.dimension and self.array[x][y + i].strip() == start:
                count += 1
            else:
                break
        for i in range(1, 5):
            if y - i >= 0 and self.array[x][y - i].strip() == start:
                count += 1
            else:
                break
        return count >= 5

    def check_col(self, x, y):
        start = self.array[x][y].strip()
        count = 1
        for i in range(1, 5):
            if x + i < self.dimension and self.array[x + i][y].strip() == start:
                count += 1
            else:
                break
        for i in range(1, 5):
            if x - i >= 0 and self.array[x - i][y].strip() == start:
                count += 1
            else:
                break
        return count >= 5

    def check_right_diag(self, x, y):
        start = self.array[x][y].strip()
        count = 1
        for i in range(1, 5):
            if x + i < self.dimension and y + i < self.dimension and self.array[x + i][y + i].strip() == start:
                count += 1
            else:
                break
        for i in range(1, 5):
            if x - i >= 0 and y - i >= 0 and self.array[x - i][y - i].strip() == start:
                count += 1
            else:
                break
        return count >= 5

    def check_left_diag(self, x, y):
        start = self.array[x][y].strip()
        count = 1
        for i in range(1, 5):
            if x + i < self.dimension and y - i >= 0 and self.array[x + i][y - i].strip() == start:
                count += 1
            else:
                break
        for i in range(1, 5):
            if x - i >= 0 and y + i < self.dimension and self.array[x - i][y + i].strip() == start:
                count += 1
            else:
                break
        return count >= 5

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
        self.occupied_cells.remove((x,y))

    def check_draw(self):
        if self.free_cells == 0:
            return True
        return False
