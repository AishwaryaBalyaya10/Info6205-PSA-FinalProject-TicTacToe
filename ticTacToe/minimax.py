import numpy as np
from typing import Dict, Tuple

from utils.plot import plot
from utils.ternary import Ternary
from utils.combinations import determineWinner


def score(board: Ternary, depth: int, player: int = 2) -> Tuple[int, bool]:
    winner = determineWinner(board)

    if winner == player:
        return 10 - depth, True
    elif winner < 1:
        return 0, winner == 0
    else:
        return depth - 10, True


def minimax(board: Ternary, depth: int = 0, player: int = 2) -> Tuple[Ternary, int]:
    score, ended = determineWinner(board, depth, player)

    if score != 0 or ended:
        return board, score

    depth += 1
    actionsScored: Dict = {}
    actions = np.where(np.array(list(board.number)) == "0")[0]
    playerActive = len(actions) % 2 + 1

    for a in actions:
        action_board = list(board.number)
        action_board[a] = str(playerActive)
        newBoard = "".join(action_board)
        _, actionsScored[newBoard] = minimax(Ternary(newBoard), depth, player)

    if player == playerActive:
        maxValue = max(actionsScored.values())
        maxBoards = [b for b, v in actionsScored.items() if v == maxValue]
        return Ternary(np.random.choice(maxBoards)), maxValue
    else:
        minValue = min(actionsScored.values())
        minBoards = [b for b, v in actionsScored.items() if v == minValue]
        return Ternary(np.random.choice(minBoards)), minValue


if __name__ == "__main__":
    play_again = True
    while play_again:
        _board = Ternary("0" * 9)
        _winner = -1
        _turn = 1

        while _winner < 0:
            _player = _turn % 2 + 1
            if _player == 2:
                _board, _ = minimax(_board)
            else:
                print(plot(_board))
                _action = int(input("Human turn (0-8): "))
                while _action not in np.where(np.array(list(_board.number)) == "0")[0]:
                    _action = int(input(f"Action {_action} is already used, try new (0-9): "))

                _action_board = list(_board.number)
                _action_board[_action] = str(_player)

                _board = Ternary("".join(_action_board))

            _winner = determineWinner(_board)
            _turn += 1

        print(f"\nWinner: {_winner}\n")
        print(plot(_board))

        play_again = input("Play again [y/n]: ") == "y"
