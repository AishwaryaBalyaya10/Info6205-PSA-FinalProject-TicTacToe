import numpy as np
import logging
from typing import Dict, Tuple

from ticTacToe.utils.plot import plot
from ticTacToe.utils.ternary import Ternary
from ticTacToe.utils.combinations import determineWinner


def getScore(board: Ternary, depth: int, player: int = 2) -> Tuple[int, bool]:
    winner = determineWinner(board)

    if winner == player:
        return 10 - depth, True
    elif winner < 1:
        return 0, winner == 0
    else:
        return depth - 10, True


def minimax(board: Ternary, depth: int = 0, player: int = 2) -> Tuple[Ternary, int]:
    score, ended = getScore(board, depth, player)
    if score != 0 or ended:
        return board, score

    depth += 1
    scoredActions: Dict = {}
    actions = np.where(np.array(list(board.number)) == "0")[0]
    activePlayer = len(actions) % 2 + 1

    for a in actions:
        actionBoard = list(board.number)
        actionBoard[a] = str(activePlayer)
        new_board = "".join(actionBoard)
        _, scoredActions[new_board] = minimax(Ternary(new_board), depth, player)

    if player == activePlayer:
        max_value = max(scoredActions.values())
        max_boards = [b for b, v in scoredActions.items() if v == max_value]
        return Ternary(np.random.choice(max_boards)), max_value
    else:
        minValue = min(scoredActions.values())
        minBoards = [b for b, v in scoredActions.items() if v == minValue]
        return Ternary(np.random.choice(minBoards)), minValue


if __name__ == "__main__":
    playAgain = True
    while playAgain:
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
                    _action = int(input(f"Action {_action} is already used, try new (0-8): "))

                _actionBoard = list(_board.number)
                _actionBoard[_action] = str(_player)

                _board = Ternary("".join(_actionBoard))

            _winner = determineWinner(_board)
            _turn += 1

        print(f"\nWinner: {_winner}\n")
        print(plot(_board))

        playAgain = input("Play again [y/n]: ") == "y"
