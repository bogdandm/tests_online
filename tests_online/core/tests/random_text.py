import operator
from functools import reduce
from random import choice, randint, random
from typing import Tuple

import requests

word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = requests.get(word_site)
WORDS = [w.lower() for w in response.content.decode().splitlines() if len(w) > 2]
del response

ENDS_RATES = {
    ".": 100,
    "?": 15,
    "!": 4
}
ENDS_CHARS = reduce(operator.add, map(lambda x: [x[0]] * x[1], ENDS_RATES.items()))
COMMA_RATE = (3, 20)
COMMA_MEAN = round(sum(COMMA_RATE) / 2)
COMMA_DELTA = COMMA_RATE[1] - COMMA_RATE[0]


def rand_square(mean, delta):
    """
    Parabolic distribution
    (Normal dist would be better, but it's difficult to implement without scipy)
    :param mean:
    :param delta:
    :return:
    """
    return round(mean + delta * random() ** 2)


def random_word():
    return choice(WORDS)


def random_sentences(words=100, words_delta=20):
    """
    Generate pseudo-random sentence with given params:
    count := words +- words_delta
    :param words: mean
    :param words_delta: std
    :return:
    """

    def gen(words_count):
        sep_flag = rand_square(COMMA_MEAN, COMMA_DELTA)
        for i in range(words_count):
            if (i + 1) % sep_flag == 0:
                sep = ", "
                sep_flag = rand_square(COMMA_MEAN, COMMA_DELTA)
            else:
                sep = " "
            if random() > .3:
                word = random_word()
            else:
                word = random_word()[:randint(1, 4)] + " " + random_word()
            yield word + sep
        yield random_word()

    count = round(rand_square(words, words_delta))
    return "".join(gen(count)).capitalize() + choice(ENDS_CHARS)


def random_paragraph(words=Tuple[int, int], sentences=Tuple[int, int]):
    return " ".join(random_sentences(*words) for i in range(rand_square(*sentences)))
