import time
import tkinter as tk
import ex11_utils as utils
from ex11_GUI import BoggleGUI
from ex11_logic import BoggleModel

WORD_SET = utils.build_words_set("boggle_dict.txt")
MAX_TIME = 180


class BoggleController:
    def __init__(self):
        self._gui = BoggleGUI()
        self._model = None
        self._time = MAX_TIME
        self._did_game_start = False
        self._max_score = None

        def action():
            self.new_game_started()

        self._gui.set_button_command("new_game", action)

        return

    def new_game_started(self):
        """Initiates a new model, and updates all GUI items to fit that
        model - score, current word, used words, buttons.
        Also starts running the timer"""
        board = utils.randomize_board()
        self._model = BoggleModel(board, WORD_SET)
        self._gui.set_time_label(f"Time Left: ")
        self._gui.clear_used_words()
        self._gui.set_board(self._model.get_board())
        self.set_buttons_actions()
        self._gui.set_score(f"Score: {self._model.get_score()}")
        self._time = MAX_TIME
        self._gui.set_curr_word(self._model.get_curr_word())
        self._gui.set_max_score_label(f"Max score:"
                                      f" {self._model.get_max_score()}")
        if not self._did_game_start:
            self.timer()
            self._did_game_start = True

# ----------------------- SETTING BUTTONS ACTIONS -------------------------- #

    def set_buttons_actions(self):
        """Sets all buttons actions"""
        self.set_game_buttons_actions()
        self.set_submit_action()
        self.hint_button()

    def set_submit_action(self):
        """Sets the submit button's action"""
        def action():
            word = self._model.handle_done()
            if word:
                self._gui.add_used_words(word)
            self._gui.set_curr_word(self._model.get_curr_word())
            self._gui.set_score(f"Score: {self._model.get_score()}")
            if self._model.get_max_score() == self._model.get_score():
                self.make_buttons_useless()
                self._gui.set_curr_word("You won!")

        self._gui.set_button_command("submit", action)
        return

    def set_game_buttons_actions(self):
        """Sets the board's buttons' actions"""
        for row_index in range(len(self._model.get_board())):
            for col_index in range(len(self._model.get_board())):
                loc = row_index, col_index
                action = self.create_game_button_action(loc)
                self._gui.set_button_command(loc, action)
        return

    def create_game_button_action(self, loc):
        """Returns a function that fits a button on the board"""
        def action():
            self._model.update_curr_loc(loc)
            self._gui.set_curr_word(self._model.get_curr_word())
        return action

    def make_buttons_useless(self):
        """A function that makes the board's buttons do nothing. Will be
        called after timer ended."""
        for row_index in range(len(self._model.get_board())):
            for col_index in range(len(self._model.get_board())):
                loc = row_index, col_index

                def action():
                    return None
                self._gui.set_button_command(loc, action)
        return

    def hint_button(self):
        """Sets the action of the hint button to show a hint word as the
        current word"""
        def action():
            word = self._model.get_hint()
            self._gui.set_curr_word(word)

        self._gui.set_button_command("hint", action)
        return

# ---------------------------- HANDLE TIME --------------------------------- #

    def timer(self):
        """Changes the time attribute of the game every second and changes
        the time label to show to remaining time.
        After time is up, makes the buttons of the game non-functional,
        so the user can't keep playing."""
        def calc_time_value():
            minutes = self._time // 60
            seconds = self._time % 60
            if seconds < 10:
                seconds = "0" + str(seconds)
            return str(minutes), seconds

        if self._time > 0:
            self._time -= 1
            min, sec = calc_time_value()
            self._gui.set_time_label(f"Time Left: {min}:{sec} | ")
            self._gui.get_root().after(1000, self.timer)
        else:
            self._did_game_start = False
            self.make_buttons_useless()

    def run(self):
        self._gui.run()


if __name__ == '__main__':
    BoggleController().run()



