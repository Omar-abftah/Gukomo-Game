from BoardManager import Board
from GameManager import GameManager
from HumanPlayer import HumanPlayer
from Player import Player
from MinMaxAI import MinMaxAI
from AlphBetaPruningAI import AlphaBetaPruningAI

def main():
    case = input("Welcome to our version of Gomoku Game"
          "\nTo play Human VS AI press 1"
          "\nTo play AI VS AI press 2"
          "\n:")
    player1 = None
    player2 = None
    if case == '1':
        name = input("Please enter Player1's name: ")
        player1 = HumanPlayer(name, 0, 'W')
        player2 = MinMaxAI("AI", 0, 'B')
    elif case == '2':
        player1 = MinMaxAI("AI1", 0, 'W')
        player2 = AlphaBetaPruningAI("AI2", 0, 'B')
    else:
        print("Invalid input")

    dim = int(input("Please enter the board dimension: "))
    game_manager = GameManager(Board(dim),player1, player2)
    game_manager.play()

if __name__ == "__main__":
    main()