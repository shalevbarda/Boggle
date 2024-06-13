from typing import List, Tuple, Iterable, Optional, Set
from boggle_board_randomizer import *
from functools import wraps, cache
import time
import math
import tkinter as tki


Board = List[List[str]]
Path = List[Tuple[int, int]]


def time_counter_decorator(func):
    """A decorator that prints the runtime of the function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func_result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Runtime of '{func.__name__}' is:", end_time - start_time,
              "seconds.")
        return func_result
    return wrapper


def clean_word(word: str):
    """
    Receives a word, removes all non-relevant chars from it (end of line,
    beginning of line).
    :param word:
    :return:
    """
    new_word: List[str] = []
    for char in word:
        if char.isupper():
            new_word.append(char)
    return "".join(new_word)


@cache
def build_words_set(file_name: str):
    """
    Receives file name, returns a words set with all words in that file.
    :param file_name:
    :return:
    """
    words_set = set()
    with open(file_name, 'rb') as boggle_dict:
        for line in boggle_dict:
            word = str(line)
            words_set.add(clean_word(word))
    return words_set


def valid_next(curr_loc: tuple, next_loc: tuple, board: Board) -> bool:
    """
    Returns True if the next tuple is reachable from the current tuple.
    :param next_loc:
    :param curr_loc:
    :param board:
    :return:
    """
    curr_x, curr_y = curr_loc
    next_x, next_y = next_loc
    # Checking if the next tuple is out of the board.
    if not is_loc_in_board(next_loc, board):
        return False
    # Checking if there is a jump in the rows or cols of 2.
    if abs(curr_x - next_x) > 1 or abs(curr_y - next_y) > 1:
        return False
    return True


def is_loc_in_board(loc: tuple, board: Board) -> bool:
    """
    Returns True if the tuple is in the board.
    :param loc:
    :param board:
    :return:
    """
    rows = len(board)
    cols = len(board[0])
    x, y = loc
    if x >= rows or y >= cols or x < 0 or y < 0:
        return False
    return True


def create_word_from_path(path: Path, board: Board) -> str:
    """
    Receives a VALID path only.
    :param path:
    :param board:
    :return:
    """
    result = ""
    for cord in path:
        result += board[cord[0]][cord[1]]
    return result


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """
    If the word created in the path is valid, returns it. Otherwise, returns None.
    :param board:
    :param path:
    :param words:
    :return:
    """
    # If the path is empty, return None.
    if len(path) == 0:
        return None
    # Checking if there is a coordinate that repeats itself:
    path_set = set(path)
    if len(path_set) != len(path):
        return None
    # Checking if the first coordinate is in the board:
    if not is_loc_in_board(path[0], board):
        return None
    # Going through all coordinates, validating and building word:
    path_word: List[str] = [board[path[0][0]][path[0][1]]]
    for i in range(len(path) - 1):
        curr_loc = path[i]
        next_loc = path[i + 1]
        # Validating that the next coordinate is reachable from current:
        if not valid_next(curr_loc, next_loc, board):
            return None
    # Checking if created word is within the word bank:
    final_word = create_word_from_path(path, board)
    if final_word not in words:
        return None
    # All validations are good, returning the word created.
    return final_word


def _help_find_length_n_path(n: int, curr_path: Path, board: Board, words: \
    Iterable[str], results: List[Path], work_set):
    """
    Helper to the find_length_n_path function. The idea is to start from the
    beginning point given by mother function and backtrack all possible
    advances in the board from there.
    :param n:
    :param curr_path: Receives the beginning point of the path.
    :param board:
    :param words:
    :param results:
    :return:
    """
    if n == 0:
        result_word = is_valid_path(board, curr_path, words)
        if result_word is not None:  # The path creates a valid word.
            results.append(curr_path[:])
        return

    args = [board, words, results, work_set]  # Not repeating args

    for row_index in range(-1, 2, 1):
        for col_index in range(-1, 2, 1):
            curr_x, curr_y = curr_path[len(curr_path) - 1]
            next_loc = row_index + curr_x, col_index + curr_y

            # The next location was already visited:
            if next_loc in curr_path:
                continue

            # The next location is in the board, so add it to the path:
            if is_loc_in_board(next_loc, board):
                curr_path.append(next_loc)
                # If the path creates not valid sequence of letters, stop.
                if create_word_from_path(curr_path, board) in work_set:
                    _help_find_length_n_path(n - 1, curr_path, *args)
                curr_path.pop(len(curr_path) - 1)


# @time_counter_decorator
def find_length_n_paths(n: int, board: Board, words: Iterable[str])\
        -> List[Path]:
    """
    Returns ALL the possible n-steps paths that create a valid word in a
    given board.
    It will return different paths for the same word if they exist.
    :param n:
    :param board:
    :param words:
    :return:
    """
    results: List[Path] = []
    # The idea of the loop is to start using the helper function from EVERY
    # possible coordinate in the board.

    # Creating a set of all possible words in the board and their sub-sequences
    work_set = clear_word_set(board, words)
    for word in work_set:
        work_set = work_set | word_to_set(word)

    for row_index in range(len(board)):
        for col_index in range(len(board[0])):
            starting_location = row_index, col_index
            path: Path = [starting_location]
            _help_find_length_n_path(n - 1, path, board, words, results,
                                     work_set)
    return results


def _help_find_length_n_word(n: int, word_length: int,
                             curr_path: Path, board: Board,
                             words: Iterable[str], results: List[Path],
                             work_set):
    """
    Helper to the find_length_n_path function. The idea is to start from the
    beginning point given by mother function and backtrack all possible
    advances in the board from there.
    :param n:
    :param curr_path: Receives the beginning point of the path.
    :param board:
    :param words:
    :param results:
    :return:
    """
    # Stop because we reached the length of the word (path wise).
    if n == 0:
        result_word = is_valid_path(board, curr_path, words)
        if result_word is not None:  # The path creates a valid word.
            results.append(curr_path[:])
        return

    # Stop if the word already has enough or too many letters.
    result_word = is_valid_path(board, curr_path, words)
    if result_word is not None:
        if len(result_word) == word_length:
            results.append(curr_path[:])
            return
        if len(result_word) > word_length:
            return

    args = [board, words, results, work_set]  # Not repeating args

    for row_index in range(-1, 2, 1):
        for col_index in range(-1, 2, 1):
            curr_x, curr_y = curr_path[len(curr_path) - 1]
            next_loc = row_index + curr_x, col_index + curr_y

            # The next location was already visited:
            if next_loc in curr_path:
                continue

            # The next location is in the board, so add it to the path:
            if is_loc_in_board(next_loc, board):
                curr_path.append(next_loc)
                # If the path creates not valid sequence of letters, stop.
                if create_word_from_path(curr_path, board) in work_set:
                    _help_find_length_n_word(n - 1, word_length, curr_path, *args)
                curr_path.pop(len(curr_path) - 1)


# @time_counter_decorator
def find_length_n_words(n: int, board: Board, words: Iterable[str])\
        -> List[Path]:
    """
    Returns ALL the possible n-steps paths that create a valid word in a
    given board.
    It will return different paths for the same word if they exist.
    :param n:
    :param board:
    :param words:
    :return:
    """
    if n == 0:
        return []

    # Creating a set of all possible words in the board and their sub-sequences
    work_set = clear_word_set(board, words)
    for word in work_set:
        work_set = work_set | word_to_set(word)

    results: List[Path] = []
    # The idea of the loop is to start using the helper function from EVERY
    # possible coordinate in the board.
    for row_index in range(len(board)):
        for col_index in range(len(board[0])):
            starting_location = row_index, col_index
            path: Path = [starting_location]
            _help_find_length_n_word(n - 1, n, path, board, words, results,
                                     work_set)
    return results


def word_to_set(word: str) -> Set:
    """
    Adds all sub words (with order) to the set and returns it.
    :param word:
    :return:
    """
    res_set = set()
    for i in range(1, len(word)):
        res_set.add(word[:i])
    return res_set


def create_string_from_board(board: Board):
    """Returns a string including all letters in the board"""
    res = ""
    for row in board:
        for item in row:
            res += item
    return res


def clear_word_set(board: Board, words: Iterable):
    """
    Returns a set containing all the words of which all letters exist in the
    board.
    :param board:
    :param words:
    :return:
    """
    result_set = set()
    board_str = create_string_from_board(board)
    for word in words:
        valid_flag = True
        for letter in word:
            if letter not in board_str:
                valid_flag = False
        if valid_flag:
            result_set.add(word)
    return result_set


def _help_max_score(board: Board, word: str, curr_path: Path, results: List):
    """
    Appends all paths possible on a board for a specific word.
    :param board:
    :param word:
    :param curr_path:
    :param results:
    :return:
    """
    # Stop because we reached the length of the word (path wise).
    if create_word_from_path(curr_path, board) == word:
        results.append(curr_path[:])
        return

    if len(curr_path) > len(word):
        return

    # Stop if the word already has enough or too many letters.

    for row_index in range(-1, 2, 1):
        for col_index in range(-1, 2, 1):
            curr_x, curr_y = curr_path[len(curr_path) - 1]
            next_loc = row_index + curr_x, col_index + curr_y

            # The next location was already visited:
            if next_loc in curr_path:
                continue

            if is_loc_in_board(next_loc, board):
                curr_path.append(next_loc)
                path_word = create_word_from_path(curr_path, board)
                if path_word == word[:len(path_word)]:
                    _help_max_score(board, word, curr_path, results)
                curr_path.pop(len(curr_path) - 1)


# @time_counter_decorator
def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    For a board, returns a list containing the longest paths for each word
    that is possible to create within the board.
    :param board:
    :param words:
    :return:
    """
    result_paths: List[Path] = []
    cleared_word_set = clear_word_set(board, words)
    for word in cleared_word_set:
        word_paths = []
        # Trying to start from every point in the board:
        for row_index in range(len(board)):
            for col_index in range(len(board[0])):
                board_value = board[row_index][col_index]
                # Checking if this point in the board is relevant as beginning:
                if len(board_value) > len(word):
                    continue
                if board_value != word[:len(board_value)]:
                    continue

                # This point in the board is relevant. Start backtracking:
                starting_location = row_index, col_index
                path: Path = [starting_location]
                _help_max_score(board, word, path, word_paths)
        # If there is no path to create the word in this board, continue.
        if len(word_paths) == 0:
            continue

        # There is a path, adding the longest path to the results.
        longest_path = return_longest_path(word_paths)
        result_paths.append(longest_path)
    return result_paths


def return_longest_path(path_list: List[Path]):
    """
    From a list of paths, returns the longest one.
    :param path_list:
    :return:
    """
    max_length = 0
    curr_longest = []
    for path in path_list:
        if len(path) > max_length:
            curr_longest = path
    return curr_longest


def print_board(board: Board):
    """Prints a board"""
    for i in range(len(board)):
        print(board[i])
    return None


def calc_score(words_paths: List[Path]) -> int:
    """
    Calculates the score for a given paths list.
    :param words_paths:
    :return:
    """
    score = 0
    for path in words_paths:
        score += len(path) ** 2
    return score


if __name__ == "__main__":
    # words_set = build_words_set("boggle_dict.txt")

    # # board = randomize_board()
    # board1 = [['E', 'D', 'P', 'Y'], ['F', 'L', 'A', 'M'],
    #          ['S', 'I', 'A', 'U'], ['T', 'I', 'R', 'O']]
    # board2 = [['I', 'A', 'I', 'R'], ['S', 'E', 'R', 'U'],
    #           ['T', 'E', 'F', 'E'], ['O', 'Y', 'A', 'C']]
    # print_board(board2)
    # print(create_word_from_path([(0, 1), (0, 2), (0,3)], board1))
    # result1 = find_length_n_paths(9, board1, words_set)
    # result2 = find_length_n_words(4, board2, words_set)
    # print(result2)
    # max = max_score_paths(board1, words_set)
    # print(max)
    # print(len(max))
    # print(calc_score(max))
    # print(word_to_set("hello"))
    # print(len(result2))
    pass

