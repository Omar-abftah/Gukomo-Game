
class Board:
    # Class constructor
    def __init__(self, dimension):
        self.dimension = dimension
        self.array = [[f'({j:02}, {i:02})' for i in range(dimension)] for j in range(dimension)]  #formating i and j with leading Zeros in case they are less than 10
        self.free_cells = (dimension-1) * (dimension-1)
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
            print("Invalid position, Please try again")
            return False
        if self.array[x][y].strip() in ["B", "W"]:
            print("Position already taken, Please try again")
            return False
        return True
    # updating the grid
    def update(self, x, y, value):
        self.array[x][y] = f"   {value}    "
        self.free_cells -= 1
        self.display()

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
            if x-i <= 0 or y+i <= 0 or self.array[x+i][y+i] != start:
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


    def check_draw(self):
        if self.free_cells == 0:
            print("Draw!")
            return True
        return False
