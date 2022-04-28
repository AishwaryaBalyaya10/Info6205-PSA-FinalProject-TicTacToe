import numpy as np
import logging
from typing import Dict, Tuple

from ticTacToe.utils.plot import plot
from ticTacToe.utils.ternary import Ternary
from ticTacToe.utils.combinations import determineWinner

logging.basicConfig(filename='logs/minmax.log', level=logging.INFO, filemode='a', format='%(asctime)s - %(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')



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
        newBoard = "".join(actionBoard)
        _, scoredActions[newBoard] = minimax(Ternary(newBoard), depth, player)

    if player == activePlayer:
        maxValue = max(scoredActions.values())
        maxBoards = [b for b, v in scoredActions.items() if v == maxValue]
        return Ternary(np.random.choice(maxBoards)), maxValue
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
                logging.info(plot(_board))
                action = int(input("Human turn (0-8): "))
                while action not in np.where(np.array(list(_board.number)) == "0")[0]:
                    action = int(input(f"Action {action} is already used, try new (0-8): "))

                _actionBoard = list(_board.number)
                _actionBoard[action] = str(_player)

                _board = Ternary("".join(_actionBoard))

            _winner = determineWinner(_board)
            _turn += 1

        logging.info("Turns " + str(_turn))

        print(f"\nWinner: {_winner}\n")
        print(f"\nWinner: {'Menace' if _winner == 2 else 'Human'}\n")
        print(plot(_board))
        logging.info(f"Winner: {'Menace' if _winner == 2 else 'Human'}")
        logging.info("\n" + plot(_board))

        playAgain = input("Play again [y/n]: ") == "y"
