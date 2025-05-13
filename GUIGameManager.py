import tkinter as tk
from tkinter import messagebox
from GameManager import GameManager
from HumanPlayer import HumanPlayer
from MinMaxAI import MinMaxAI
from AlphaBetaPruningAI import AlphaBetaPruningAI

class GUIGameManager(GameManager):
    def __init__(self, board, player1, player2):
        super().__init__(board, player1, player2)
        self.root = tk.Tk()
        self.root.title("Gomoku Game")
        self.current_player_index = 0
        self.buttons = []
        self.game_active = True
        self.ai_move_delay = 800
        self.setup_ui()
        if isinstance(self.players[0], (MinMaxAI, AlphaBetaPruningAI)):
            self.root.after(self.ai_move_delay, self.process_ai_move)

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack()
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        self.player_turn_label = tk.Label(
            control_frame,
            text=f"{self.players[self.current_player_index].name}'s turn ({self.players[self.current_player_index].char})",
            font=('Arial', 12)
        )
        self.player_turn_label.pack(side=tk.LEFT)
        self.score_label = tk.Label(
            control_frame,
            text=f"Scores: {self.players[0].name}: {self.players[0].score} | {self.players[1].name}: {self.players[1].score}",
            font=('Arial', 12)
        )
        self.score_label.pack(side=tk.LEFT, padx=20)
        self.restart_btn = tk.Button(
            control_frame,
            text="Restart Game",
            command=self.restart_game,
            font=('Arial', 12)
        )
        self.restart_btn.pack(side=tk.RIGHT)
        self.create_board_buttons()

    def create_board_buttons(self):
        for i in range(self.board.dimension):
            row = []
            for j in range(self.board.dimension):
                btn = tk.Button(
                    self.main_frame,
                    text="",
                    width=3,
                    height=1,
                    font=('Arial', 14),
                    command=lambda x=i, y=j: self.handle_human_move(x, y)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)

    def handle_human_move(self, x, y):
        if not self.game_active:
            return
        current_player = self.players[self.current_player_index]
        if isinstance(current_player, HumanPlayer):
            if self.board.is_valid(x, y, current_player.char):
                self.make_move(x, y, current_player)
                if self.game_active and isinstance(self.players[self.current_player_index], (MinMaxAI, AlphaBetaPruningAI)):
                    self.root.after(self.ai_move_delay, self.process_ai_move)

    def process_ai_move(self):
        if not self.game_active:
            return
        current_player = self.players[self.current_player_index]
        if isinstance(current_player, (MinMaxAI, AlphaBetaPruningAI)):
            move = current_player.make_move(self.board)
            if move:
                x, y = move
                self.make_move(x, y, current_player)
                if self.game_active and isinstance(self.players[self.current_player_index], (MinMaxAI, AlphaBetaPruningAI)):
                    self.root.after(self.ai_move_delay, self.process_ai_move)

    def make_move(self, x, y, player):
        self.board.update(x, y, player.char)
        self.update_button(x, y, player.char)
        self.check_game_state()

    def update_button(self, x, y, char):
        self.buttons[x][y].config(text=char, state=tk.DISABLED)
        color = 'white' if char == 'W' else 'black'
        self.buttons[x][y].config(bg=color, fg='white' if color == 'black' else 'black')

    def check_game_state(self):
        current_player = self.players[self.current_player_index]
        if self.board.check_win(current_player.char):
            self.end_game(current_player)
            return
        if self.board.check_draw():
            self.end_game(None)
            return
        self.current_player_index = (self.current_player_index + 1) % 2
        self.update_turn_label()

    def end_game(self, winner):
        self.game_active = False
        for row in self.buttons:
            for btn in row:
                btn.config(state=tk.DISABLED)
        if winner:
            winner.increment_score()
            messagebox.showinfo("Game Over", f"{winner.name} wins!")
        else:
            messagebox.showinfo("Game Over", "It's a draw!")
        self.update_turn_label()

    def update_turn_label(self):
        if not self.game_active:
            status = "Game Over"
        else:
            current_player = self.players[self.current_player_index]
            status = f"{current_player.name}'s turn ({current_player.char})"
        self.player_turn_label.config(text=status)
        self.score_label.config(
            text=f"Scores: {self.players[0].name}: {self.players[0].score} | {self.players[1].name}: {self.players[1].score}"
        )

    def restart_game(self):
        self.board.reset()
        self.game_active = True
        self.current_player_index = 0
        self.update_turn_label()
        for i in range(self.board.dimension):
            for j in range(self.board.dimension):
                self.buttons[i][j].config(
                    text="",
                    state=tk.NORMAL,
                    bg='light gray',
                    fg='black'
                )
        if isinstance(self.players[0], (MinMaxAI, AlphaBetaPruningAI)):
            self.root.after(self.ai_move_delay, self.process_ai_move)

    def play(self):
        self.root.mainloop()