import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import random
import math


class Cell:
    def __init__(self, x, y):
        self.x, self.y, self.checked, self.flagged, self.value = x, y, False, False, ""


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.game_state = 'playing'

        board = tk.Frame(self.parent, height=300, width=300)
        board.place(x=0, y=60)

        custom_font = tkFont.Font(size=16, weight="normal", family="Arial")
        btn_style = {'borderwidth': "0", 'font': custom_font, 'bd': '2', 'fg': "black", 'anchor': "w", 'padx': 5,
                     'bg': '#dedede'}
        btn_size = {'height': 30, 'width': 30}

        reset_btn = tk.Button(self.parent, text="Reset", command=lambda: self.reset())
        reset_btn.place(height=20, width=50, x=10, y=10)

        self.game_state_string = StringVar()
        self.game_state_string.set("Playing")
        game_state_label = tk.Label(self.parent, textvariable=self.game_state_string)
        game_state_label.place(x=70, y=10)

        self.board = None
        self.bombs = None
        self.buttons = None
        self.total_flag = 0

        self.setup()

        # SETUP BUTTONS
        self.buttons = []
        for x in range(10):
            column = []
            for y in range(10):
                # SETTING UP BUTTONS
                btn = tk.Button(board, command=lambda i=x, j=y: self.check(i, j), **btn_style)
                btn.bind("<Button-2>", lambda event, i=x, j=y: self.flag(i, j))  # right click
                btn.bind("<Button-3>", lambda event, i=x, j=y: self.flag(i, j))  # right click
                btn.place(**btn_size, x=x * 30, y=y * 30)
                column.append(btn)
            self.buttons.append(column)

    def setup(self):
        # BOARD ARRAY
        self.board = []
        for x in range(10):
            column = []
            for y in range(10):
                column.append(Cell(x, y))
            self.board.append(column)

        # SETUP BOMBS
        self.bombs = random.sample(range(100), 10)
        for i in self.bombs:
            y = math.floor(i / 10)
            x = i % 10
            self.board[x][y].value = "x"

        # SETUP CELL VALUES
        for x in range(10):
            for y in range(10):
                total_bombs = 0
                if self.board[x][y].value == "x":
                    continue

                # SETTING UP NUMBERS TO CELLS
                # TOP
                # |x| | |
                # | |o| |
                # | | | |
                if x - 1 >= 0 and y - 1 >= 0 and self.board[x - 1][y - 1].value == "x":
                    total_bombs += 1

                # | |x| |
                # | |o| |
                # | | | |
                if y - 1 >= 0 and self.board[x][y - 1].value == "x":
                    total_bombs += 1

                # | | |x|
                # | |o| |
                # | | | |
                if x + 1 < 10 and y - 1 >= 0 and self.board[x + 1][y - 1].value == "x":
                    total_bombs += 1

                # SIDE
                # | | | |
                # |x|o| |
                # | | | |
                if x - 1 >= 0 and self.board[x - 1][y].value == "x":
                    total_bombs += 1
                # | | | |
                # | |o|x|
                # | | | |
                if x + 1 < 10 and self.board[x + 1][y].value == "x":
                    total_bombs += 1

                # BOTTOM
                # | | | |
                # | |o| |
                # |x| | |
                if x - 1 >= 0 and y + 1 < 10 and self.board[x - 1][y + 1].value == "x":
                    total_bombs += 1

                # | | | |
                # | |o| |
                # | |x| |
                if y + 1 < 10 and self.board[x][y + 1].value == "x":
                    total_bombs += 1

                # | | | |
                # | |o| |
                # | | |x|
                if x + 1 < 10 and y + 1 < 10 and self.board[x + 1][y + 1].value == "x":
                    total_bombs += 1

                self.board[x][y].value = str(total_bombs)

    def check(self, x, y):
        if self.game_state == 'playing' and not self.board[x][y].flagged and not self.board[x][y].checked:
            self.buttons[x][y]['background'] = '#828282'
            self.buttons[x][y]['state'] = 'disabled'
            self.buttons[x][y]['text'] = self.board[x][y].value

            if self.board[x][y].value == "0":
                self.buttons[x][y]['disabledforeground'] = '#828282'
            elif self.board[x][y].value == "1":
                self.buttons[x][y]['disabledforeground'] = '#50f27b'
            elif self.board[x][y].value == "2":
                self.buttons[x][y]['disabledforeground'] = '#00eaff'
            elif self.board[x][y].value == "x":
                self.buttons[x][y]['disabledforeground'] = '#ffa500'
            else:
                self.buttons[x][y]['disabledforeground'] = '#ffef12'

            self.board[x][y].checked = True

            if self.board[x][y].value == "x":
                self.game_state = 'lost'
                self.endgame()
                return

            if self.board[x][y].value == "0":
                # TOP
                # |x| | |
                # | |o| |
                # | | | |
                if x - 1 >= 0 and y - 1 >= 0 and not self.board[x - 1][y - 1].checked and self.board[x - 1][
                    y - 1].value != "x":
                    self.check(x - 1, y - 1)

                # | |x| |
                # | |o| |
                # | | | |
                if y - 1 >= 0 and not self.board[x][y - 1].checked and self.board[x][y - 1].value != "x":
                    self.check(x, y - 1)

                # | | |x|
                # | |o| |
                # | | | |
                if x + 1 < 10 and y - 1 >= 0 and not self.board[x + 1][y - 1].checked and self.board[x + 1][
                    y - 1].value != "x":
                    self.check(x + 1, y - 1)

                # SIDE
                # | | | |
                # |x|o| |
                # | | | |
                if x - 1 >= 0 and not self.board[x - 1][y].checked and self.board[x - 1][y].value != "x":
                    self.check(x - 1, y)

                # | | | |
                # | |o|x|
                # | | | |
                if x + 1 < 10 and not self.board[x + 1][y].checked and self.board[x + 1][y].value != "x":
                    self.check(x + 1, y)

                # BOTTOM
                # | | | |
                # | |o| |
                # |x| | |
                if x - 1 >= 0 and y + 1 < 10 and not self.board[x - 1][y + 1].checked and self.board[x - 1][
                    y + 1].value != "x":
                    self.check(x - 1, y + 1)

                # | | | |
                # | |o| |
                # | |x| |
                if y + 1 < 10 and not self.board[x][y + 1].checked and self.board[x][y + 1].value == "x":
                    self.check(x, y + 1)

                # | | | |
                # | |o| |
                # | | |x|
                if x + 1 < 10 and y + 1 < 10 and not self.board[x + 1][y + 1].checked and self.board[x + 1][
                    y + 1].value != "x":
                    self.check(x + 1, y + 1)
        pass

    def flag(self, x, y):
        if self.game_state == 'playing':
            if not self.board[x][y].checked:
                if self.board[x][y].flagged:
                    self.board[x][y].flagged = False
                    self.buttons[x][y]['background'] = '#dedede'
                    self.total_flag -= 1
                else:
                    if self.total_flag < 10: # only 10 flags are allowed
                        self.board[x][y].flagged = True
                        self.buttons[x][y]['background'] = '#ff0000'
                        self.total_flag += 1

                        for i in self.bombs:
                            y = math.floor(i / 10)
                            x = i % 10
                            if not self.board[x][y].flagged:
                                return
                        self.game_state = 'won'
                        self.endgame()
        pass

    def endgame(self):
        if self.game_state == 'lost':
            self.reveal_bombs()
            self.game_state_string.set("You Lost")
        elif self.game_state == 'won':
            self.game_state_string.set("You Won")
        pass

    def reveal_bombs(self):
        for i in self.bombs:
            y = math.floor(i / 10)
            x = i % 10
            self.buttons[x][y]['background'] = '#828282'
            self.buttons[x][y]['state'] = 'disabled'
            self.buttons[x][y]['text'] = self.board[x][y].value
            self.buttons[x][y]['disabledforeground'] = '#ffa500'
        pass

    def reset(self):
        self.board = None
        self.bombs = None
        self.total_flag = 0

        for x in range(10):
            for y in range(10):
                self.buttons[x][y]['background'] = '#dedede'
                self.buttons[x][y]['state'] = 'normal'
                self.buttons[x][y]['text'] = ''

        self.game_state = 'playing'
        self.game_state_string.set("Playing")
        self.setup()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    root.minsize("300", "360")
    root.resizable(0, 0)
    root.geometry("300x360")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
