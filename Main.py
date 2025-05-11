
from BoardManager import Board
from ConsoleGameManager import ConsoleGameManager
from HumanPlayer import HumanPlayer
from MinMaxAI import MinMaxAI
from AlphaBetaPruningAI import AlphaBetaPruningAI
from GUISetup import GUISetup

def main():
    print("Welcome to Gomoku Game")
    choice = input("Choose interface:\n1 - GUI\n2 - Console\nYour choice (1/2): ")

    if choice == '1':
        setup = GUISetup()
        setup.run()
    elif choice == '2':
        start_console_game()
    else:
        print("Invalid choice")

def start_console_game():
    case = input("\n1 - Human vs AI"
                 "\n2 - AI vs AI"
                 "\nType your choice here(1, 2): ")
    dim = int(input("Please enter the board dimension: "))
    player1 = None
    player2 = None
    if case == '1':
        name = input("Please enter Player1's name: ")
        player1 = HumanPlayer(name, 0, 'W')
        player2 = MinMaxAI("AI2", 0, 'B', dim)
    elif case == '2':
        player1 = MinMaxAI("AI1", 0, 'W', dim)
        player2 = AlphaBetaPruningAI("AI2", 0, 'B', dim)
    else:
        print("Invalid input")
        return

    game_manager = ConsoleGameManager(Board(dim), player1, player2)
    game_manager.play()

if __name__ == "__main__":
    main()
