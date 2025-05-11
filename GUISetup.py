
import tkinter as tk
from tkinter import ttk
from BoardManager import Board
from GUIGameManager import GUIGameManager
from HumanPlayer import HumanPlayer
from MinMaxAI import MinMaxAI
from AlphaBetaPruningAI import AlphaBetaPruningAI

class GUISetup:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gomoku Setup")
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack()

        # Game mode selection
        tk.Label(main_frame, text="Game Mode:", font=('Arial', 12)).grid(row=0, column=0, sticky='w', pady=5)
        self.game_mode = tk.StringVar(value="1")
        ttk.Radiobutton(main_frame, text="Human vs AI", variable=self.game_mode, value="1").grid(row=1, column=0, sticky='w')
        ttk.Radiobutton(main_frame, text="AI vs AI", variable=self.game_mode, value="2").grid(row=2, column=0, sticky='w')

        # Board dimension
        tk.Label(main_frame, text="Board Dimension:", font=('Arial', 12)).grid(row=3, column=0, sticky='w', pady=5)
        self.dimension = tk.IntVar(value=15)
        ttk.Spinbox(main_frame, from_=5, to=20, textvariable=self.dimension, width=5).grid(row=4, column=0, sticky='w')

        # Player name (only for Human vs AI)
        tk.Label(main_frame, text="Player Name:", font=('Arial', 12)).grid(row=5, column=0, sticky='w', pady=5)
        self.player_name = tk.StringVar(value="Player1")
        ttk.Entry(main_frame, textvariable=self.player_name).grid(row=6, column=0, sticky='we')

        # Start button
        ttk.Button(main_frame, text="Start Game", command=self.start_game).grid(row=7, column=0, pady=20, sticky='we')

    def start_game(self):
        dim = self.dimension.get()
        mode = self.game_mode.get()

        if mode == "1":
            player1 = HumanPlayer(self.player_name.get(), 0, 'W')
            player2 = MinMaxAI("AI", 0, 'B', dim)
        elif mode == "2":
            player1 = MinMaxAI("AI1", 0, 'W', dim)
            player2 = AlphaBetaPruningAI("AI2", 0, 'B', dim)

        board = Board(dim)
        game_manager = GUIGameManager(board, player1, player2)
        self.root.destroy()
        game_manager.play()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    setup = GUISetup()
    setup.run()