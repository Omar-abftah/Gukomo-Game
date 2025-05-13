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

        tk.Label(main_frame, text="Game Mode:", font=('Arial', 12)).grid(row=0, column=0, sticky='w', pady=5)
        self.game_mode = tk.StringVar(value="0")

        ttk.Radiobutton(main_frame, text="Human vs Human", variable=self.game_mode, value="0",
                        command=self.update_name_fields).grid(row=1, column=0, sticky='w')
        ttk.Radiobutton(main_frame, text="Human vs AI", variable=self.game_mode, value="1",
                        command=self.update_name_fields).grid(row=2, column=0, sticky='w')
        ttk.Radiobutton(main_frame, text="AI vs AI", variable=self.game_mode, value="2",
                        command=self.update_name_fields).grid(row=3, column=0, sticky='w')


        tk.Label(main_frame, text="Board Dimension:", font=('Arial', 12)).grid(row=4, column=0, sticky='w', pady=5)
        self.dimension = tk.IntVar(value=15)
        ttk.Spinbox(main_frame, from_=5, to=20, textvariable=self.dimension, width=5).grid(row=5, column=0, sticky='w')


        self.name_frame1 = tk.Frame(main_frame)
        self.name_frame2 = tk.Frame(main_frame)


        tk.Label(self.name_frame1, text="Player 1 Name:", font=('Arial', 12)).grid(row=0, column=0, sticky='w', pady=5)
        self.player1_name = tk.StringVar(value="Player1")
        ttk.Entry(self.name_frame1, textvariable=self.player1_name).grid(row=0, column=1, sticky='we')

        tk.Label(self.name_frame2, text="Player 2 Name:", font=('Arial', 12)).grid(row=0, column=0, sticky='w', pady=5)
        self.player2_name = tk.StringVar(value="Player2")
        ttk.Entry(self.name_frame2, textvariable=self.player2_name).grid(row=0, column=1, sticky='we')

        self.name_frame1.grid(row=6, column=0, sticky='we', pady=5)
        self.name_frame2.grid(row=7, column=0, sticky='we', pady=5)
        ttk.Button(main_frame, text="Start Game", command=self.start_game).grid(row=8, column=0, pady=20, sticky='we')
        self.update_name_fields()

    def update_name_fields(self):
        mode = self.game_mode.get()

        if mode == "0":  # Human vs Human
            self.name_frame1.grid()
            self.name_frame2.grid()
            self.player1_name.set("Player1")
            self.player2_name.set("Player2")
        elif mode == "1":  # Human vs AI
            self.name_frame1.grid()
            self.name_frame2.grid_remove()
            self.player1_name.set("Player1")
        else:  # AI vs AI
            self.name_frame1.grid_remove()
            self.name_frame2.grid_remove()

    def start_game(self):
        dim = self.dimension.get()
        mode = self.game_mode.get()

        if mode == "0":  # Human vs Human
            player1 = HumanPlayer(self.player1_name.get(), 0, 'W')
            player2 = HumanPlayer(self.player2_name.get(), 0, 'B')
        elif mode == "1":  # Human vs AI
            player1 = HumanPlayer(self.player1_name.get(), 0, 'W')
            player2 = MinMaxAI("AI", 0, 'B', dim)
        else:  # AI vs AI
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