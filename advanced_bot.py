from mastermind import bulls_cows
import itertools
from base_bot import BaseBot


def penalty(bulls_cows):
    best_bulls = 0
    best_cows = 1.5
    return (bulls_cows[0] - best_bulls) * (bulls_cows[0] - best_bulls) + (
            bulls_cows[1] - best_cows) * (bulls_cows[1] - best_cows)


class AdvancedBot(BaseBot):
    def __init__(self, num_colors, num_symbols, repetition):
        super().__init__(num_colors, num_symbols, repetition)
        self.answers = list(
            map(lambda x: bytearray(x),
                itertools.product(range(self.num_colors), repeat=self.num_symbols)))

    def get_answer(self, guess):
        dict_answers = {}
        for answer in self.answers:
            bulls_and_cows = bulls_cows(answer, guess)
            if bulls_and_cows in dict_answers:
                dict_answers[bulls_and_cows].append(answer)
            else:
                dict_answers[bulls_and_cows] = [answer]
        answers = dict_answers.keys()
        n = min(answers, key=penalty)
        self.answers = dict_answers[n]
        return n
