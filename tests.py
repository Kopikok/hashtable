from random import randint
from random import choice

from hashlib import sha256

from main import HashTable
from main import LinkedList
from main import Node
from main import Iteration


def generate_string():
    s = ''
    n = randint(1, 100)
    for i in range(n):
        s = s + chr(randint(65, 122))
    return s


def filling_hash_table():
    global n
    global h
    global generating_keys
    for i in range(n):
        a, b = generate_string(), generate_string()
        h.add(a, b)
        generating_keys.append(a)


def test_len():
    global h
    assert len(h) == n


def test_keyword():
    global h
    global generating_keys
    k = randint(1, len(h))
    for i in range(k):
        assert (choice(generating_keys) in h) is True
    for i in range(k):
        s = generate_string()
        if s not in generating_keys:
            assert (s in h) is False


def test_remove():
    global h
    global generating_keys
    k = randint(1, len(generating_keys))
    deleted_keys = []
    for i in range(k):
        key = choice(generating_keys)
        deleted_key = key
        h.remove(deleted_key)
        deleted_keys.append(deleted_key)
        generating_keys.remove(key)
    for element in deleted_keys:
        assert (element in h) is False


generating_keys = []
h = HashTable()
n = randint(1, 1000)
filling_hash_table()
