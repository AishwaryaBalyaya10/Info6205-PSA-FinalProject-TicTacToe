import numpy as np
from typing import Tuple, Dict
from copy import deepcopy

from ticTacToe.utils.ternary import Ternary
from ticTacToe.utils.plot import plot, valuePlotting
from ticTacToe.utils.combinations import determineWinner

np.set_printoptions(suppress=True)

VALUE_X: Dict = {}
VALUE_O: Dict = {}
DEFAULT_VALUE = 0.5
EPSILON = 0.05
ALPHA = 0.5


def getValue(board: Ternary, player: int) -> Tuple[Ternary, float]:
    v = VALUE_X if player == 2 else VALUE_O

    if (w := determineWinner(board)) >= 0:
        v[board.number] = (w == player) * 1
        return board, v[board.number]

    return board, v.get(board.number, DEFAULT_VALUE)


def actions(board: Ternary, player: int) -> Tuple[int, Ternary]:
    """Choose action at random from the set of available actions"""
    actions = np.where(np.array(list(board.number)) == "0")[0]
    action_chosen = np.random.choice(actions, 1)[0]

    action_board = list(board.number)
    action_board[action_chosen] = str(player)

    return action_chosen, Ternary("".join(action_board))


def exploit(board: Ternary, player: int) -> Tuple[int, Ternary, Dict]:
    """Choose action with the highest value from player's value function"""
    actions = np.where(np.array(list(board.number)) == "0")[0]
    best_action_value = -99.0
    best_action_hash = Ternary("0" * 9)
    best_action = 0
    action_values: Dict = {}

    for a in actions:
        action_board = list(board.number)
        action_board[a] = str(player)
        action_hash, action_value = getValue(Ternary("".join(action_board)), player)
        action_values[a] = action_value

        if best_action_value < action_value:
            best_action_value = action_value
            best_action_hash = deepcopy(action_hash)
            best_action = a

    return best_action, best_action_hash, action_values


def train(num_rounds=10000):
    for r in range(1, num_rounds + 1):
        board = Ternary("0" * 9)
        turn = 1
        winner = -1
        game = ""
        history_x = []
        history_o = []

        # Play game
        while winner < 0:
            player = turn % 2 + 1

            # Explore move
            if np.random.uniform(0, 1) < EPSILON:
                action, board_hash = actions(board, player)
            # Exploit move
            else:
                action, board_hash, _ = exploit(board, player)

            if player == 2:
                history_x.append(board_hash)
            else:
                history_o.append(board_hash)

            game += str(action)

            action_board = list(board.number)
            action_board[action] = str(player)

            board = Ternary("".join(action_board))
            winner = determineWinner(board)
            turn += 1

        reward_x = (winner == 2) * 1.0
        reward_o = (winner == 1) * 1.0

        # Assign values player X
        for h in history_x[::-1]:
            _, v = getValue(h, 2)
            VALUE_X[h.number] = v + ALPHA * (reward_x - v)
            reward_x = deepcopy(VALUE_X[h.number])

        # Assign values player O
        for h in history_o[::-1]:
            _, v = getValue(h, 1)
            VALUE_O[h.number] = v + ALPHA * (reward_o - v)
            reward_o = deepcopy(VALUE_O[h.number])

        # Logging
        if r % (num_rounds // 10) == 0:
            print(f"\nGame: {game}, winner: {winner}, round: {r}\n")
            print(plot(game))


if __name__ == "__main__":
    print("Training...")
    train()
    print("Training finished!")
