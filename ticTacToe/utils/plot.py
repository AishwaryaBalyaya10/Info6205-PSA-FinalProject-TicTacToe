from typing import Union

from ticTacToe.utils.ternary import Ternary, gameToTernary, ternaryToXandO


def plot(game: Union[str, Ternary]) -> str:
    template = " {0} | {1} | {2} \n" "---+---+---\n" " {3} | {4} | {5} \n" "---+---+---\n" " {6} | {7} | {8} "

    if not isinstance(game, Ternary):
        board = gameToTernary(game)
    else:
        board = game

    x_o = ternaryToXandO(board)
    return template.format(*x_o)


def valuePlotting(game: Union[str, Ternary], dictonary: dict, decimal: bool = True) -> str:
    template = (
        " {0} | {1} | {2} \n"
        "-------+-------+------\n"
        " {3} | {4} | {5} \n"
        "-------+-------+------\n"
        " {6} | {7} | {8} \n"
    )

    if not isinstance(game, Ternary):
        board = gameToTernary(game)
    else:
        board = game

    values = []

    for k, a in enumerate(ternaryToXandO(board)):
        if a != " ":
            values.append(f"  {a}  ")
            continue
        if decimal:
            values.append("{0:.3f}".format(round(dictonary[k], 3)))
        else:
            values.append("  {0}  ".format(round(dictonary[k])))

    return template.format(*values)
