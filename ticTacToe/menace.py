import numpy as np
from typing import Tuple, Dict, List

from utils.ternary import Ternary
from utils.plot import plot, plot_values
from utils.combinations import (
    determineWinner,
    getAllPossibleBoards,
    getBoardSymmetries,
    SYMMETRICAL_COMBINATIONS,
)

np.set_printoptions(suppress=True)

# D. Michie used 4, 3, 2, 1 / 8, 4, 2, 1
REPLICAS_PER_STAGE = [8, 4, 2, 1]
REWARDS = {"won": 3, "draw": 1, "lost": -1}
MENACE_MEMORY: Dict = {0: {}, 1: {}}


class MenaceException(Exception):
    pass


def getPossibleOptions(boardClasses: List, board: str, stage: int) -> List:
    if stage == 7:
        return np.where(np.array(list(board)) == "0")[0]

    actions = []

    for b in boardClasses[stage + 1]:
        diff = Ternary(board) - Ternary(b)
        not_null = np.where(np.array(list(diff)) != "0")[0]

        if len(not_null) == 1:
            actions.append(not_null[0])

    return np.array(actions)


def initiate_menace_memory():
    boardClasses, _ = getAllPossibleBoards()
    for stage, boards in enumerate(boardClasses[:-2]):
        turn = stage // 2

        for b in boards:
            actions = np.where(np.array(list(b)) == "0")[0] if stage > 0 else np.array([0, 1, 2])

            MENACE_MEMORY[stage % 2][b] = []

            for a in actions:
                MENACE_MEMORY[stage % 2][b].extend([int(a)] * REPLICAS_PER_STAGE[turn])


def menaceMove(board: Ternary, player: int = 2) -> Tuple[Ternary, int, str, Dict]:
    boardList = list(board.number)
    actions = np.where(np.array(boardList) == "0")[0]

    if len(actions) == 1:
        boardList[actions[0]] = str(player)
        return Ternary("".join(boardList)), actions[0], board.number, {a: 0 for a in range(9)}

    symmetryClass = None
    symmetryElement = SYMMETRICAL_COMBINATIONS[0]

    if board.number in MENACE_MEMORY[player % 2]:
        symmetryClass = board.number
    else:
        for e, s in enumerate(getBoardSymmetries(board.number)):
            if s in MENACE_MEMORY[player % 2]:
                symmetryClass = s
                symmetryElement = SYMMETRICAL_COMBINATIONS[e]

    if symmetryClass is None:
        raise MenaceException(f"Any symmetry class found for {board.number} in MENACE's memory")

    try:
        action = np.random.choice(MENACE_MEMORY[player % 2][symmetryClass])
    except ValueError:
        raise MenaceException("MENACE's memory has died out")

    actionForOriginalBoard = symmetryElement[action]
    boardList[actionForOriginalBoard] = str(player)

    action_histogram = {
        a: len(np.where(np.array(MENACE_MEMORY[player % 2][symmetryClass]) == a)[0]) + 0.1 for a in range(9)
    }
    return Ternary("".join(boardList)), action, symmetryClass, action_histogram


def makeMenaceLearn(history: List, winner: int, player: int = 2) -> None:
    if len(history) == 5:
        history = history[:-1]

    # Game hasn't ended yet
    if winner < 0:
        return

    if winner not in [player, 0]:
        for action, symmetryClass in history:
            for _ in range(abs(REWARDS["lost"])):
                MENACE_MEMORY[player % 2][symmetryClass].remove(action)

        return

    result = "won" if winner == player else "draw"
    for action, symmetryClass in history:
        MENACE_MEMORY[player % 2][symmetryClass].extend([action] * REWARDS[result])

    return


def randomPlayer(board: Ternary, player: int = 1) -> Tuple[Ternary, int]:
    boardList = list(board.number)
    actions = np.where(np.array(boardList) == "0")[0]
    action = np.random.choice(actions)
    boardList[action] = str(player)
    return Ternary("".join(boardList)), action


def humanPlayer(board: Ternary, player: int = 1) -> Tuple[Ternary, int]:
    boardList = list(board.number)
    action = int(input("Human turn (0-8): "))
    while action not in np.where(np.array(list(board.number)) == "0")[0]:
        action = int(input(f"Action {action} is already used, try new (0-9): "))

    boardList[action] = str(player)
    return Ternary("".join(boardList)), action


def trainMenace(num_rounds=100):
    for r in range(1, num_rounds + 1):
        board = Ternary("0" * 9)
        winner = -1
        turn = 1
        menace_actions = []

        while winner < 0:
            player = turn % 2 + 1
            if player == 2:
                board, action, symmetryClass, _ = menaceMove(board)
                menace_actions.append((action, symmetryClass))
            else:
                board, _ = randomPlayer(board)

            turn += 1

            winner = determineWinner(board)
            makeMenaceLearn(menace_actions, winner)

        # Logging
        if r % (num_rounds // 10) == 0:
            action_histogram = {a: len(np.where(np.array(MENACE_MEMORY[0]["0" * 9]) == a)[0]) for a in range(9)}
            print(plot_values(Ternary("0" * 9), action_histogram, decimal=False))


if __name__ == "__main__":
    initiate_menace_memory()
    print("trainMenaceing...")
    trainMenace()
    print("trainMenaceing finished!")
    print("-------------------------")
    print("Human vs Menace")

    play_again = True
    while play_again:
        _board = Ternary("0" * 9)
        _winner = -1
        _turn = 1
        _menaceActions = []
        _actionValues = {a: len(np.where(np.array(MENACE_MEMORY[0]["0" * 9]) == a)[0]) for a in range(9)}

        while _winner < 0:
            _player = _turn % 2 + 1
            if _player == 2:
                print(_actionValues)
                print(plot_values(_board, _actionValues, decimal=False))
                _board, _action, _symmetryClass, _actionValues = menaceMove(_board)
                _menaceActions.append((_action, _symmetryClass))

            else:
                print(plot(_board))
                _board, _ = humanPlayer(_board)

            _winner = determineWinner(_board)
            _turn += 1

        makeMenaceLearn(_menaceActions, _winner)

        print(f"\nWinner: {_winner}\n")
        print(plot(_board))

        play_again = input("Play again [y/n]: ") == "y"
