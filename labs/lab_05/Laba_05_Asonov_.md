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

# Хеш-функции и хеш-таблицы


## Цель работы


Изучение хеш-функций и хеш-таблиц, а также основных операций над ними.


### Задание 1( Хеш-таблица на основе метода цепочек)


#### Хеш-таблица 
— это структура данных, предназначенная для реализации ассоциативного массива (отображения ключей в значения). Она позволяет выполнять операции добавления, удаления и поиска элементов в среднем за O(1) время.

#### Основные компоненты:

 Ключ — уникальный идентификатор, по которому происходит поиск данных.
 Значение — данные, связанные с ключом.
Хеш-функция — функция, преобразующая ключ в индекс (хеш-код) для размещения в таблице.
Массив бакетов — массив, где хранятся элементы. Каждая ячейка массива называется бакетом (bucket) или слотом.
Коэффициент нагрузки (load factor) — отношение количества элементов в таблице к размеру массива (n / size). Важный параметр для эффективности.
#### Хеш-функции
Хеш-функция — это функция, которая преобразует ключ произвольного размера и типа в целое число (индекс) фиксированного диапазона [0, size-1].

#### Требования к хорошей хеш-функции:

Детерминированность: Один и тот же ключ всегда должен давать один и тот же хеш-код.

Равномерное распределение: Ключи должны равномерно распределяться по всем индексам таблицы для минимизации коллизий.

Вычислительная эффективность: Функция должна быстро вычисляться.

#### Распространенные методы вычисления хеш-кодов:

Для целых чисел: часто используют взятие по модулю размера таблицы: hash(key) = key % size.

Для строк: популярна полиномиальная хеш-функция (например, метод Горнера), чтобы учесть значение каждого символа.

```python
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * capacity
    
    def _hash(self, key):
        return hash(key) % self.capacity 
    
    def put(self, key, value):
        index = self._hash(key)  
        node = self.buckets[index]
        
        if node is None:
            self.buckets[index] = Node(key, value)
            self.size += 1
            return
        
        prev = None
        while node is not None:
            if node.key == key:
                node.value = value
                return
            prev = node
            node = node.next
        
        prev.next = Node(key, value)
        self.size += 1
    
    def get(self, key):
        """Возвращает значение по ключу или None если ключ не найден"""
        index = self._hash(key)
        node = self.buckets[index]
        
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        
        return None
    
    def remove(self, key):
        index = self._hash(key)
        node = self.buckets[index]
        prev = None
        
        while node is not None:
            if node.key == key:
                if prev is None:
                    self.buckets[index] = node.next
                else:
                    prev.next = node.next
                self.size -= 1
                return True
            prev = node
            node = node.next
        
        return False
    
    def __len__(self):
        return self.size
    
    def __contains__(self, key):
        return self.get(key) is not None
    
    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(f"Key '{key}' not found")
        return value
    
    def __setitem__(self, key, value):
        self.put(key, value)



def test_basic():
    ht = HashTable()
    ht.put("apple", 5)
    ht.put("banana", 10)
    
    assert ht.get("apple") == 5
    assert ht.get("banana") == 10
    assert ht.get("orange") is None
    assert len(ht) == 2
    print(" Базовая функциональность работает")


def test_update():
    ht = HashTable()
    ht.put("apple", 5)
    ht.put("apple", 15) 
    
    assert ht.get("apple") == 15
    assert len(ht) == 1
    print(" Обновление значений работает")


def test_remove():
    ht = HashTable()
    ht.put("apple", 5)
    ht.put("banana", 10)
    
    assert ht.remove("apple") == True
    assert ht.remove("apple") == False
    assert ht.get("apple") is None
    assert len(ht) == 1
    print(" Удаление элементов работает")


def test_operators():
    ht = HashTable()
    ht["apple"] = 5
    ht["banana"] = 10
    
    assert ht["apple"] == 5
    assert "apple" in ht
    assert "orange" not in ht
    print(" Python операторы работают")


def test_collisions():
    ht = HashTable(2)  
    ht.put("a", 1)
    ht.put("b", 2)
    ht.put("c", 3)
    
    assert ht.get("a") == 1
    assert ht.get("b") == 2
    assert ht.get("c") == 3
    assert len(ht) == 3
    print(" Обработка коллизий работает")


if __name__ == "__main__":
    test_basic()
    test_update()
    test_remove()
    test_operators()
    test_collisions()
    print("\n Все тесты пройдены!")
```

#### Метод цепочек (Separate Chaining)

- self.buckets = [None] * capacity
- buckets: [None, None, None, None, None, None, None, None, None, None]

- % self.capacity - берем остаток от деления на capacity для попадания в диапазон [0, capacity-1]

#### Специальные методы Python

def __len__(self):
    return self.size  # Поддержка len(hashtable)

def __contains__(self, key):
    return self.get(key) is not None  # Поддержка 'key in hashtable'

def __getitem__(self, key):
    value = self.get(key)
    if value is None:
        raise KeyError(f"Key '{key}' not found")
    return value  # Поддержка hashtable[key]

def __setitem__(self, key, value):
    self.put(key, value)  # Поддержка hashtable[key] = value

Каждый бакет представляет собой связный список (или другую структуру), в котором хранятся все элементы с одинаковым хеш-кодом.

Операции:

Вставка: Вычисляется индекс. Элемент добавляется в начало или конец списка в данном бакете.

Поиск: Вычисляется индекс. Производится линейный поиск по списку в бакете по ключу.

Удаление: Аналогично поиску, после нахождения элемент удаляется из списка.

Преимущества: Простота реализации, эффективен при высокой нагрузке.

Недостатки: Требует дополнительной памяти на хранение указателей.


### Задание 2 (Хеш-таблица на основе открытой адресации)

```python
class HashTableOpenAddressing:    
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size
        self.count = 0
        self.load_factor_threshold = 0.7 
        self.DELETED = object() #DELETED = object() - специальный маркер, который отличает удаленные элементы от пустых ячеек
    
    def _hash(self, key):
        if isinstance(key, int):
            return key % self.size
        elif isinstance(key, str): #полиномиальный хеш (31 - простое число для уменьшения коллизий)
            hash_value = 0
            for char in key:
                hash_value = (hash_value * 31 + ord(char)) % self.size # hash = (97*31 + 98) % size = (3007 + 98) % size
            return hash_value 
        else:
            return hash(key) % self.size
    
    def _probe(self, key, i):
        return (self._hash(key) + i) % self.size
    
    def _resize(self):
        if self.count / self.size > self.load_factor_threshold:
            old_table = self.table
            old_size = self.size
            self.size = self.size * 2
            self.table = [None] * self.size
            self.count = 0
            for item in old_table:
                if item and item != self.DELETED:
                    self.put(item[0], item[1])
    
    def put(self, key, value):
        self._resize()
        for i in range(self.size):
            index = self._probe(key, i)
            if self.table[index] is None or self.table[index] == self.DELETED:
                self.table[index] = (key, value)
                self.count += 1
                return
            elif self.table[index][0] == key:
                self.table[index] = (key, value)
                return
        raise Exception("Hash table is full")
    
    def get(self, key):
        for i in range(self.size):
            index = self._probe(key, i)
            if self.table[index] is None:
                break
            elif self.table[index] != self.DELETED and self.table[index][0] == key:
                return self.table[index][1]
        raise KeyError(f"Key {key} not found")
    
    def delete(self, key):
        for i in range(self.size):
            index = self._probe(key, i)
            if self.table[index] is None:
                break
            elif self.table[index] != self.DELETED and self.table[index][0] == key:
                self.table[index] = self.DELETED #Если бы ставили None, то цепочка пробирования прервалась бы и последующие элементы стали бы недоступны
                self.count -= 1
                return True
        raise KeyError(f"Key {key} not found")
    
    def contains(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False
    
    def __str__(self):
        result = []
        for i, item in enumerate(self.table):
            if item is None:
                result.append(f"Bucket {i}: None")
            elif item == self.DELETED:
                result.append(f"Bucket {i}: DELETED")
            else:
                result.append(f"Bucket {i}: ({item[0]}: {item[1]})")
        return "\n".join(result)



def test_basic_operations():
    ht = HashTableOpenAddressing()
    ht.put("apple", 5)
    ht.put("banana", 10)
    
    assert ht.get("apple") == 5
    assert ht.get("banana") == 10
    assert ht.count == 2
    print("Базовая функциональность работает")


def test_update_values():
    ht = HashTableOpenAddressing()
    ht.put("apple", 5)
    ht.put("apple", 15)  
    
    assert ht.get("apple") == 15
    assert ht.count == 1  
    print(" Обновление значений работает")


def test_deletion():
    ht = HashTableOpenAddressing()
    ht.put("apple", 5)
    ht.put("banana", 10)
    
    assert ht.delete("apple") == True
    assert ht.count == 1
    try:
        ht.get("apple")
        assert False, "Должно было возникнуть KeyError"
    except KeyError:
        pass
    
    assert ht.contains("banana") == True
    assert ht.contains("apple") == False
    print(" Удаление элементов работает")


def test_collisions():
    ht = HashTableOpenAddressing(5) 
    ht.put("a", 1)
    ht.put("b", 2)
    ht.put("c", 3)
    ht.put("d", 4)
    
    assert ht.get("a") == 1
    assert ht.get("b") == 2
    assert ht.get("c") == 3
    assert ht.get("d") == 4
    assert ht.count == 4
    
    
    ht.delete("b")
    assert ht.contains("b") == False
    ht.put("e", 5)
    assert ht.get("e") == 5
    print(" Обработка коллизий работает")



if __name__ == "__main__":
    test_basic_operations()
    test_update_values()
    test_deletion()
    test_collisions()
    
    print("\n Все тесты хеш-таблицы с открытой адресацией пройдены!")
```

#### Метод открытой адресации (Open Addressing)

self.DELETED = object()  # Уникальный объект

Преимущества:

- Уникальность: object() создает абсолютно уникальный объект

 - Безопасность: невозможно случайно совпадение с пользовательскими данными

 - Производительность: быстрая проверка is или ==

Все элементы хранятся непосредственно в массиве. При коллизии элемент помещается в другую свободную ячейку согласно выбранной стратегии.

 ###### DELETED решает фундаментальную проблему открытой адресации:

 - Сохраняет целостность цепочек пробирования

- Позволяет повторно использовать ячейки

- Обеспечивает корректный поиск после удалений

Просто реализуется и эффективно работает
#### Стратегии поиска свободной ячейки:

Линейное пробирование: index = (hash(key) + i) % size, где i = 0, 1, 2, ...

Квадратичное пробирование: index = (hash(key) + i²) % size

Двойное хеширование: index = (hash1(key) + i * hash2(key)) % size

##### Преимущества: 
Не требует дополнительной памяти для указателей, лучше использует кэш процессора.

##### Недостатки:
Более сложное удаление элементов, может возникнуть "кластеризация" (скопление элементов), сильная зависимость от коэффициента нагрузки.


### Задание 3(Блокчейн)

<!-- #region -->
1. Создание строки блока
python
block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
Объединяет все важные данные блока в одну строку:

self.index - номер блока в цепочке

self.timestamp - время создания блока

self.data - содержимое блока (транзакции, информация)

self.previous_hash - хеш предыдущего блока

2. Кодирование в байты
python
block_string.encode()
Преобразует строку в байты, так как хеш-функции работают с бинарными данными.

3. Вычисление хеша SHA-256
python
hashlib.sha256(block_string.encode())
Применяет криптографическую функцию SHA-256 к данным.

4. Получение шестнадцатеричного представления
python
.hexdigest()
Преобразует бинарный хеш в читаемую строку из 64 шестнадцатеричных символов.


##### Генезис-блок - особый первый блок:

index=0 - начало цепочки

data="Genesis Block" - специальная метка

previous_hash="0" - ссылка на "ничто"

timestamp - время создания блокчейна
<!-- #endregion -->

```python
import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index           
        self.timestamp = timestamp   # Время создания блока
        self.data = data            
        self.previous_hash = previous_hash  
        self.hash = self.calculate_hash()   
        
    def calculate_hash(self): 
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}" # Создаем строку из всех значимых данных блока
        return hashlib.sha256(block_string.encode()).hexdigest()  
    
    def __str__(self):
        return f"Block {self.index} [Hash: {self.hash}, Previous: {self.previous_hash}, Data: {self.data}]"

class Blockchain:    
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    """  генезис-блок (первый блок) с индексом 0"""
    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")
    
    def add_block(self, data):
        """ Получаем последний блок в цепочке"""
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)): # Проверяем все блоки, начиная с первого после генезиса
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash(): # Проверка 1: Не изменились ли данные текущего блока?
                return False
            if current_block.previous_hash != previous_block.hash:  # Проверка 2: Корректная ссылка на предыдущий блок?
                return False
        return True
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def get_chain_length(self):
        return len(self.chain)
    
    def __str__(self):
        return "\n".join(str(block) for block in self.chain)



def test_genesis_block():
    blockchain = Blockchain()
    
    assert len(blockchain.chain) == 1
    assert blockchain.chain[0].index == 0
    assert blockchain.chain[0].data == "Genesis Block"
    assert blockchain.chain[0].previous_hash == "0"
    assert blockchain.chain[0].hash == blockchain.chain[0].calculate_hash()
    print("✓ Генезис-блок создан корректно")


def test_adding_blocks():
    blockchain = Blockchain()
    
    blockchain.add_block("Transaction 1")
    blockchain.add_block("Transaction 2")
    
    assert len(blockchain.chain) == 3
    assert blockchain.chain[1].data == "Transaction 1"
    assert blockchain.chain[2].data == "Transaction 2"
    assert blockchain.chain[1].index == 1
    assert blockchain.chain[2].index == 2
    print(" Добавление блоков работает")


def test_block_linking():
    blockchain = Blockchain()
    
    blockchain.add_block("Data 1")
    blockchain.add_block("Data 2")
    
    
    assert blockchain.chain[1].previous_hash == blockchain.chain[0].hash
    assert blockchain.chain[2].previous_hash == blockchain.chain[1].hash
    print(" Связи между блоками корректны")


def test_chain_validation():
    blockchain = Blockchain()
    
    blockchain.add_block("Valid Data 1")
    blockchain.add_block("Valid Data 2")
    
    
    assert blockchain.is_chain_valid() == True
    
   
    blockchain.chain[1].data = "Tampered Data"
    
    
    assert blockchain.is_chain_valid() == False
    print(" Валидация цепочки работает")


def test_data_integrity():
    blockchain = Blockchain()
    
    original_data = "Original Data"
    blockchain.add_block(original_data)
    
    original_hash = blockchain.chain[1].hash
    
   
    assert blockchain.chain[1].calculate_hash() == original_hash
    
   
    blockchain.chain[1].data = "Modified Data"
    assert blockchain.chain[1].calculate_hash() != original_hash
    print(" Целостность данных и хеширование работают")


if __name__ == "__main__":
    test_genesis_block()
    test_adding_blocks()
    test_block_linking()
    test_chain_validation()
    test_data_integrity()
    print("\n Все тесты блокчейна пройдены!")
```

### Задание 4(Проверка пересечения двух массивов)

```python
def has_intersection(arr1, arr2):
    
    hash_set = set(arr1) #Создаем множество(O(n) - для хранения множества)
    for item in arr2:
        if item in hash_set:
            return True
    return False



def test_has_intersection():
   
    arr1 = [1, 2, 3, 4, 5]
    arr2 = [5, 6, 7, 8, 9]
    assert has_intersection(arr1, arr2) == True
    print(" Тест 1: Есть пересечение - пройден")
    
   
    arr1 = [1, 2, 3, 4]
    arr2 = [5, 6, 7, 8]
    assert has_intersection(arr1, arr2) == False
    print(" Тест 2: Нет пересечения - пройден")
    
    arr1 = []
    arr2 = [1, 2, 3]
    assert has_intersection(arr1, arr2) == False
    
    arr1 = [1, 2, 3]
    arr2 = []
    assert has_intersection(arr1, arr2) == False
    
    arr1 = []
    arr2 = []
    assert has_intersection(arr1, arr2) == False
    print(" Тест 3: Пустые массивы - пройден")
    
    arr1 = [1, 2, 3, 4, 5]
    arr2 = [3, 4, 5, 6, 7]
    assert has_intersection(arr1, arr2) == True
    print(" Тест 4: Множественные пересечения - пройден")
    
    arr1 = ["apple", "banana", "orange"]
    arr2 = ["banana", "grape", "kiwi"]
    assert has_intersection(arr1, arr2) == True
    
    arr1 = [1.5, 2.7, 3.1]
    arr2 = [3.1, 4.2, 5.8]
    assert has_intersection(arr1, arr2) == True
    print(" Тест 5: Разные типы данных - пройден")

if __name__ == "__main__":
    test_has_intersection()
   
    print("\n Все тесты пройдены успешно!")
```

### Задание 5 (Проверка уникальности элементов в массиве)

```python
def has_unique_elements(arr):
    
    hash_set = set() # Пустое множество
    for item in arr:
        if item in hash_set:
            return False
        hash_set.add(item)
    return True


def test_has_unique_elements():
    
   
    arr = [1, 2, 3, 4, 5]
    assert has_unique_elements(arr) == True
    print(" Тест 1: Все элементы уникальны - пройден")
    
    
    arr = [1, 2, 3, 2, 4]
    assert has_unique_elements(arr) == False
    print(" Тест 2: Есть дубликаты - пройден")
    
    
    arr = []
    assert has_unique_elements(arr) == True
    print(" Тест 3: Пустой массив - пройден")
    
    
    arr = [42]
    assert has_unique_elements(arr) == True
    print(" Тест 4: Один элемент - пройден")
    
    
    arr = ["apple", "banana", "orange"]
    assert has_unique_elements(arr) == True
    
    arr = ["apple", "banana", "apple"]
    assert has_unique_elements(arr) == False
    
    arr = [1, "1", 2, "2"]  #
    assert has_unique_elements(arr) == True
    print(" Тест 5: Разные типы данных - пройден")


if __name__ == "__main__":
    test_has_unique_elements()
    print("\n Все тесты пройдены успешно!")
```

### Задание 6 (Нахождение пар с заданной суммой)

```python
def find_pairs_with_sum(arr, target_sum):
    result = []
    seen = set() # Множество для отслеживания просмотренных чисел
    for num in arr:
        complement = target_sum - num
        if complement in seen:
            result.append((complement, num))
        seen.add(num) #l обавляет новый элемент в множество, автоматически игнорируя дубликаты
    return result

def test_find_pairs_with_sum():
    """Тестирование функции find_pairs_with_sum"""
    arr = [2, 7, 11, 15, 3, 6]
    target = 9
    result = find_pairs_with_sum(arr, target) 
    
    
    assert (2, 7) in result
    assert (3, 6) in result
    assert len(result) == 2
    print(" Тест пройден: найдены пары (2,7) и (3,6)")

if __name__ == "__main__":
    test_find_pairs_with_sum()
    print(" Тест пройден успешно!")
```

### Задание 7(Задача на проверку анаграмм)

```python
def are_anagrams(str1, str2):
    if len(str1) != len(str2):
        return False
    char_count = {} #Создание словаря для подсчета символов
    for char in str1:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    for char in str2:
        if char not in char_count or char_count[char] == 0:
            return False
        char_count[char] -= 1
    return True


def test_are_anagrams():
    """Тестирование функции are_anagrams"""
    str1 = "listen"
    str2 = "silent"
    result = are_anagrams(str1, str2)
    
    assert result == True
    print(" Тест пройден: 'listen' и 'silent' являются анаграммами")

if __name__ == "__main__":
    test_are_anagrams()
    print(" Тест пройден успешно!")
```

1. Определение хеш-таблицы и основная задача

Хеш-таблица — это структура данных, которая реализует абстрактный тип данных "ассоциативный массив" (или "словарь"). Она хранит пары "ключ-значение".

Основная задача, которую она решает — это обеспечение быстрого доступа к данным по ключу. В среднем случае, время выполнения операций (вставка, поиск, удаление) составляет O(1).

---

2. Хеш-функция и ее роль

Хеш-функция — это детерминированная функция, которая преобразует произвольный ключ (например, строку, число, объект) в число фиксированной длины (хеш-код), которое затем используется как индекс в массиве (хеш-таблице).

Роль в работе хеш-таблицы: Хеш-функция равномерно распределяет ключи по ячейкам (бакетам) таблицы. Это позволяет по ключу за время O(1) вычислить позицию, где должно храниться или где следует искать соответствующее значение.

---

3. Ключевые свойства хорошей хеш-функции

1. Детерминированность: Один и тот же ключ всегда должен давать один и тот же хеш-код.
2. Равномерное распределение: Хеш-функция должна распределять ключи по всем возможным индексам максимально равномерно. Это минимизирует количество коллизий.
3. Вычислительная эффективность: Вычисление хеш-кода должно быть быстрым (желательно O(1) или O(длина ключа)).
4. Устойчивость к коллизиям (для криптографии): Для обычных хеш-таблиц это свойство менее критично, но в целом хорошая функция должна минимизировать вероятность коллизий для разных входных данных.

---

4. Коллизии и почему их нельзя избежать

Коллизия — это ситуация, когда две разные пары ключ-значение претендуют на одну и ту же ячейку хеш-таблицы, то есть h(key1) = h(key2).

Коллизии невозможно полностью избежать из-за принципа Дирихле (или "принципа ящиков"). Хеш-функция отображает потенциально бесконечное (или очень большое) множество возможных ключей на конечное множество индексов таблицы (например, 0..N-1). Следовательно, какие-то два разных ключа неизбежно попадут в одну ячейку.

---

5. Коэффициент нагрузки (Load Factor)

Коэффициент нагрузки (α) — это отношение количества элементов в таблице (n) к ее общему размеру (m): α = n / m.

Влияние на производительность:

· Низкий α (много свободного места): Коллизии маловероятны, операции выполняются быстро, близко к O(1).
· Высокий α (таблица заполнена): Вероятность коллизий резко возрастает. Для метода цепочек поиск в длинной цепочке замедляется до O(n). Для открытой адресации увеличивается длина последовательностей проб, что также замедляет все операции.
  Когда α превышает определенный порог (обычно 0.7-0.8), необходимо выполнять рехеширование.

---

6. Принцип работы метода цепочек (Separate Chaining)

Каждая ячейка хеш-таблицы является не самим элементом, а указателем на голову связного списка (или корень другого дерева). Все элементы, чьи ключи дали один и тот же хеш (коллизия), просто добавляются в этот список.

· Вставка: Вычисляем индекс, добавляем элемент в начало/конец списка в этой ячейке. O(1).
· Поиск: Вычисляем индекс, ищем элемент в соответствующем списке. O(длина списка).
· Удаление: Вычисляем индекс, удаляем элемент из списка. O(длина списка).

---

7. Принцип работы метода открытой адресации (Open Addressing)

При использовании этого метода все элементы хранятся непосредственно в самом массиве хеш-таблицы. При возникновении коллизии алгоритм ищет следующую свободную ячейку внутри самой таблицы по определенному алгоритму (пробингу).

Принципиальное отличие от метода цепочек: В методе цепочек элементы с коллизиями хранятся вне основного массива (в цепочках), а в открытой адресации разрешение коллизий происходит внутри самого массива.

---

8. Линейное, квадратичное пробирование и двойное хеширование

· Линейное пробирование: Поиск следующей ячейки идет с фиксированным шагом (обычно 1). index = (h(key) + i) % m, где i = 0, 1, 2, ...
  · Проблема: Возникает первичная кластеризация — длинные последовательности занятых ячеек, которые замедляют все операции.
· Квадратичное пробирование: Шаг поиска зависит от номера попытки квадратично.
index = (h(key) + c₁*i + c₂*i²) % m.
  · Решает проблему первичной кластеризации, но может возникнуть вторичная кластеризация (элементы с одинаковым начальным хешем имеют одинаковую последовательность проб).
  · Проблема: Не гарантирует, что будут проверены все ячейки.
· Двойное хеширование: Для определения шага используется вторая хеш-функция. index = (h₁(key) + i * h₂(key)) % m.
  · Наиболее эффективен, так как использует две независимые хеш-функции. Это приводит к самому равномерному распределению проб и минимизирует кластеризацию. Разные ключи имеют разные последовательности проб.

---

9. Преимущества и недостатки метода цепочек vs открытой адресации

Метод цепочек Открытая адресация
+ Проще в реализации + Лучшая локальность ссылок (все данные в одном массиве), может быть быстрее из-за кеша процессора
+ Устойчив к высоким коэффициентам нагрузки (α > 1 возможен) - Сильнее страдает от высокой нагрузки, требует большей таблицы
+ Удаление тривиально - Удаление сложнее (требует пометки "удален")
- Требует дополнительной памяти на указатели - Не требует дополнительной памяти
- Хуже локальность ссылок (узлы списка разбросаны в памяти) - Высокая вероятность кластеризации (кроме двойного хеширования)

---

10. Проблема удаления в открытой адресации

Простое удаление (например, установка ячейки в "пусто") нарушает целостность, потому что при поиске мы идем по последовательности проб, пока не встретим пустую ячейку. Если мы удалим элемент из середины такой последовательности, последующие элементы станут недоступными.

Правильная реализация: При удалении ячейка помечается специальным флагом "удален" (tombstone). При вставке в такую ячейку можно помещать новый элемент. При поиске мы просто "перепрыгиваем" через такие ячейки, продолжая пробинг.

---

11. Сложность O(1) в среднем случае

Предполагая, что хеш-функция равномерна и коэффициент нагрузки α является константой, длина цепочек (для метода цепочек) и длина последовательностей проб (для открытой адресации) также будет константной. Поэтому для доступа к нужной ячейке или для проверки константного числа ячеек требуется O(1) времени.

---

12. Худший случай для хеш-таблицы

Худший случай — когда все ключи попадают в одну и ту же ячейку.

· Для метода цепочек: Все элементы оказываются в одном связном списке. Таблица вырождается в список со сложностью операций O(n).
· Для открытой адресации: Длина последовательности проб становится равна n, сложность операций также O(n).

Условия возникновения:

1. Плохая хеш-функция, которая не распределяет ключи равномерно.
2. Злонамеренно подобранные ключи (атака на хеш-таблицу), если хеш-функция известна и не является криптостойкой.

---

13. Рехеширование (Rehashing)

Рехеширование — это процесс создания новой хеш-таблицы большего размера и пересчета хешей для всех существующих элементов с последующим их перемещением в новую таблицу.

Для чего необходимо: Чтобы уменьшить коэффициент нагрузки и, как следствие, снизить вероятность коллизий и поддерживать высокую производительность операций.

---

14. Момент для выполнения рехеширования

Момент обычно выбирается на основе коэффициента нагрузки α.

· Для метода цепочек порог может быть выше (например, α = 0.75 - 1.0).
· Для открытой адресации порог ниже (например, α = 0.6 - 0.75), так как она сильнее страдает от заполнения.

Когда α превышает заданный порог, инициируется рехеширование.

---

15. Процесс рехеширования

 Создается новая хеш-таблица, размер которой обычно в 1.5-2 раза больше предыдущего. Желательно, чтобы новый размер был простым числом.
 Для каждого элемента из старой таблицы:
   · Вычисляется новый хеш-код с использованием новой функции (или той же, но с новым размером таблицы).
   · Элемент вставляется в новую таблицу.
Старая таблица освобождается из памяти.
Дальнейшие операции выполняются с новой таблицей.

---

16. Структура данных для бакетов в методе цепочек

Наиболее удобна связный список (linked list).

Обоснование:

· Динамический размер: Списки идеально подходят для хранения динамически изменяющегося количества элементов в бакете.
· Простота вставки/удаления: Вставка и удаление из односвязного списка выполняются за O(1), если есть указатель на предыдущий элемент (или используется двусвязный список).
· Эффективность по памяти: Требуют только дополнительной памяти на указатели.

Альтернатива: Если бакеты становятся очень длинными из-за плохой хеш-функции или атаки, их можно заменить на сбалансированные двоичные деревья поиска (например, красно-черные). Это гарантирует O(log n) время поиска даже в худшем случае. Именно так реализовано в java.util.HashMap начиная с JDK 8.

---

17. Формула для вычисления индекса

index = hash(key) % table_size

Операция взятия по модулю гарантирует, что полученный индекс будет находиться в диапазоне [0, table_size - 1].

---

18. Размер таблицы — простое число

Использование простого числа в качестве размера таблицы помогает уменьшить количество коллизий, особенно если хеш-функция неидеальна.

Причина: Многие ключи в реальных задачах имеют скрытые закономерности (например, все четные). Если размер таблицы (m) и шаги в хеш-функции имеют общие делители, то многие ячейки могут никогда не быть использованы, что усиливает кластеризацию. Простое число m минимизирует количество общих делителей, способствуя более равномерному распределению.

---

19. Хеш-функция для строки

Одна из самых распространенных и эффективных — полиномиальное хеширование.

Формула: hash = (s[0] * p^(n-1) + s[1] * p^(n-2) + ... + s[n-1] * p^0) % m

Где:

· s[i] — код i-го символа строки.
· p — простое число (например, 31 или 37).
· n — длина строки.
· m — размер хеш-таблицы (модуль).

Пример для строки "hi":
h = ('h' * 31 + 'i') % m

Чтобы избежать переполнения и работать с большими числами, на каждом шаге лучше брать по модулю:
def hash_string(s, table_size):
    h = 0
    p = 31
    for char in s:
        h = (h * p + ord(char)) % table_size
    return h

---

20. Проблемы неравномерного распределения хеш-функции

· Резкое падение производительности: Возрастает количество коллизий, операции из O(1) вырождаются в O(n).
· Кластеризация: Элементы скапливаются в определенных областях таблицы, что особенно губительно для открытой адресации.
· Уязвимость к DoS-атакам: Злоумышленник может подобрать данные, которые все попадут в один бакет, и "положить" сервер, использующий хеш-таблицу.

---

21. Когда использовать цепочки, а когда открытую адресацию?

Метод цепочек предпочтительнее, когда:

· Неизвестно заранее количество элементов.
· Требуется стабильная производительность даже при высокой нагрузке.
· Нужна простая и надежная реализация удаления.

Открытая адресация предпочтительнее, когда:

· Важна производительность на современных процессорах (лучшая локальность кеша).
· Известен примерный размер данных, и можно выделить таблицу с запасом.
· Жесткие ограничения по памяти (не тратится на указатели).

---

22. Примеры реальных задач для хеш-таблиц

- Словарь или кеш: Быстрый поиск определения по слову или кешированного результата по запросу.
- Удаление дубликатов: Можно за O(n) найти и удалить все дубликаты в массиве, просто добавляя элементы в хеш-таблицу.
-  Подсчет частоты элементов: Ключ — элемент, значение — счетчик. За один проход по массиву можно построить частотный словарь.

---

23. Сравнение с сбалансированным деревом поиска

Хеш-таблица Сбалансированное дерево (например, красно-черное)
В среднем O(1) на операцию Гарантированно O(log n) на операцию
Нет упорядоченности данных Данные упорядочены (можно обходить по порядку)
Производительность сильно зависит от хеш-функции Производительность стабильна и предсказуема
Может быть уязвима к атакам Устойчива к патологическим наборам данных
Обычно использует меньше памяти на элемент Использует больше памяти на указатели

---

24. Хранение одинаковых ключей

Да, может. Это реализуется двумя основными способами:

1. Хранение списка значений: Каждому ключу соответствует не одно значение, а список (или другая коллекция) всех значений, вставленных с этим ключом.
2. Подсчет (для мультимножеств): Значением является счетчик. При вставке существующего ключа счетчик увеличивается.

---

25.Построение хеш-таблицы для ключей

Дано: h(key) = key % 7, ключи: 12, 5, 19, 7, 26, 14, 33

а) Метод цепочек:

- 12 % 7 = 5
- 5 % 7 = 5 -> коллизия с 12
- 19 % 7 = 5 -> коллизия с 12 и 5
- 7 % 7 = 0
- 26 % 7 = 5 -> коллизия
- 14 % 7 = 0 -> коллизия с 7
- 33 % 7 = 5 -> коллизия

Таблица (индексы 0-6):
- 0: [7] -> [14]
- 1: []
- 2: []
- 3: []
- 4: []
- 5: [12] -> [5] -> [19] -> [26] -> [33]
- 6: []

б) Линейное пробирование (шаг +1):

- 12 -> 5
- 5 -> 5 (занято) -> 6
- 19 -> 5 (занято) -> 6 (занято) -> 0
- 7 -> 0 (занято) -> 1
- 26 -> 5 (занято) -> 6 (занято) -> 0 (занято) -> 1 (занято) -> 2
- 14 -> 0 (занято) -> 1 (занято) -> 2 (занято) -> 3
- 33 -> 5 (занято) -> 6 (занято) -> 0 (занято) -> 1 (занято) -> 2 (занято) -> 3 (занято) -> 4

Таблица:
- 0: 19
- 1: 7
- 2: 26
- 3: 14
- 4: 33
- 5: 12
- 6: 5

в) Квадратичное пробирование (index = (h(key) + i²) % 7):

- 12 -> 5
- 5 -> 5 (занято, i=1) -> (5+1)%7=6
- 19 -> 5 (занято, i=1) -> (5+1)%7=6 (занято, i=2) -> (5+4)%7=2
-  7 -> 0
·-26 -> 5 (занято, i=1) -> 6 (занято, i=2) -> 2 (занято, i=3) -> (5+9)%7=0 (занято, i=4) -> (5+16)%7=0 (занято, i=5) -> (5+25)%7=2 (занято, i=6) -> (5+36)%7=6 (занято).

Здесь видна проблема квадратичного пробирования — оно не всегда находит свободную ячейку, даже если она есть. На практике используют (h(key) + c1*i + c2*i²) и тщательно подбирают константы и размер таблицы.

---

26. Поиск двух чисел с суммой X

Алгоритм:

-  Создаем пустую хеш-таблицу (множество).
- Для каждого элемента num в массиве:
   · Вычисляем complement = X - num.
   · Проверяем, есть ли complement в хеш-таблице.
   · Если есть — мы нашли пару (num, complement).
   · Если нет — добавляем текущий num в хеш-таблицу.

Сложность: O(n), так как каждая операция с хеш-таблицей — O(1).

---

27. Поиск первого повторяющегося элемента

Алгоритм:

-  Создаем пустую хеш-таблицу (в качестве значения можно хранить индекс первого вхождения).
-  Проходим по массиву. Для каждого элемента:
   · Если его уже нет в таблице, добавляем его (и его индекс).
   · Если он уже есть в таблице — это и есть первый повторяющийся элемент.

---

28. Идеальное хеширование

Идеальное хеширование — это техника, которая позволяет построить хеш-функцию, не имеющую коллизий для заранее известного статического набора ключей.

Применение: Используется в случаях, когда набор ключей фиксирован и известен на этапе компиляции (например, ключевые слова в языке программирования), и требуется гарантировать константное время доступа даже в худшем случае.

Как работает: Часто используется двухуровневая схема. Хеш-функция первого уровня распределяет ключи по бакетам. Затем для каждого бакета, содержащего более одного ключа, подбирается своя собственная хеш-функция второго уровня, которая без коллизий размещает ключи этого бакета во вторичной таблице.

```python

```
