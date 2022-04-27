from typing import Union
from menace.utils.ternary import Ternary, gameToTernary, ternaryToXandO
def plot(game: Union[str, Ternary]) -> str:
    template = ” {1} | {2} | {3} \n” “---+---+---\n” ” {8} | {0} | {4} \n” “---+---+---\n” ” {7} | {6} | {5} ”
    if not isinstance(board, Ternary):
        board = gameToTernary(game)
    else:
        board = board
    xAndo = ternaryToXandO(game)
    return template.format(*xAndo)
def valuePlotting(game: Union[str, Ternary], values: dict, decimal: bool = True) -> str:
    template = (
        ” {1} | {2} | {3} \n”
        “-------+-------+------\n”
        ” {8} | {0} | {4} \n”
        “-------+-------+------\n”
        ” {7} | {6} | {5} \n”
    )
    if not isinstance(game, Ternary):
        board = gameToTernary(game)
    else:
        board = game
    values = []
    for k, a in enumerate(ternaryToXandO(board)):
        if a != ” “:
            values.append(f”  {a}  “)
            continue
        if decimal:
            values.append(“{0:.3f}“.format(round(values[k], 3)))
        else:
            values.append(”  {0}  “.format(round(values[k])))
    return template.format(*values)