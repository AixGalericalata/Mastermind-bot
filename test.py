from mastermind import bulls_cows
from utils import to_byte_array


def test():
    assert bulls_cows(to_byte_array('12444', 5, 8, True),
                      to_byte_array('14244', 5, 8, True)) == (3, 2)
    assert bulls_cows(to_byte_array('1111', 4, 8, True),
                      to_byte_array('2222', 4, 8, True)) == (0, 0)
    assert bulls_cows(to_byte_array('222222', 6, 8, True),
                      to_byte_array('222222', 6, 8, True)) == (6, 0)
