import numpy as np
from typing import List, Tuple, Set

from ticTacToe.utils.ternary import Ternary


SYMMETRICAL_COMBINATIONS = [
    np.array([0, 1, 2, 3, 4, 5, 6, 7, 8]),
    np.array([0, 3, 6, 1, 4, 7, 2, 5, 8]),
    np.array([6, 3, 0, 7, 4, 1, 8, 5, 2]),
    np.array([6, 7, 8, 3, 4, 5, 0, 1, 2]),
    np.array([8, 7, 6, 5, 4, 3, 2, 1, 0]),
    np.array([8, 5, 2, 7, 4, 1, 6, 3, 0]),
    np.array([2, 5, 8, 1, 4, 7, 0, 3, 6]),
    np.array([2, 1, 0, 5, 4, 3, 8, 7, 6]),
]


def getBoardSymmetries(board: str) -> List[str]:
    board_array = np.array(list(board))

    symmetrical_board_list = []
    for p in SYMMETRICAL_COMBINATIONS:
        symmetry = list(board_array[p])
        symmetry_board_str = "".join([str(s) for s in symmetry])
        symmetrical_board_list.append(symmetry_board_str)

    return symmetrical_board_list


def getAllPossibleBoards(player_start: int = 2, exclude_winners: bool = True) -> Tuple[List[List[str]], List[Set[str]]]:
    possibleBoards = [set(), set(), set(), set(), set(), set(), set(), set(), set(), set()]
    boardClasses = [[], [], [], [], [], [], [], [], [], []]
    possibleBoards[0].add("000000000")
    boardClasses[0].append("000000000")

    for r in range(1, 10):
        player = int((r + player_start) % 2 + 1)
        for s in boardClasses[r - 1]:
            possible_moves = np.where(np.array(list(s)) == "0")[0]
            for a in possible_moves:
                temporaryBoard = list(s)
                temporaryBoard[int(a)] = str(player)
                board = "".join(temporaryBoard)

                # Game end
                if exclude_winners and determineWinner(Ternary(board)) >= 0:
                    continue

                # We allow winning boards, but exclude boards which ended round ago
                if not exclude_winners and determineWinner(Ternary(s)) >= 0:
                    continue

                # If board already exists
                if board in possibleBoards[r]:
                    continue

                boardSymmetries = getBoardSymmetries(board)
                possibleBoards[r].update(boardSymmetries)
                boardClasses[r].append(board)

    return boardClasses, possibleBoards


def determineWinner(board: Ternary) -> int:
    winningWays = [
        board.number[0] + board.number[1] + board.number[2],
        board.number[3] + board.number[4] + board.number[5],
        board.number[6] + board.number[7] + board.number[8],
        board.number[0] + board.number[3] + board.number[6],
        board.number[1] + board.number[4] + board.number[7],
        board.number[2] + board.number[5] + board.number[8],
        board.number[0] + board.number[4] + board.number[8],
        board.number[6] + board.number[4] + board.number[2],
    ]

    # Check if winner is X or O
    for winner, s in enumerate(["111", "222"]):
        for ww in winningWays:
            if s == ww:
                return winner + 1

    # It's a draw
    if "0" not in board.number:
        return 0

    # Game has not ended
    return -1
