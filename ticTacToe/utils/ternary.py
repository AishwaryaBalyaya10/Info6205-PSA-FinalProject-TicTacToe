import numpy as np
from typing import Optional, List


class Ternary:
    def __init__(self, number: str, decimal: Optional[int] = None) -> None:
        if isinstance(number, int):
            number = int(number)

        self.number = "0" * (9 - len(number)) + number
        self.decimal = decimal or int(number, 3)

    def __repr__(self) -> str:
        return self.number

    def __sub__(self, other):
        a = np.array([int(i) for i in self.number])
        b = np.array([int(i) for i in other.number])
        diff = a - b

        return "".join([str(abs(i)) for i in diff])


def decimalToTernary(decimal: int) -> Ternary:
    def convert(d: int) -> str:
        q = d / 3
        r = d % 3
        if q == 0:
            return ""
        else:
            return convert(int(q)) + str(int(r))

    ternary = convert(decimal)

    return Ternary(ternary, decimal)


def gameToTernary(play: str) -> Ternary:
    num = ["0"] * 9

    for i, s in enumerate(play):
        # Even positions are X's turns (2), odd are O's (1)
        num[int(s)] = str(((i + 1) % 2) + 1)
    
    return Ternary("".join(num))


def ternaryToXandO(number: Ternary) -> List[str]:
    mapping = {"0": " ", "1": "O", "2": "X"}
    return [mapping[m] for m in str(number.number)]
