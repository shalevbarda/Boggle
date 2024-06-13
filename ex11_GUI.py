import tkinter as tk
import ex11_logic as logic
import ex11_utils as utils


REGULAR_COLOR = '#A07A56'
# REGULAR_COLOR = '#C39C75'
ACTIVE_COLOR = '#BF8650'
BUTTON_STYLE = {'font': ('courier', 30), "borderwidth": 2, 'bg': REGULAR_COLOR,
                'activebackground': ACTIVE_COLOR}
FRAME_COLOR = '#7D5A3C'
# FRAME_COLOR = '#A07A56'
TEXT_COLOR = 'black'


class BoggleGUI:
    def __init__(self):
        self._listbox_used_words = None
        self._label_cur_word = None
        self._label_score = None
        self._label_time = None
        self._label_max_score = None
        self._board: logic.Board = [[" " for _ in range(4)] for _ in range(4)]

        # creates tkinter window
        self._root = tk.Tk()


        # Properties of the window
        self.root_settings()

        # buttons
        self._buttons = dict()

        # outer frame
        self._outer_frame = tk.Frame()
        self.create_outer_frame()
        self._outer_frame.pack()

        # upper frame
        self._upper_frame = tk.Frame()
        self.create_upper_frame()
        self._upper_frame.pack()

        # mid frame
        self._mid_frame = tk.Frame(self._outer_frame, bg= FRAME_COLOR)
        self.create_mid_frame()
        self._mid_frame.pack()

        # lower frame
        self._lower_frame = tk.Frame()
        self._lower_inner_frame = tk.Frame()
        self.create_lower_frame()
        self._lower_frame.pack()

    def root_settings(self):
        """Updates the settings of the root"""
        # name of the window
        self._root.title("Boggle by Yuval and Shalev")

        def on_closing():
            print("Game was closed")
            self._root.destroy()

        self._root.protocol("WM_DELETE_WINDOW", on_closing)

# -------------------------- CREATING THE FRAMES --------------------------- #

    def create_outer_frame(self):
        self._outer_frame = tk.Frame(self._root, bg=FRAME_COLOR,
                                     highlightbackground="black",
                                     highlightthickness=3)
        self._outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_upper_frame(self):
        self._upper_frame = tk.Frame(self._outer_frame, bg=FRAME_COLOR)
        self._upper_frame.pack()

        self._label_time = tk.Label(self._upper_frame, text="Time Left: ",
                                    font=('Comic Sans MS', 12), bg=FRAME_COLOR,fg=TEXT_COLOR)
        self._label_time.pack(side=tk.LEFT)

        self._label_max_score = tk.Label(self._upper_frame, text="Max score:",
                                         font=('Comic Sans MS', 12), bg=FRAME_COLOR,fg=TEXT_COLOR)
        self._label_max_score.pack(side=tk.RIGHT)

        self._label_score = tk.Label(self._upper_frame, text="Score: 0",
                                     font=('Comic Sans MS', 12), bg=FRAME_COLOR,fg=TEXT_COLOR)
        self._label_score.pack(side=tk.RIGHT)


    def create_lower_frame(self):
        # BUTTON_PHOTO = tk.PhotoImage(file="button.png")
        self._lower_inner_frame["bg"] = FRAME_COLOR
        self._lower_inner_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        self._lower_frame["bg"] = FRAME_COLOR
        self._lower_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        submit_bth = tk.Button(self._lower_frame, text="submit",
                               font=('courier', 14), bg=REGULAR_COLOR, borderwidth=5)
        submit_bth.pack(side=tk.BOTTOM)
        new_game_bth = tk.Button(self._lower_inner_frame, text="New game",
                                 font=('courier', 13), bg=REGULAR_COLOR, borderwidth= 5)
        new_game_bth.pack(side=tk.LEFT)
        hint_bth = tk.Button(self._lower_inner_frame, text="  hint  ",
                             font=('courier', 13), bg=REGULAR_COLOR, borderwidth= 5)
        hint_bth.pack(side=tk.RIGHT)
        self._buttons["submit"] = submit_bth
        self._buttons["new_game"] = new_game_bth
        self._buttons["hint"] = hint_bth

        self._label_cur_word = tk.Label(self._lower_frame, text="שלום",
                                        font=('courier', 15), bg=FRAME_COLOR,fg=TEXT_COLOR)
        self._label_cur_word.pack(side="bottom")

    def create_mid_frame(self):
        # The right side - the board of the game
        _mid_right = tk.Frame(self._mid_frame, bg= FRAME_COLOR)
        label = tk.Label(_mid_right, text="Boggle Board" ,bg= FRAME_COLOR,fg=TEXT_COLOR)
        label.pack()
        _mid_right_lower = tk.Frame(_mid_right ,bg= FRAME_COLOR)
        self.create_board_grid(_mid_right_lower)
        _mid_right_lower.pack()
        _mid_right.pack(side="right")

        # The left side - the used words display.
        _mid_left = tk.Frame(self._mid_frame ,bg= FRAME_COLOR)
        self.create_mid_left(_mid_left)
        _mid_left.pack(side="left")
        return

    def create_mid_left(self, _mid_left):
        label = tk.Label(_mid_left, text="Used words:", bg=FRAME_COLOR,fg=TEXT_COLOR, font=('Comic Sans MS', 12))
        label.pack(side=tk.TOP)
        self._listbox_used_words = tk.Listbox(_mid_left, activestyle="none", bg=FRAME_COLOR)
        self._listbox_used_words.pack(side=tk.RIGHT)
        scrollbar = tk.Scrollbar(_mid_left)
        self._listbox_used_words.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self._listbox_used_words.yview)
        scrollbar.pack(side=tk.LEFT)

        return

# -------------------------- SETTERS AND GETTERS --------------------------- #

    def set_curr_word(self, text):
        """Updates the current word"""
        self._label_cur_word["text"] = text
        self._label_cur_word["bg"] = FRAME_COLOR
        return

    def set_score(self, text):
        """Updates the score"""
        self._label_score["text"] = text
        return

    def set_board(self, board):
        """Receives a board (from controller), updates the board attribute
        and updates all the game buttons to the new board."""
        self._board = board
        self.update_game_buttons()
        return None

    def set_time_label(self, text):
        self._label_time.config(text=text, fg=TEXT_COLOR)
        return

    def set_max_score_label(self, text):
        self._label_max_score.config(text=text,fg=TEXT_COLOR)
        return

    def get_buttons(self):
        return self._buttons

    def get_root(self):
        return self._root

    def get_time_label(self):
        return self._label_time["text"]

# -------------------------- HANDLE USED WORDS ----------------------------- #

    def add_used_words(self, word):
        """Updates the used word list."""
        self._listbox_used_words.insert(tk.END, word)
        return

    def clear_used_words(self):
        """Clears all elements in the used words listbox"""
        length = self._listbox_used_words.size()
        for i in range(length):
            self._listbox_used_words.delete(0)

# -------------------------- HANDLE BOARD BUTTONS -------------------------- #

    def set_button_command(self, button_name, action):
        """Sets an action for a button"""
        self._buttons[button_name]["command"] = action
        return

    def create_button(self, frame, row, col, text: str, rowspan=1,
                      colspan=1) -> tk.Button:
        button = tk.Button(frame, text=text, **BUTTON_STYLE)
        # Sticky keyword?
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

        def _on_enter(event):
            button['background'] = 'gray'

        def _on_leave(event):
            button['background'] = REGULAR_COLOR

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)  # Not working.

        # The buttons dict will sort tuples (locations) to buttons.
        self._buttons[(row, col)] = button
        return button

    def update_game_buttons(self):
        """Updates all buttons to the board's values."""
        for row in range(4):
            for col in range(4):
                loc = row, col
                self._buttons[loc]['text'] = self._board[row][col]
        return None

    def create_board_grid(self, frame):
        """Creates the button grid (in the beginning)"""
        for row_index in range(4):
            for col_index in range(4):
                board_val = self._board[row_index][col_index]
                self.create_button(frame, row_index, col_index, board_val)
        return

# ---------------------------------- RUN ---------------------------------- #

    def run(self):
        self._root.mainloop()


if __name__ == '__main__':
    pass
