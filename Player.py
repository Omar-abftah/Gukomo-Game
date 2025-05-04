import BoardManager

class Player:
    def __init__(self, name,score, char):
        self.name = name
        self.score = score
        self.char = char

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score

    def get_char(self):
        return self.char

    def set_name(self, name):
        self.name = name

    def set_score(self, score):
        self.score = score

    def set_char(self, char):
        self.char = char

    def increment_score(self):
        self.score += 1

    def make_move(self, board):
        pass

