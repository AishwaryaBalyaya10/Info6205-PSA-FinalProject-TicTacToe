from ticTacToe.utils.ternary import Ternary
from ticTacToe.utils.plot import plot


def test_plot():
    board_ternary = Ternary("210102020")
    game = "01735"

    expected = " X | O |   \n---+---+---\n O |   | X \n---+---+---\n   | X |   "

    assert plot(board_ternary) == expected
    assert plot(game) == expected
