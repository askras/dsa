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
        self.load_factor_threshold = 0.7 # Порог для перехэширования
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

Все элементы хранятся непосредственно в массиве. При коллизии элемент помещается в другую свободную ячейку согласно выбранной стратегии.

#### Стратегии поиска свободной ячейки:

Линейное пробирование: index = (hash(key) + i) % size, где i = 0, 1, 2, ...

Квадратичное пробирование: index = (hash(key) + i²) % size

Двойное хеширование: index = (hash1(key) + i * hash2(key)) % size

##### Преимущества: 
Не требует дополнительной памяти для указателей, лучше использует кэш процессора.

##### Недостатки:
Более сложное удаление элементов, может возникнуть "кластеризация" (скопление элементов), сильная зависимость от коэффициента нагрузки.


### Задание 3(Блокчейн)


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

```python
import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index           # Порядковый номер блока
        self.timestamp = timestamp   # Время создания блока
        self.data = data             # Полезная нагрузка (транзакции, информация)
        self.previous_hash = previous_hash  # Хеш предыдущего блока
        self.hash = self.calculate_hash()   # Хеш текущего блока
        
    def calculate_hash(self): # Вычисление хеша
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}" #Создание строки блока
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def __str__(self):
        return f"Block {self.index} [Hash: {self.hash}, Previous: {self.previous_hash}, Data: {self.data}]"

class Blockchain:    
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")
    
    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
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
        seen.add(num)
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

```python
### Задание 7(Задача на проверку анаграмм)
```

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

1. Определение хеш-таблицы
Хеш-таблица - это структура данных, которая реализует ассоциативный массив (словарь), храня пары ключ-значение. Основная задача - обеспечить быстрый доступ к данным по ключу (в среднем O(1)).

2. Хеш-функция
Хеш-функция - это функция, которая преобразует ключ произвольного размера в целочисленный индекс фиксированного диапазона. Роль: равномерно распределять ключи по ячейкам таблицы.

3. Свойства хорошей хеш-функции
Детерминированность: одинаковые ключи → одинаковый хеш

Равномерность: равномерное распределение по всему диапазону

Быстрота вычисления: O(1) время вычисления

Устойчивость к коллизиям: минимизирует вероятность коллизий

4. Коллизии
Коллизия - ситуация, когда разные ключи имеют одинаковый хеш. Неизбежны из-за принципа Дирихле (pigeonhole principle): если ключей больше, чем ячеек, коллизии неизбежны.

5. Коэффициент нагрузки
Load factor = (количество элементов) / (размер таблицы).
Влияние: при высоком коэффициенте увеличивается вероятность коллизий и снижается производительность.

6. Метод цепочек
Каждая ячейка содержит ссылку на связный список элементов. При коллизии новый элемент добавляется в список.

7. Метод открытой адресации
Все элементы хранятся непосредственно в массиве. При коллизии ищется следующая свободная ячейка по определенному алгоритму.

8. Методы пробирования
Линейное: h(k, i) = (h(k) + i) % m

Квадратичное: h(k, i) = (h(k) + c₁i + c₂i²) % m

Двойное хеширование: h(k, i) = (h₁(k) + i·h₂(k)) % m

Наиболее эффективен двойное хеширование, так как оно уменьшает кластеризацию.

9. Преимущества и недостатки методов
Метод цепочек:

✓ Проще в реализации удаления

✓ Устойчив к высокому load factor

✗ Дополнительная память на указатели

Открытая адресация:

✓ Лучшая локальность ссылок

✓ Меньше выделений памяти

✗ Сложнее удаление, чувствителен к load factor

10. Проблема удаления в открытой адресации
Простое удаление нарушает цепочку пробирования. Решение: использовать специальные маркеры (DELETED), которые игнорируются при вставке, но учитываются при поиске.

11. Сложность O(1)
В среднем случае благодаря равномерному распределению и постоянному времени доступа к ячейкам по индексу.

12. Худший случай
Все ключи попадают в одну ячейку. Сложность деградирует до O(n). Возникает при плохой хеш-функции или атаке.

13-15. Рехеширование
Рехеширование - процесс увеличения размера таблицы и перераспределения элементов. Выполняется при достижении порогового load factor (обычно 0.7-0.8).

Процесс:

Создать новую таблицу большего размера

Перехешировать все элементы из старой таблицы

Заменить старую таблицу новой

16. Структура для бакетов
Связный список - прост в реализации, эффективен для небольших цепочек. Сбалансированное дерево - лучше для длинных цепочек.

17-18. Размер таблицы
Формула: index = hash(key) % table_size
Простой размер уменьшает кластеризацию при модульной операции.

19. Хеш-функция для строк

20. 
python
def hash_string(s, table_size):
    hash_val = 0
    for char in s:
        hash_val = (hash_val * 31 + ord(char)) % table_size
    return hash_val
    
22. Проблемы неравномерного распределения
Увеличивается количество коллизий

Снижается производительность

Возможна атака отказом в обслуживании

21. Выбор метода
Цепочки: когда неизвестно количество элементов, частые удаления
Открытая адресация: когда известен максимальный размер, важна производительность

22. Примеры применения
Кэширование (memcached, Redis)

Словари в Python, HashMap в Java

Базы данных (индексы)

23. Сравнение с деревьями
Хеш-таблица:

✓ Быстрее в среднем (O(1) vs O(log n))

✗ Нет упорядочивания, худший случай O(n)

Дерево:

✓ Гарантированная O(log n), упорядоченность

✗ Сложнее реализация, медленнее в среднем

24. Дубликаты ключей
Может, если значения хранятся в списке или используется мульти-хеш-таблица.

25. Построение таблицы
Ключи: 12, 5, 19, 7, 26, 14, 33
h(key) = key % 7

Метод цепочек:

text
0: 14 → 7
1: 33 → 26 → 19 → 12
2: 
3: 
4: 
5: 5
6: 

Линейное пробирование:

text
0: 14
1: 7
2: 33
3: 26
4: 19
5: 5
6: 12

26. Поиск двух чисел
python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
27. Первый повторяющийся элемент
python
def first_duplicate(arr):
    seen = set()
    for num in arr:
        if num in seen:
            return num
        seen.add(num)
    
28. Идеальное хеширование
Идеальное хеширование - хеш-функция без коллизий для фиксированного набора ключей. Применяется когда набор ключей известен заранее и не изменяется (например, ключевые слова языка).

Статическое идеальное хеширование использует двухуровневую структуру, где на втором уровне для каждой ячейки строится своя хеш-функция без коллизий.


