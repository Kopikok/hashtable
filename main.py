from hashlib import sha256

from filter import BloomFilter


class Iteration:
    """
    Итерация для хеш-таблицы
    """
    def __iter__(self):
        for elem in self.items:
            if elem is not None and not isinstance(elem, LinkedList):
                yield elem
            elif elem is not None and isinstance(elem, LinkedList):
                element = elem.head
                while element:
                    yield element
                    element = element.next


class LinkedList:
    """
    Связной список, написанный для разрешения коллизий,
    содержит:
    1. __init__()
    2. __str__()
    3. __iter__()
    4. __len__()
    5. push()
    6. remove()
    """
    def __init__(self, head=None):
        self.head = head

    def __str__(self):
        result = ""
        element = self.head
        while element:
            result = result + str(element) + ' '
            element = element.next
        return result

    def __iter__(self):
        element = self.head
        while element:
            yield element
            element = element.next

    def __len__(self):
        counter = 0
        for i in self:
            counter += 1
        return counter

    def push(self, item):
        """
        Вставка элемента в начало связного списка
        """
        item.next = self.head
        self.head = item

    def remove(self, value):
        """
        1. Если первый элемент начала списка равен ключу, то
        меняем ссылаемый объект на ссылаемый объект
        2. В другом случае, идем по объектам, пока ссылаемый объект
        не будет равен ключу, и потом когда находим, меняем ссылаемый объект
        на ссылаемый ссылаемого объекта
        """
        if self.head[0] == value:
            self.head = self.head.next
        else:
            for element in self:
                if element.next is not None:
                    if element.next[0] == value:
                        try:
                            element.next = element.next.next
                        except AttributeError:
                            element.next = None


class Node(tuple):
    """
    Узел для разрешения коллизий и, соответсвенно для
    создания связных списков
    """
    def __init__(self, *args):
        super().__init__()
        self.next = None


class HashTable(Iteration):
    """
    Хеш-таблица, родительским классом которым является класс Iteration,
    содержит в себе:
    1. __init__()
    2. add(x)
    3. remove(x)
    4. x in HashTable
    5. len(HashTable)
    где x - ключ
    """
    def __init__(self):
        self.filter = BloomFilter()
        self.items = [None for i in range(50)]

    def __contains__(self, item):
        for elem in self:
            if elem[0] == item:
                return True
        return False

    def __len__(self):
        length = 0
        for i in self.items:
            if isinstance(i, LinkedList):
                length += len(i)
            elif i is not None:
                length += 1
        return length

    def add(self, key, val):
        """
        1. Хешируем, остаток = индекс
        2. Если иднекс не пуст и не содержит связной список, то
        мы создаем связной список и вставляем туда значение ячейки
        и то, что мы хотим вставить
        2.1 Если индекс не пуст и содержит связной список, то мы
        вставляем в него наше значение
        2.2 Иначе ячейка заменяется на значение
        """
        self.filter.add(key)
        s_b = bytearray(str(key), "UTF-8")
        sha_res = sha256(s_b).hexdigest()
        h_s = int(sha_res, 16)
        index = h_s % len(self.items)
        cargo = Node([key, val])
        if self.items[index] is not None and not isinstance(self.items[index], LinkedList):
            buffer = self.items[index]
            self.items[index] = LinkedList()
            self.items[index].push(buffer)
            self.items[index].push(cargo)
        elif self.items[index] is not None and isinstance(self.items[index], LinkedList):
            self.items[index].push(cargo)
        else:
            self.items[index] = cargo

    def remove(self, key):
        """
        1. Хешируем, остаток = индекс
        2. Если в ячейке лежит узел, то мы заменяем его
        на объект его ссылки, то есть на None
        2.1. Иначе мы вызываем метод remove у связного списка
        """
        s_b = bytearray(str(key), "UTF-8")
        sha_res = sha256(s_b).hexdigest()
        h_s = int(sha_res, 16)
        index = h_s % len(self.items)
        if isinstance(self.items[index], Node):
            self.items[index] = self.items[index].next
        elif isinstance(self.items[index], LinkedList):
            self.items[index].remove(key)

    def pre_contains(self, item):
        return item in self.filter
