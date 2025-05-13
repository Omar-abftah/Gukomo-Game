from Player import Player

class HumanPlayer(Player):
    def __init__(self, name, score, char):
        super().__init__(name, score, char)

    def make_move(self, board, *args):
        if len(args) == 2:
            x, y = args[0], args[1]
            if board.is_valid(x, y, self.char):
                board.update(x, y, self.char)
                return x, y
            return None
        else:
            while True:
                try:
                    coords = input("Enter the coordinates of your move separated by a space: ").split()
                    if len(coords) != 2:
                        print("Please enter exactly two numbers separated by a space.")
                        continue
                    x = int(coords[0])
                    y = int(coords[1])
                    if board.is_valid(x, y, self.char):
                        board.update(x, y, self.char)
                        return x, y
                    else:
                        print("Invalid move, try again.")
                except ValueError:
                    print("Please enter two numbers separated by a space.")