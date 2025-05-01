
class Board:
    # Class constructor
    def __init__(self, dimension):
        self.dimension = dimension
        self.array = [[f'({j:02}, {i:02})' for i in range(dimension)] for j in range(dimension)]  #formating i and j with leading Zeros in case they are less than 10
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
        self.display()

board = Board(19)
board.display()