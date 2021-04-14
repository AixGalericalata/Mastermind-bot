import random
from mastermind import bulls_cows


class SimpleBot:
    def __init__(self, num_colors, num_symbols):
        self.num_colors = num_colors
        self.num_symbols = num_symbols
        self.enigma = bytearray()
        for i in range(num_symbols):
            self.enigma.append(random.randrange(0, num_colors))

    def get_answer(self, guess):
        return bulls_cows(self.enigma, guess)

    def get_greeting(self):
        return f'Я загадал комбинацию из {self.num_symbols} цифр от 0 до {self.num_colors - 1}.\n' \
               f'Попробуйте её отгадать!'
