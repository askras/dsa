---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.17.3
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

## Хеш-функции и хеш-таблицы

## Задание 1:

```python
class HashTableChaining:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def insert(self, key, value):
        index = self._hash(key)
        bucket = self.table[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        bucket.append((key, value))
        self.count += 1
        
        if self.count / self.size > 0.7:
            self._rehash()
    
    def search(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        
        for k, v in bucket:
            if k == key:
                return v
        return None
    
    def delete(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                return True
        return False
    
    def _rehash(self):
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)
    
    def __str__(self):
        result = []
        for i, bucket in enumerate(self.table):
            if bucket:
                result.append(f"{i}: {bucket}")
        return "\n".join(result)
```

Тест:

```python
print("=== Тестирование HashTableChaining ===")

ht = HashTableChaining(5)

ht.insert("apple", 1)
ht.insert("banana", 2)
ht.insert("cherry", 3)

assert ht.search("apple") == 1, "Ошибка поиска apple"
assert ht.search("banana") == 2, "Ошибка поиска banana"
assert ht.search("cherry") == 3, "Ошибка поиска cherry"
assert ht.search("unknown") is None, "Ошибка поиска неизвестного ключа"
print("✓ Тест вставки и поиска пройден")

ht.insert("apple", 10)
assert ht.search("apple") == 10, "Ошибка обновления значения"
print("✓ Тест обновления значения пройден")

assert ht.delete("banana") == True, "Ошибка удаления существующего ключа"
assert ht.search("banana") is None, "Ошибка: ключ не удален"
assert ht.delete("unknown") == False, "Ошибка удаления несуществующего ключа"
print("✓ Тест удаления пройден")

ht2 = HashTableChaining(1)  
ht2.insert("key1", "value1")
ht2.insert("key2", "value2")
ht2.insert("key3", "value3")

assert ht2.search("key1") == "value1", "Ошибка при коллизии"
assert ht2.search("key2") == "value2", "Ошибка при коллизии"
assert ht2.search("key3") == "value3", "Ошибка при коллизии"
print("✓ Тест коллизий пройден")

print("Все тесты HashTableChaining пройдены успешно!\n")
```

## Задание 2:

```python
class HashTableOpenAddressing:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size
        self.count = 0
        self.DELETED = object()  
    
    def _hash(self, key, i=0):
        return (hash(key) + i) % self.size
    
    def insert(self, key, value):
        if self.count / self.size > 0.7:
            self._rehash()
        
        i = 0
        while i < self.size:
            index = self._hash(key, i)
            
            if self.table[index] is None or self.table[index] is self.DELETED:
                self.table[index] = (key, value)
                self.count += 1
                return
            elif self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            
            i += 1
        
        self._rehash()
        self.insert(key, value)
    
    def search(self, key):
        i = 0
        while i < self.size:
            index = self._hash(key, i)
            
            if self.table[index] is None:
                return None
            elif self.table[index] is not self.DELETED and self.table[index][0] == key:
                return self.table[index][1]
            
            i += 1
        
        return None
    
    def delete(self, key):
        i = 0
        while i < self.size:
            index = self._hash(key, i)
            
            if self.table[index] is None:
                return False
            elif self.table[index] is not self.DELETED and self.table[index][0] == key:
                self.table[index] = self.DELETED
                self.count -= 1
                return True
            
            i += 1
        
        return False
    
    def _rehash(self):
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        self.count = 0
        
        for item in old_table:
            if item is not None and item is not self.DELETED:
                self.insert(item[0], item[1])
    
    def __str__(self):
        result = []
        for i, item in enumerate(self.table):
            if item is not None and item is not self.DELETED:
                result.append(f"{i}: {item}")
            elif item is self.DELETED:
                result.append(f"{i}: DELETED")
        return "\n".join(result)
```

Тесты 

```python
print("=== Тестирование HashTableOpenAddressing ===")

ht = HashTableOpenAddressing(5)

ht.insert("apple", 1)
ht.insert("banana", 2)
ht.insert("cherry", 3)

assert ht.search("apple") == 1, "Ошибка поиска apple"
assert ht.search("banana") == 2, "Ошибка поиска banana"
assert ht.search("cherry") == 3, "Ошибка поиска cherry"
assert ht.search("unknown") is None, "Ошибка поиска неизвестного ключа"
print("✓ Тест вставки и поиска пройден")

ht.insert("apple", 10)
assert ht.search("apple") == 10, "Ошибка обновления значения"
print("✓ Тест обновления значения пройден")

assert ht.delete("banana") == True, "Ошибка удаления существующего ключа"
assert ht.search("banana") is None, "Ошибка: ключ не удален"
assert ht.delete("unknown") == False, "Ошибка удаления несуществующего ключа"
print("✓ Тест удаления пройден")

ht2 = HashTableOpenAddressing(3)  
ht2.insert("key1", "value1")
ht2.insert("key2", "value2")
ht2.insert("key3", "value3")

assert ht2.search("key1") == "value1", "Ошибка при коллизии"
assert ht2.search("key2") == "value2", "Ошибка при коллизии"
assert ht2.search("key3") == "value3", "Ошибка при коллизии"
print("✓ Тест коллизий пройден")

print("Все тесты HashTableOpenAddressing пройдены успешно!\n")
```

## Задание 4

```python
def array_intersection_custom(arr1, arr2):
    """Проверка пересечения массивов через нашу хеш-таблицу"""
    ht = HashTableChaining(len(arr1))
    
    for item in arr1:
        ht.insert(item, True)  
    
    for item in arr2:
        if ht.search(item) is not None:  
            return True
    
    return False

print("=== Пересечение через HashTableChaining ===")
arr1 = [1, 2, 3, 4, 5]
arr2 = [4, 5, 6, 7, 8]
result = array_intersection_custom(arr1, arr2)
print(f"Массивы {arr1} и {arr2} пересекаются: {result}")
```

## Здание 5

```python
def has_unique_elements(arr):
    """Проверка уникальности"""
    ht = HashTableOpenAddressing(len(arr))
    
    for item in arr:
        if ht.search(item) is not None:
            return False
        ht.insert(item, True)
    
    return True


print("\n=== Уникальность через HashTableOpenAddressing ===")
arr = [1, 2, 3, 2, 4, 1]
arr2 = [1, 3, 4, 6]
print(f"Массив {arr} уникален: {has_unique_elements(arr)}")
print(f"Массив {arr2} уникален: {has_unique_elements(arr2)}")
```

## Задание 6

```python
def find_pairs_with_sum(arr, target_sum):
    """Поиск пар с заданной суммой"""
    ht = HashTableChaining(len(arr))
    pairs = []
    
    for num in arr:
        complement = target_sum - num
        
        if ht.search(complement) is not None:
            pairs.append((complement, num))
        
        ht.insert(num, True)
    
    return pairs

print("\n=== Пары с суммой через HashTableChaining ===")
arr = [1, 4, 2, 3, 5, 6, 7]
target = 7
pairs = find_pairs_with_sum(arr, target)
print(f"Пары с суммой {target} в {arr}: {pairs}")
```

## Задание 7

```python
def are_anagrams_custom(str1, str2):
    """Проверка анаграмм через нашу хеш-таблицу"""
    if len(str1) != len(str2):
        return False
    
    ht = HashTableOpenAddressing(26)  
    
    for char in str1:
        current_count = ht.search(char)
        if current_count is None:
            ht.insert(char, 1)
        else:
            ht.insert(char, current_count + 1)
    
    for char in str2:
        current_count = ht.search(char)
        if current_count is None or current_count == 0:
            return False
        ht.insert(char, current_count - 1)
    
    return True

print("\n=== Анаграммы через HashTableOpenAddressing ===")
str1 = "listen"
str2 = "silent"
print(f"'{str1}' и '{str2}' - анаграммы: {are_anagrams_custom(str1, str2)}")
```

## Задание 2

```python
import hashlib
import time
import json

class Block:
    def __init__(self, data, previous_hash=""):
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Вычисляет хеш блока на основе его данных"""
        import hashlib
        data_string = f"{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def __str__(self):
        return f"Данные: {self.data}\nХеш: {self.hash[:20]}...\nПредыдущий: {self.previous_hash[:20]}...\n"

class BlockchainWithCustomHashTable:
    def __init__(self):
        self.chain = HashTableChaining(10)
        self.current_hash = None
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Создает генезис-блок используя нашу хеш-таблицу"""
        genesis_data = "Genesis Block"
        genesis_hash = self._calculate_hash(genesis_data, "0")
        self.chain.insert(genesis_hash, Block(genesis_data, "0"))
        self.current_hash = genesis_hash
        print("✓ Создан генезис-блок (в нашей хеш-таблице)")
    
    def _calculate_hash(self, data, previous_hash):
        """Вычисляет хеш для блока"""
        import hashlib
        data_string = f"{data}{previous_hash}"
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def add_block(self, data):
        """Добавляет блок используя нашу хеш-таблицу"""
        previous_hash = self.current_hash
        new_hash = self._calculate_hash(data, previous_hash)
        
        new_block = Block(data, previous_hash)
        self.chain.insert(new_hash, new_block)
        self.current_hash = new_hash
        
        print(f"✓ Добавлен блок: {data}")
        return new_hash
    
    def is_chain_valid(self):
        """Проверяет целостность через нашу хеш-таблицу"""
        current = self.current_hash
        
        while current:
            block = self.chain.search(current)
            if not block:
                return False
            
            previous_hash = block.previous_hash
            
            if previous_hash == "0":
                return True
            
            if block.calculate_hash() != current:
                return False
            
            current = previous_hash
        
        return False

def test_custom_blockchain():
    print("\n" + "="*60)
    print("БЛОКЧЕЙН С НАШЕЙ HASHTableChaining")
    print("="*60)
    
    blockchain = BlockchainWithCustomHashTable()
    blockchain.add_block("Транзакция 1: Alice -> Bob")
    blockchain.add_block("Транзакция 2: Bob -> Carol")
    
    print(f"✓ Цепочка валидна: {blockchain.is_chain_valid()}")

test_custom_blockchain()
```

```python

```
