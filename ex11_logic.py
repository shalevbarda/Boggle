from ex11_utils import *


class BoggleModel:

    def __init__(self, board: Board, total_words_set: Set[str]):
        """

        :param board: A given legitimate board.
        :param total_words_set: A set including all valid words.
        """
        self._score: int = 0
        self._used_words: Set[str] = set()
        self._board: List[List[str]] = board
        self._total_words_set: Set[str] = total_words_set
        self._curr_path: Path = []
        self._curr_loc: Tuple = ()
        self._curr_word = ""
        self._max_score_paths = max_score_paths(board, total_words_set)
        self._max_score = calc_score(self._max_score_paths)

        return

    def update_curr_loc(self, loc: Tuple):
        """
        Updates the new curr loc according to given location
        Calls the handler for changing the curr loc.
        """
        self._curr_loc = loc
        self.handle_curr_loc()
        return

    def handle_curr_loc(self):
        """
        Checks if that curr loc is valid - can be reached from the current
        path.
        If yes, updates curr_path and the word that appears to the user.
        If its already in the path, cuts the path.
        If neither, does nothing.
        Updates the curr_word as well (for the display).
        """

        # This is the first location. Add it to the path.
        if len(self._curr_path) == 0:
            self._curr_path.append(self._curr_loc)
            self._curr_word = create_word_from_path(self._curr_path,
                                                    self._board)
            return

        # If that location is already in the path, remove everything after it.
        if self._curr_loc in self._curr_path:
            self._curr_path = self._curr_path[:self._curr_path.index(
                self._curr_loc) + 1]
            self._curr_word = create_word_from_path(self._curr_path,
                                                    self._board)
            return

        # This next location is valid. Add it to the path.
        if valid_next(self._curr_path[len(self._curr_path) - 1],
                      self._curr_loc, self._board):
            self._curr_path.append(self._curr_loc)
            self._curr_word = create_word_from_path(self._curr_path,
                                                    self._board)
            return
        return

    def calculate_score(self):
        """
        Returns the score that a certain path deserves.
        :return:
        """
        return int(math.pow(len(self._curr_path), 2))

    def handle_done(self):
        """
        Checks if the word created by the path is valid and compares to
        the dict of already used words.
        If yes: changes score, enters the word to the used ones, clears
        curr path, adds the score addition to the curr_word attribute.

        If not: clears curr path, changes curr_word to "not a valid word".
        If we want - error of used already, not a word etc.
        """
        word = is_valid_path(self._board, self._curr_path,
                             self._total_words_set)

        # Word exists and wasn't used yet:
        if word is not None and word not in self._used_words:
            score_to_add = self.calculate_score()
            self._score += score_to_add
            self._used_words.add(word)
            self._curr_path = []
            self._curr_word += " - " + str(score_to_add) + " points!"
            return word

        # Word exists but was used already:
        if word is not None:
            self._curr_path = []
            self._curr_word += str(" - this word already used")
            return False

        # Word doesn't exist:
        if word is None:
            self._curr_path = []
            self._curr_word = "not a word"
            return False

        return

    def get_score(self):
        return self._score

    def get_curr_word(self):
        return self._curr_word

    def get_board_value(self, loc: Tuple):
        """Returns the value of a cell in the board"""
        x, y = loc
        return self._board[x][y]

    def get_board(self):
        return self._board

    def get_used_words(self):
        return self._used_words

    def get_max_score(self):
        return self._max_score

    def print_board(self):
        print_board(self._board)
        return

    def get_hint(self):
        """Will return a word that is possible in the board and wasn't used
        yet"""
        for path in self._max_score_paths:
            word = create_word_from_path(path, self._board)
            if word not in self._used_words:
                return word
        return ""


def str_to_tup(string):
    mid = tuple(string)
    end = int(mid[0]), int(mid[1])
    return end


def mini_main():
    words_set = build_words_set("boggle_dict.txt")
    test_board = [['I', 'A', 'I', 'R'], ['S', 'E', 'R', 'U'],
                  ['T', 'E', 'F', 'E'], ['O', 'Y', 'A', 'C']]
    test_board2 = [['AI', 'R', 'I', 'R'], ['R', 'E', 'R', 'U'],
                  ['T', 'E', 'F', 'E'], ['O', 'Y', 'A', 'C']]
    bg = BoggleModel(test_board2, words_set)
    bg.print_board()
    user_input = input("here:")
    bg.update_curr_loc(str_to_tup(user_input))
    print(bg.get_curr_word())
    while user_input != "!":
        bg.update_curr_loc(str_to_tup(user_input))
        print(bg.get_curr_word())
        user_input = input("here:")
        if user_input == "d":
            bg.handle_done()
            print("Score is:", bg.get_score())
            print(bg.get_curr_word())
            print(bg.get_used_words())
            user_input = input("here:")
    return


if __name__ == "__main__":
    pass
