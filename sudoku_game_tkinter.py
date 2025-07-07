import tkinter as tk
from tkinter import messagebox

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game - Tkinter GUI")
        self.puzzles = [
            [
                [0, 0, 0, 2, 6, 0, 7, 0, 1],
                [6, 8, 0, 0, 7, 0, 0, 9, 0],
                [1, 9, 0, 0, 0, 4, 5, 0, 0],
                [8, 2, 0, 1, 0, 0, 0, 4, 0],
                [0, 0, 4, 6, 0, 2, 9, 0, 0],
                [0, 5, 0, 0, 0, 3, 0, 2, 8],
                [0, 0, 9, 3, 0, 0, 0, 7, 4],
                [0, 4, 0, 0, 5, 0, 0, 3, 6],
                [7, 0, 3, 0, 1, 8, 0, 0, 0]
            ],
            [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ],
            [
                [0, 2, 0, 6, 0, 8, 0, 0, 0],
                [5, 8, 0, 0, 0, 9, 7, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [3, 7, 0, 0, 0, 0, 5, 0, 0],
                [6, 0, 0, 0, 0, 0, 0, 0, 4],
                [0, 0, 8, 0, 0, 0, 0, 1, 3],
                [0, 0, 0, 0, 2, 0, 0, 0, 0],
                [0, 0, 9, 8, 0, 0, 0, 3, 6],
                [0, 0, 0, 3, 0, 6, 0, 9, 0]
            ]
        ]
        self.board = []
        self.cells = {}
        self.selected_cell = None
        self.timer_seconds = 0
        self.timer_running = False
        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        for row in range(9):
            for col in range(9):
                e = tk.Entry(self.frame, width=2, font=('Arial', 24), justify='center', borderwidth=2, relief='ridge')
                e.grid(row=row, column=col, padx=1, pady=1)
                e.bind('<FocusIn>', lambda event, r=row, c=col: self.cell_selected(r, c))
                e.bind('<KeyRelease>', lambda event, r=row, c=col: self.on_key_release(event, r, c))
                self.cells[(row, col)] = e

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Solve", command=self.solve).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset_board).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_board).pack(side='left', padx=5)
        tk.Button(btn_frame, text="New Game", command=self.new_game).pack(side='left', padx=5)

        timer_frame = tk.Frame(self.root)
        timer_frame.pack(pady=10)

        self.timer_label = tk.Label(timer_frame, text="Timer: 00:00", font=('Arial', 14))
        self.timer_label.pack(side='left', padx=10)

        tk.Button(timer_frame, text="2 min", command=lambda: self.set_timer(2*60)).pack(side='left', padx=5)
        tk.Button(timer_frame, text="5 min", command=lambda: self.set_timer(5*60)).pack(side='left', padx=5)
        tk.Button(timer_frame, text="10 min", command=lambda: self.set_timer(10*60)).pack(side='left', padx=5)

    def draw_board(self):
        for row in range(9):
            for col in range(9):
                val = self.board[row][col]
                e = self.cells[(row, col)]
                if val != 0:
                    e.delete(0, tk.END)
                    e.insert(0, str(val))
                    e.config(state='disabled', disabledforeground='black')
                else:
                    e.delete(0, tk.END)
                    e.config(state='normal')

    def cell_selected(self, row, col):
        self.selected_cell = (row, col)

    def on_key_release(self, event, row, col):
        val = event.widget.get()
        if val == '':
            self.board[row][col] = 0
            return
        if val.isdigit() and 1 <= int(val) <= 9:
            if self.is_valid_move(row, col, int(val)):
                self.board[row][col] = int(val)
            else:
                messagebox.showwarning("Invalid Move", f"Number {val} cannot be placed at ({row+1}, {col+1})")
                event.widget.delete(0, tk.END)
        else:
            event.widget.delete(0, tk.END)

    def is_valid_move(self, row, col, num):
        # Check row
        for c in range(9):
            if c != col and self.board[row][c] == num:
                return False
        # Check column
        for r in range(9):
            if r != row and self.board[r][col] == num:
                return False
        # Check 3x3 box
        box_row = row // 3 * 3
        box_col = col // 3 * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r != row or c != col) and self.board[r][c] == num:
                    return False
        return True

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return (r, c)
        return None

    def solve(self):
        empty = self.find_empty()
        if not empty:
            messagebox.showinfo("Sudoku", "Puzzle solved!")
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                self.cells[(row, col)].delete(0, tk.END)
                self.cells[(row, col)].insert(0, str(num))
                self.cells[(row, col)].config(disabledforeground='blue')
                self.root.update()
                if self.solve():
                    return True
                self.board[row][col] = 0
                self.cells[(row, col)].delete(0, tk.END)
                self.cells[(row, col)].config(state='normal')
        return False

    def reset_board(self):
        self.board = [
            [0, 0, 0, 2, 6, 0, 7, 0, 1],
            [6, 8, 0, 0, 7, 0, 0, 9, 0],
            [1, 9, 0, 0, 0, 4, 5, 0, 0],
            [8, 2, 0, 1, 0, 0, 0, 4, 0],
            [0, 0, 4, 6, 0, 2, 9, 0, 0],
            [0, 5, 0, 0, 0, 3, 0, 2, 8],
            [0, 0, 9, 3, 0, 0, 0, 7, 4],
            [0, 4, 0, 0, 5, 0, 0, 3, 6],
            [7, 0, 3, 0, 1, 8, 0, 0, 0]
        ]
        self.draw_board()

    def clear_board(self):
        self.board = [[0]*9 for _ in range(9)]
        self.draw_board()
        self.stop_timer()

    def new_game(self):
        import random
        self.board = random.choice(self.puzzles)
        # Deep copy to avoid modifying original puzzles
        self.board = [row[:] for row in self.board]
        self.draw_board()
        self.set_timer(2*60)  # default timer 2 minutes
        self.start_timer()

    def set_timer(self, seconds):
        self.timer_seconds = seconds
        self.update_timer_label()

    def update_timer_label(self):
        mins = self.timer_seconds // 60
        secs = self.timer_seconds % 60
        self.timer_label.config(text=f"Timer: {mins:02d}:{secs:02d}")

    def timer_tick(self):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.update_timer_label()
            self.timer_running = True
            self.root.after(1000, self.timer_tick)
        else:
            self.timer_running = False
            messagebox.showinfo("Time's up!", "Time is over! Please start a new game or reset.")
            # Optionally disable inputs here

    def start_timer(self):
        if not self.timer_running:
            self.timer_tick()

    def stop_timer(self):
        self.timer_running = False

def main():
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
