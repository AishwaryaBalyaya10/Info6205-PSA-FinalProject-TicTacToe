from ticTacToe.utils.ternary import Ternary
from ticTacToe.utils.combinations import getBoardSymmetries, determineWinner


def test_getBoardSymmetries():
    board = "221100002"
    symmetries = getBoardSymmetries(board)
    expected_symmetries = {
        "210200102",
        "012002201",
        "002100221",
        "200001122",
        "201002012",
        "102200210",
        "122001200",
        "221100002",
    }

    for s in symmetries:
        assert s in expected_symmetries


def test_determineWinner():
    x_is_winner = Ternary("222001011")
    o_is_winner = Ternary("210212011")
    no_winner_yet = Ternary("210102001")
    draw = Ternary("121211212")

    assert determineWinner(x_is_winner) == 2
    assert determineWinner(o_is_winner) == 1
    assert determineWinner(draw) == 0
    assert determineWinner(no_winner_yet) == -1
