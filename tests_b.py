from random import randint
from random import choice

from main import BloomFilter


def generate_string():
    s = ""
    n = randint(1, 100)
    for i in range(n):
        s = s + chr(randint(65, 122))
    return s


def test_structure():
    b = BloomFilter()
    n = randint(1, 100)
    array = [generate_string() for i in range(n)]
    for element in array:
        b.add(element)
    k = randint(1, len(array))
    for i in range(k):
        assert (choice(array) in b) is True
