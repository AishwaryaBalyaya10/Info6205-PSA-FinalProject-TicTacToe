import numpy as np
import logging
from typing import Tuple, Dict, List

from ticTacToe.utils.ternary import Ternary
from ticTacToe.utils.plot import plot, valuePlotting
from ticTacToe.utils.combinations import (
    determineWinner,
    getAllPossibleBoards,
    getBoardSymmetries,
    SYMMETRICAL_COMBINATIONS,
)

np.set_printoptions(suppress=True)

logging.basicConfig(filename='logs/menace.log', level=logging.INFO, filemode='a', format='%(asctime)s - %(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')

# D. Michie used 4, 3, 2, 1 / 8, 4, 2, 1
REPLICAS_PER_STAGE = [8, 4, 2, 1]
REWARDS = {"won": 3, "draw": 1, "lost": -1}
MENACE_MEMORY: Dict = {0: {}, 1: {}}
TOTAL_GAMES = 100
STATS = {"matches": 0, "menaceWins": 0, "menaceLost": 0, "menaceDraws": 0}


class MenaceException(Exception):
    pass


def getActions(board_classes: List, board: str, stage: int) -> List:
    if stage == 7:
        return np.where(np.array(list(board)) == "0")[0]

    actions = []

    for b in board_classes[stage + 1]:
        diff = Ternary(board) - Ternary(b)
        not_null = np.where(np.array(list(diff)) != "0")[0]

        if len(not_null) == 1:
            actions.append(not_null[0])

    return np.array(actions)


def initMenace():
    board_classes, _ = getAllPossibleBoards()
    for stage, boards in enumerate(board_classes[:-2]):
        turn = stage // 2
        for b in boards:
            actions = np.where(np.array(list(b)) == "0")[0] if stage > 0 else np.array([0, 1, 2])
            MENACE_MEMORY[stage % 2][b] = []

            for a in actions:
                MENACE_MEMORY[stage % 2][b].extend([int(a)] * REPLICAS_PER_STAGE[turn])


def menaceMove(board: Ternary, player: int = 2) -> Tuple[Ternary, int, str, Dict]:
    listOfBoards = list(board.number)
    actions = np.where(np.array(listOfBoards) == "0")[0]

    if len(actions) == 1:
        listOfBoards[actions[0]] = str(player)
        return Ternary("".join(listOfBoards)), actions[0], board.number, {a: 0 for a in range(9)}

    symmetricalClass = None
    symmetricalElement = SYMMETRICAL_COMBINATIONS[0]

    if board.number in MENACE_MEMORY[player % 2]:
        symmetricalClass = board.number
    else:
        for e, s in enumerate(getBoardSymmetries(board.number)):
            if s in MENACE_MEMORY[player % 2]:
                symmetricalClass = s
                symmetricalElement = SYMMETRICAL_COMBINATIONS[e]

    if symmetricalClass is None:
        raise MenaceException(f"Any symmetry class found for {board.number} in MENACE's memory")

    try:
        action = np.random.choice(MENACE_MEMORY[player % 2][symmetricalClass])
    except ValueError:
        raise MenaceException("MENACE's memory died out")

    actionOnBoard = symmetricalElement[action]
    listOfBoards[actionOnBoard] = str(player)

    actionHistogram = {
        a: len(np.where(np.array(MENACE_MEMORY[player % 2][symmetricalClass]) == a)[0]) + 0.1 for a in range(9)
    }
    return Ternary("".join(listOfBoards)), action, symmetricalClass, actionHistogram


def menaceTrain(history: List, winner: int, player: int = 2) -> None:
    if len(history) == 5:
        history = history[:-1]

    # Game hasn't ended yet
    if winner < 0:
        return

    if winner not in [player, 0]:
        for action, symmetricalClass in history:
            for _ in range(abs(REWARDS["lost"])):
                MENACE_MEMORY[player % 2][symmetricalClass].remove(action)

        return

    result = "won" if winner == player else "draw"
    for action, symmetricalClass in history:
        MENACE_MEMORY[player % 2][symmetricalClass].extend([action] * REWARDS[result])

    return


def randomHumanMoves(board: Ternary, player: int = 1) -> Tuple[Ternary, int]:
    listOfBoards = list(board.number)
    actions = np.where(np.array(listOfBoards) == "0")[0]
    action = np.random.choice(actions)
    listOfBoards[action] = str(player)
    return Ternary("".join(listOfBoards)), action


def train(num_rounds=100):
    for r in range(1, num_rounds + 1):
        board = Ternary("0" * 9)
        winner = -1
        turn = 1
        game = ""
        menaceActions = []

        while winner < 0:
            player = turn % 2 + 1

            if player == 2:
                board, action, symmetricalClass, _ = menaceMove(board)
                menaceActions.append((action, symmetricalClass))
            else:
                board, _ = randomHumanMoves(board)

            game = str(board)

            turn += 1

            winner = determineWinner(board)
            menaceTrain(menaceActions, winner)

        # Logging
        if r % (num_rounds // 10) == 0:
            actionHistogram = {a: len(np.where(np.array(MENACE_MEMORY[0]["0" * 9]) == a)[0]) for a in range(9)}
            logging.info(f"\nGame: {game}, winner: {winner}, round: {r}\n")
            logging.info("\n" + valuePlotting(Ternary("0" * 9), actionHistogram, decimal=False))
            print(f"\nGame: {game}, winner: {winner}, round: {r}\n")
            print(valuePlotting(Ternary("0" * 9), actionHistogram, decimal=False))


if __name__ == "__main__":
    gameCount = 0
    initMenace()
    logging.info("-------------------------")
    logging.info("Training...")
    print("-------------------------")
    print("Training...")
    train()
    logging.info("Training finished!")
    logging.info("-------------------------")
    print("Training finished!")
    print("-------------------------")

    play_again = True
    while play_again:
        print("Human Moves vs Menace game count - " + str(gameCount))
        logging.info("Human Moves vs Menace game count - " + str(gameCount))
        _board = Ternary("0" * 9)
        _winner = -1
        _turn = 1
        _menaceActions = []
        _actionValues = {a: len(np.where(np.array(MENACE_MEMORY[0]["0" * 9]) == a)[0]) for a in range(9)}

        while _winner < 0:
            _player = _turn % 2 + 1
            if _player == 2:
                print(_actionValues)
                print(valuePlotting(_board, _actionValues, decimal=False))
                logging.info(_actionValues)
                logging.info("\n" + valuePlotting(_board, _actionValues, decimal=False))
                _board, _action, _symmetricalClass, _actionValues = menaceMove(_board)
                _menaceActions.append((_action, _symmetricalClass))

            else:
                print(plot(_board))
                logging.info("Human moves")
                logging.info("\n" + plot(_board))
                _board, _ = randomHumanMoves(_board)

            _winner = determineWinner(_board)
            _turn += 1

        menaceTrain(_menaceActions, _winner)

        if _winner == 0:
            print('Draw')
            STATS['menaceDraws'] = STATS['menaceDraws'] + 1
            print('Draw count' + str(STATS['menaceDraws']))

        if _winner == 1:
            print('Menace')
            STATS['menaceWins'] = STATS['menaceWins'] + 1
            print('Win count' + str(STATS['menaceWins']))

        if _winner == 2:
            print('Human')
            STATS['menaceLost'] = STATS['menaceLost'] + 1
            print('Lost count' + str(STATS['menaceLost']))

        print(f"\nWinner: {'Menace' if _winner == 2 else 'Human'}\n")
        print(plot(_board))
        logging.info(f"Winner: {'Menace' if _winner == 2 else 'Human'}")
        logging.info("\n" + plot(_board))

        gameCount = gameCount + 1
        STATS['matches'] = gameCount

        if(gameCount==TOTAL_GAMES): 
            print("Stats" + "-- Game -- "+ str(STATS['matches']) + "-- Wins -- "+ str(STATS['menaceWins']) + "-- Draws -- "+ str(STATS['menaceDraws']) + "-- Loss -- "+ str(STATS['menaceLost']))
            logging.info("Stats" + "-- Game -- "+ str(STATS['matches']) + "-- Wins -- "+ str(STATS['menaceWins']) + "-- Draws -- "+ str(STATS['menaceDraws']) + "-- Loss -- "+ str(STATS['menaceLost']))

        play_again = gameCount < TOTAL_GAMES
