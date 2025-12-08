#1
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None    


#2
class HashTableChain:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            new_node = Node(key, value)
            new_node.next = self.table[index]
            self.table[index] = new_node
            self.size += 1

    def get(self, key):
        index = self._hash(key)

        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(key)

    def delete(self, key):
        index = self._hash(key)

        previous = None
        current = self.table[index]

        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            previous = current
            current = current.next

        raise KeyError(key)

    def __len__(self):
        return self.size

    def __contains__(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def __n__(self):
        elements = []
        for i in range(self.capacity):
            current = self.table[i]
            while current:
                elements.append((current.key, current.value))
                current = current.next
        return n(elements)


#3
class HashTableOpenAddress:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity
        self.DELETED = object()
    
    def _hash(self, key):
        return hash(key) % self.capacity
    
    def _probe(self, key, attempt):
        return (self._hash(key) + attempt) % self.capacity
    
    def insert(self, key, value):
        if self.size >= self.capacity:
            raise Exception("Hash table is full")
        
        for attempt in range(self.capacity):
            index = self._probe(key, attempt)
            
            if self.table[index] is None or self.table[index] == self.DELETED:
                self.table[index] = Node(key, value)
                self.size += 1
                return
            elif self.table[index].key == key:
                self.table[index].value = value
                return
        
        raise Exception("Hash table is full")
    
    def get(self, key):
        for attempt in range(self.capacity):
            index = self._probe(key, attempt)
            if self.table[index] is None:
                raise KeyError(key)
            if self.table[index] == self.DELETED:
                continue
            if self.table[index].key == key:
                return self.table[index].value
        
        raise KeyError(key)
    
    def delete(self, key):
        for attempt in range(self.capacity):
            index = self._probe(key, attempt)

            if self.table[index] is None:
                raise KeyError(key)
            
            if self.table[index] == self.DELETED:
                continue
                
            if self.table[index].key == key:
                self.table[index] = self.DELETED
                self.size -= 1
                return
        
        raise KeyError(key)
    
    def __len__(self):
        return self.size
    
    def __contains__(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False
    
    def __n__(self):
        result = []
        for i, item in enumerate(self.table):
            if item is None:
                result.append(f"{i}: None")
            elif item == self.DELETED:
                result.append(f"{i}: DELETED")
            else:
                result.append(f"{i}: ({item.key}, {item.value})")
        return "\n".join(result)


# +
#4
def peresechenie(a, b):
    hash_table = HashTableChain(len(a))
    
    for element in a:
        hash_table.insert(element, True)
    
    for element in b:
        if element in hash_table:
            return True
    
    return False

a, b = [1, 2, 3, 4], [1, 5, 6]
print(peresechenie(a,b))


# +
#5
def unique_el(n):
    hash_table = HashTableChain(len(n))
    
    for element in n:
        if element in hash_table:
            return False

        hash_table.insert(element, True)
    
    return True

n = [1,2,3,4]
print(unique_el(n))


# +
#6
def pairs_search(n, s):
    pairs = []
    hash_table = HashTableChain(len(n))
    
    for n1 in n:
        n2 = s - n1
        
        if n2 in hash_table:
            pairs.append((n2, n1))
        
        hash_table.insert(n1, True)
    
    return pairs

n = [1,2,3,4]
s = 5
print(pairs_search(n, s))


# +
#7
def anagrams(n1, n2):
    if len(n1) != len(n2):
        return False
    
    char_count = HashTableChain(len(n1))
    
    for char in n1:
        if char in char_count:
            current_count = char_count.get(char)
            char_count.insert(char, current_count + 1)
        else:
            char_count.insert(char, 1)
    
    for char in n2:
        if char not in char_count:
            return False
        
        current_count = char_count.get(char)
        if current_count == 1:
            char_count.delete(char)
        else:
            char_count.insert(char, current_count - 1)
    
    return len(char_count) == 0

n1, n2 = '1234', '4322'
print(anagrams(n1, n2))
# -


