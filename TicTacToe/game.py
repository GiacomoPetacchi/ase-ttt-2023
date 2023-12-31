# Game (functionalities, to be implemented:TODO)
from itertools import cycle
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="red"),
)


class Game:
    # initialization function
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        # class fields
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        # class method
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        """Return all possible winning combinations, i.e. rows, columns and diagonals."""
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        # TODO: check that the current move has not been played already
        # and that there is no winner yet.
        # Note that non-played cells contain an empty string (i.e. "").
        # Use variables 'no_winner' and 'move_not_played'. 
        
        no_winner = not self._has_winner
        move_not_played = (self._current_moves[row][col].label == "")
        return no_winner and move_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        # TODO: check whether the current move leads to a winning combo.
        # Do not return any values but set variables 'self._has_winner' 
        # and 'self.winner_combo' in case of winning combo.
        # Hint: you can scan pre-computed winning combos in self._winning_combos
        
        # for each winning combo
        for combo in self._winning_combos:
            symbols = set()
            # for each cell in the combo, add the label to the set
            for tupla in combo:
                (r,c) = tupla
                symbols.add(self._current_moves[r][c].label)
            # if it is the current combo, with equal symbols and without ""
            if((len(symbols) == 1) and ("" not in symbols)): # because the set automatically removes duplicates, so only 1 symbol
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        # TODO: check whether a tie was reached.
        # There is no winner and all moves have been tried.

        all_moves_tried = True
        # see if all the cells are used, i.e. without ""
        for c in self._current_moves:
            for m in c:
                if(m.label == ""):
                    all_moves_tried = False

        return (not self._has_winner) and all_moves_tried
        

    def toggle_player(self):
        """Return a toggled player."""
        # TODO: switches self.current_player to the other player.
        # Hint: https://docs.python.org/3/library/functions.html#next

        #print(self.current_player)
        self.current_player = next(self._players)
        #print(self.current_player)
       
    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []