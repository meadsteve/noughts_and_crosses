from copy import deepcopy
from dataclasses import dataclass, field
from typing import Literal, List, Union, Tuple, Optional

NOUGHTS = "o"
CROSSES = "x"
BLANK = ""
Piece = Union[Literal["o"], Literal["x"]]
Square = Union[Piece, Literal[""]]
Board = List[List[Square]]

EMPTY_BOARD: Board = [[BLANK, BLANK, BLANK], [BLANK, BLANK, BLANK], [BLANK, BLANK, BLANK]]

Move = Tuple[int, int]

QUIT = "QUIT"
Quit = Literal["QUIT"]

DRAW = "draw"
Winner = Union[Piece, Literal["draw"]]


@dataclass
class Game:
    board: List[List[Square]] = field(default_factory=lambda: EMPTY_BOARD)
    turn: Piece = NOUGHTS

    def apply_move(self, move: Move) -> "Game":
        new_game = self.copy()
        new_game.board[move[0]][move[1]] = self.turn
        new_game.turn = NOUGHTS if self.turn == CROSSES else CROSSES
        return new_game

    @property
    def running(self):
        return not self.winner

    @property
    def winner(self) -> Optional[Winner]:
        # TODO: check for a winner
        free_spaces = sum([sum([1 for element in row if element == BLANK]) for row in self.board])
        if free_spaces == 0:
            return DRAW
        return None

    def copy(self):
        return Game(board=deepcopy(self.board), turn=self.turn)


def display(game: Game):
    for line in game.board:
        print(line)


def ask_player_for_move(game: Game) -> Union[Move, Quit]:
    print(f"{game.turn}'s move")
    play_input = input("Where will you play?")
    if play_input.strip() == "":
        return QUIT
    x = (int(play_input) - 1) // 3
    y = (int(play_input) - 1) % 3
    # TODO: Check this place isn't occupied
    return x, y


def display_exit_message(game: Game):
    if game.winner == DRAW:
        print("It was a draw!")
    elif game.winner is None:
        print("The game has been quit. Good bye")
    else:
        print(f"{game.winner} won. Well done")


if __name__ == "__main__":
    print("starting")
    active_game = Game()
    while active_game.running:
        display(active_game)
        player_move = ask_player_for_move(active_game)
        if player_move == QUIT:
            break
        active_game = active_game.apply_move(player_move)
    display_exit_message(active_game)
