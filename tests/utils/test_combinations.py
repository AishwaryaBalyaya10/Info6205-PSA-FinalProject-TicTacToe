from ticTacToe.utils.ternary import Ternary
from ticTacToe.utils.combinations import getBoardSymmetries, determineWinner


def test_getBoardSymmetries():
    board = "221100002"
    symmetries = getBoardSymmetries(board)
    expected_symmetries = {
        "200001122",
        "200022110",
        "200112200",
        "202211000",
        "210000221",
        "211220000",
        "222000011",
        "221100002",
    }

    for s in symmetries:
        assert s in expected_symmetries


def test_determineWinner():
    x_is_winner = Ternary("221002020")
    o_is_winner = Ternary("210202011")
    no_winner_yet = Ternary("210102020")
    draw = Ternary("221211211")

    assert determineWinner(x_is_winner) == 2
    assert determineWinner(o_is_winner) == 1
    assert determineWinner(draw) == 0
    assert determineWinner(no_winner_yet) == -1
