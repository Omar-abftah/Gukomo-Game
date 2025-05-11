import tkinter as tk
from tkinter import messagebox

class GomokuGUI:
    def __init__(self, board, players):
        self.board = board
        self.players = players  # [player1, player2]
        self.current_player_index = 0
        self.game_active = True
        self.window = tk.Tk()
        self.setup_gui()
        self.start_game()

    def setup_gui(self):
        self.window.title("Gomoku Game")
        self.buttons = []
        for row in range(self.board.dimension):
            button_row = []
            for col in range(self.board.dimension):
                btn = tk.Button(
                    self.window, text=' ', width=1, height=1,
                    font=('Helvetica', 20),
                    command=lambda r=row, c=col: self.on_click(r, c)
                )
                btn.grid(row=row, column=col)
                button_row.append(btn)
            self.buttons.append(button_row)

    def start_game(self):
        if self.is_ai_turn():
            self.window.after(100, self.process_ai_turn)

    def is_ai_turn(self):
        return hasattr(self.players[self.current_player_index], 'find_the_best_move')

    def on_click(self, row, col):
        if not self.game_active or self.is_ai_turn():
            return

        current_player = self.players[self.current_player_index]
        if current_player.make_move(self.board, row, col):
            self.update_button(row, col, current_player.char)
            self.check_game_state()

    def process_ai_turn(self):
        if not self.game_active:
            return

        current_player = self.players[self.current_player_index]
        move = current_player.make_move(self.board)
        if move:
            row, col = move
            if self.board.is_valid(row, col, current_player.char):
                self.board.update(row, col, current_player.char)
                self.update_button(row, col, current_player.char)
                self.window.update()  # Force GUI update
                self.check_game_state()

    def update_button(self, row, col, char):
        symbol = '⚪' if char == 'W' else '⚫'
        self.buttons[row][col].config(
            text=symbol,
            state='disabled',
            disabledforeground='black' if char == 'B' else 'white'
        )

    def check_game_state(self):
        current_player = self.players[self.current_player_index]

        if self.board.check_win(current_player.char):
            self.end_game(f"{current_player.name} wins!")
            return

        if self.board.check_draw():
            self.end_game("It's a draw!")
            return


        self.current_player_index = 1 - self.current_player_index
        if self.is_ai_turn():
            self.window.after(500, self.process_ai_turn)
    def end_game(self, message):
        self.game_active = False
        for row in self.buttons:
            for btn in row:
                btn.config(state='disabled')
        messagebox.showinfo("Game Over", message)
        self.window.quit()

    def run(self):
        self.window.mainloop()