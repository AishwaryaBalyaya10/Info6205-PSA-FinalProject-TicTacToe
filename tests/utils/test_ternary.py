from ticTacToe.utils.ternary import (
    Ternary,
    decimalToTernary,
    gameToTernary,
    ternaryToXandO,
)


def test_decimalToTernary():
    ternary_number = decimalToTernary(10)

    assert ternary_number.number == "000000101"
    assert ternary_number.decimal == 10
    assert isinstance(ternary_number, Ternary)


def test_gameToTernary():
    game = "03128"
    assert gameToTernary(game).number == "221100002"


def test_ternaryToXandO():
    ternary_number = Ternary("221100002")
    assert ternaryToXandO(ternary_number) == ["X", "X", "O", "O", " ", " ", " ", " ", "X"]
