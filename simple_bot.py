import random
from mastermind import bulls_cows


class SimpleBot:
    def __init__(self, num_colors, num_symbols, repetition):
        self.num_colors = num_colors
        self.num_symbols = num_symbols
        self.repetition = repetition
        self.enigma = bytearray()
        if repetition:
            for i in range(num_symbols):
                self.enigma.append(random.randrange(0, num_colors))
        else:
            self.enigma = bytearray(random.sample(range(num_colors), num_symbols))

    def get_answer(self, guess):
        return bulls_cows(self.enigma, guess)

    def get_greeting(self):
        msg = 'с повторениями' if self.repetition else 'без повторений'
        return f'Я загадал комбинацию из {self.num_symbols} цифр от 1 до {self.num_colors} {msg}.\n' \
               f'Попробуйте её отгадать!'
