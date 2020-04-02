from hashlib import sha1
from hashlib import sha224
from hashlib import sha256
from hashlib import sha384
from hashlib import sha512
from hashlib import md5


class BloomFilter:
    def __init__(self):
        self.bits = [0 for i in range(1000)]
        self.hash_functions = [sha1, sha224, sha256, sha384, sha512, md5]

    def __contains__(self, item):
        item_b = bytearray(item, "UTF-8")
        for hash_function in self.hash_functions:
            index = int(hash_function(item_b).hexdigest(), 16) % len(self.bits)
            if self.bits[index] == 0:
                return False
        return True

    def add(self, item):
        item_b = bytearray(item, "UTF-8")
        for hash_function in self.hash_functions:
            index = int(hash_function(item_b).hexdigest(), 16) % len(self.bits)
            self.bits[index] = 1
