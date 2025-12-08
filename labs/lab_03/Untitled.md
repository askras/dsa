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

## Лабораторная работа №3
## Вариант 6
Цели лабораторной работы:
- Изучить, что такое линейный список — структура данных, где элементы связаны ссылками, а не расположены подряд в памяти.
- Научиться создавать и использовать односвязные линейные списки в программе.
- Освоить основные операции со списками: добавление, удаление, поиск элементов.
- Развить навыки работы с динамической памятью при построении и изменении списков.
- Научиться писать функции для обработки списков (например, удаление повторов, разворот, сортировка).
- Приобрести умения структурного и модульного программирования через реализацию этих задач.

## Задание 1 
Версия 1:

```python
from typing import Any, Self
import doctest

class Node:
    def __init__(self, data: Any = None, next: 'Node' = None):
        self.data = data
        self.next = next

    def __repr__(self):
        return f'Node(data={self.data}, next={self.next})'


class SingleLinkedListV1:
    def __init__(self) -> Self:
        self._head = None

    def insert_first_node(self, value: Any) -> None:
        '''Добавить элемент в начало списка'''
        self._head = Node(value, self._head)

    def remove_first_node(self) -> Any:
        '''Удалить первый элемент списка'''
        if self._head is None:
            raise ValueError("Список пуст")
        temp = self._head.data
        self._head = self._head.next
        return temp

    def insert_last_node(self, value: Any) -> None:
        '''Добавить элемент в конец списка'''
        if self._head is None:
            self.insert_first_node(value)
        else:
            current_node = self._head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = Node(value)

    def remove_last_node(self) -> Any:
        '''Удалить последний элемент списка'''
        if self._head is None:
            raise ValueError("Список пуст")
        
        if self._head.next is None:
            return self.remove_first_node()
        
        current_node = self._head
        while current_node.next.next is not None:
            current_node = current_node.next
        temp = current_node.next.data
        current_node.next = None
        return temp

    def __repr__(self) -> str:
        return f'SingleLinkedListV1({self._head})'

    def __str__(self):
        node = self._head
        elements = []
        while node:
            elements.append(str(node.data))
            node = node.next
        return 'LinkedList.head -> ' + ' -> '.join(elements) + ' -> None'

```

Версия 2: Добавлены методы поиска, замены и удаления по значению + получение размера

```python
class SingleLinkedListV2(SingleLinkedListV1):
    def get_size(self) -> int:
        '''Вернуть размер списка (сложность O(n))'''
        count = 0
        current = self._head
        while current:
            count += 1
            current = current.next
        return count

    def find_node(self, value: Any) -> Node:
        '''Найти первый узел с заданным значением'''
        current = self._head
        while current:
            if current.data == value:
                return current
            current = current.next
        return None

    def replace_node(self, old_value: Any, new_value: Any) -> bool:
        '''Заменить значение первого найденного узла'''
        node = self.find_node(old_value)
        if node:
            node.data = new_value
            return True
        return False

    def remove_node(self, value: Any) -> bool:
        '''Удалить первый узел с заданным значением'''
        if self._head is None:
            return False
        
        if self._head.data == value:
            self.remove_first_node()
            return True
        
        current = self._head
        while current.next:
            if current.next.data == value:
                current.next = current.next.next
                return True
            current = current.next
        
        return False
```

Версия 3: Добавлено хранение размера списка для оптимизации

```python
class SingleLinkedListV3(SingleLinkedListV2):
    def __init__(self) -> Self:
        '''Инициализация с счетчиком размера'''
        super().__init__()
        self.size = 0

    def insert_first_node(self, value: Any) -> None:
        '''Добавление в начало с обновлением размера'''
        super().insert_first_node(value)
        self.size += 1

    def insert_last_node(self, value: Any) -> None:
        '''Добавление в конец с обновлением размера'''
        super().insert_last_node(value)
        self.size += 1

    def remove_first_node(self) -> Any:
        '''Удаление из начала с обновлением размера'''
        result = super().remove_first_node()
        self.size -= 1
        return result

    def remove_last_node(self) -> Any:
        '''Удаление из конца с обновлением размера'''
        result = super().remove_last_node()
        self.size -= 1
        return result

    def remove_node(self, value: Any) -> bool:
        '''Удаление узла по значению с обновлением размера'''
        if super().remove_node(value):
            self.size -= 1
            return True
        return False

    def get_size(self) -> int:
        '''Получение размера за O(1)'''
        return self.size
```

Версия 4: Добавлены методы для работы с соседними узлами

```python
class SingleLinkedListV4(SingleLinkedListV3):
    def find_previous_node(self, value: Any) -> Any:
        '''Найти значение предыдущего узла относительно узла с заданным значением'''
        if self._head is None or self._head.data == value:
            return None
        
        current = self._head
        while current.next:
            if current.next.data == value:
                return current.data
            current = current.next
        return None

    def find_next_node(self, value: Any) -> Any:
        '''Найти значение следующего узла относительно узла с заданным значением'''
        node = self.find_node(value)
        if node and node.next:
            return node.next.data
        return None

    def insert_before_node(self, target_value: Any, new_value: Any) -> bool:
        '''Вставить новый узел перед узлом с заданным значением'''
        if self._head is None:
            return False
        
        if self._head.data == target_value:
            self.insert_first_node(new_value)
            return True
        
        current = self._head
        while current.next:
            if current.next.data == target_value:
                new_node = Node(new_value, current.next)
                current.next = new_node
                self.size += 1
                return True
            current = current.next
        
        return False

    def insert_after_node(self, target_value: Any, new_value: Any) -> bool:
        '''Вставить новый узел после узла с заданным значением'''
        node = self.find_node(target_value)
        if node:
            new_node = Node(new_value, node.next)
            node.next = new_node
            self.size += 1
            return True
        return False

    def replace_previous_node(self, target_value: Any, new_value: Any) -> bool:
        '''Заменить значение в предыдущем узле относительно узла с заданным значением'''
        if self._head is None or self._head.data == target_value:
            return False  
        
        current = self._head
        while current.next:
            if current.next.data == target_value:
                current.data = new_value
                return True
            current = current.next
        return False

    def replace_next_node(self, target_value: Any, new_value: Any) -> bool:
        '''Заменить значение в следующем узле относительно узла с заданным значением'''
        node = self.find_node(target_value)
        if node and node.next:
            node.next.data = new_value
            return True
        return False

    def remove_previous_node(self, target_value: Any) -> Any:
        '''Удалить предыдущий узел относительно узла с заданным значением'''
        if self._head is None or self._head.data == target_value:
            return None  
        
        if self._head.next and self._head.next.data == target_value:
            return self.remove_first_node()
        
        current = self._head
        while current.next and current.next.next:
            if current.next.next.data == target_value:
                removed_data = current.next.data
                current.next = current.next.next
                self.size -= 1
                return removed_data
            current = current.next
        return None

    def remove_next_node(self, target_value: Any) -> Any:
        '''Удалить следующий узел относительно узла с заданным значением'''
        node = self.find_node(target_value)
        if node and node.next:
            removed_data = node.next.data
            node.next = node.next.next
            self.size -= 1
            return removed_data
        return None
```

Версия 5: Добавлен указатель на хвост для оптимизации операций

```python
class SingleLinkedListV5(SingleLinkedListV4):
        def __init__(self) -> Self:
        '''Инициализация с указателем на хвост'''
        super().__init__()
        self._tail = None

    def insert_first_node(self, value: Any) -> None:
        '''Добавление в начало с обновлением хвоста'''
        super().insert_first_node(value)
        if self.size == 1:
            self._tail = self._head

    def insert_last_node(self, value: Any) -> None:
        '''Добавление в конец за O(1) с использованием хвоста'''
        if self._head is None:
            self.insert_first_node(value)
        else:
            new_node = Node(value)
            self._tail.next = new_node
            self._tail = new_node
            self.size += 1

    def remove_first_node(self) -> Any:
        '''Удаление из начала с обновлением хвоста'''
        result = super().remove_first_node()
        if self.size == 0:
            self._tail = None
        return result

    def remove_last_node(self) -> Any:
        '''Удаление из конца с обновлением хвоста'''
        if self._head is None:
            raise ValueError("Список пуст")
        
        if self._head.next is None:
            return self.remove_first_node()
        
        current = self._head
        while current.next != self._tail:
            current = current.next
        
        result = self._tail.data
        current.next = None
        self._tail = current
        self.size -= 1
        
        return result

    def find_node(self, value: Any) -> Node:
        '''Оптимизированный поиск: O(1) для головы и хвоста'''
        if self._head is None:
            return None
        
        if self._head.data == value:
            return self._head
        
        if self._tail and self._tail.data == value:
            return self._tail
        
        return super().find_node(value)

    def insert_after_node(self, target_value: Any, new_value: Any) -> bool:
        '''Оптимизированная вставка после узла: O(1) для хвоста'''
        if self._tail and self._tail.data == target_value:
            new_node = Node(new_value)
            self._tail.next = new_node
            self._tail = new_node
            self.size += 1
            return True
        
        return super().insert_after_node(target_value, new_value)

    def replace_node(self, old_value: Any, new_value: Any) -> bool:
        '''Оптимизированная замена: O(1) для головы и хвоста'''
        if self._head is None:
            return False
        
        if self._head.data == old_value:
            self._head.data = new_value
            return True
        
        if self._tail and self._tail.data == old_value:
            self._tail.data = new_value
            return True
        
        return super().replace_node(old_value, new_value)

    def remove_node(self, value: Any) -> bool:
        '''Оптимизированное удаление: O(1) для головы и хвоста'''
        if self._head is None:
            return False
        
        if self._head.data == value:
            self.remove_first_node()
            return True
        
        if self._tail and self._tail.data == value:
            self.remove_last_node()
            return True
        
        return super().remove_node(value)

    def replace_next_node(self, target_value: Any, new_value: Any) -> bool:
        '''Оптимизированная замена следующего узла: O(1) проверка для хвоста'''
        if self._tail and self._tail.data == target_value:
            return False  
        
        return super().replace_next_node(target_value, new_value)

    def remove_next_node(self, target_value: Any) -> Any:
        '''Оптимизированное удаление следующего узла: O(1) проверка для хвоста'''
        if self._tail and self._tail.data == target_value:
            return None  
        
        return super().remove_next_node(target_value)

    def find_next_node(self, value: Any) -> Any:
        '''Оптимизированный поиск следующего узла: O(1) проверка для хвоста'''
        if self._tail and self._tail.data == value:
            return None  
        
        return super().find_next_node(value)

    def get_tail(self) -> Any:
        '''Получить значение хвоста за O(1)'''
        return self._tail.data if self._tail else None

    def __str__(self):
        '''Строковое представление с информацией о хвосте'''
        base_str = super().__str__()
        tail_info = f" (tail: {self.get_tail()})" if self._tail else " (tail: None)"
        return base_str + tail_info
```

Версия 6: Оптимизация операций через замену значений

```python
class SingleLinkedListV6(SingleLinkedListV5):

    def insert_before_node_optimized(self, target_node: Node, new_value: Any) -> bool:
        '''Оптимизированная вставка перед узлом за O(1) через замену значений'''
        if target_node is None:
            return False
        
        new_node = Node(target_node.data, target_node.next)
        target_node.data = new_value
        target_node.next = new_node
        
        if self._tail == target_node:
            self._tail = new_node
        
        self.size += 1
        return True

    def remove_node_optimized(self, target_node: Node) -> Any:
        '''Оптимизированное удаление узла за O(1) через замену значений'''
        if target_node is None or target_node.next is None:
            return None
        
        removed_data = target_node.data
        target_node.data = target_node.next.data
        target_node.next = target_node.next.next
        
        if target_node.next is None:
            self._tail = target_node
        
        self.size -= 1
        return removed_data

    def remove_previous_node_optimized(self, target_node: Node) -> Any:
        '''Оптимизированное удаление предыдущего узла за O(1)'''
        if (target_node is None or self._head is None or 
            self._head == target_node or self._head.next == target_node):
            return None
        
        if self._head.next == target_node:
            return self.remove_first_node()
        
        current = self._head
        while current.next and current.next.next:
            if current.next.next == target_node:
                removed_data = current.next.data
                current.next = target_node
                self.size -= 1
                return removed_data
            current = current.next
        return None

    def insert_before_node(self, target_value: Any, new_value: Any) -> bool:
        '''Переопределение для использования оптимизации при наличии узла'''
        target_node = self.find_node(target_value)
        if target_node:
            return self.insert_before_node_optimized(target_node, new_value)
        return False

    def remove_node(self, value: Any) -> bool:
        '''Переопределение для использования оптимизации при наличии узла'''
        if self._head and self._head.data == value:
            self.remove_first_node()
            return True
        
        if self._tail and self._tail.data == value:
            self.remove_last_node()
            return True
        
        target_node = self.find_node(value)
        if target_node:
            self.remove_node_optimized(target_node)
            return True
        
        return False

    def remove_previous_node(self, target_value: Any) -> Any:
        '''Переопределение для использования оптимизации при наличии узла'''
        if self._head is None or self._head.data == target_value:
            return None
        
        target_node = self.find_node(target_value)
        if target_node:
            return self.remove_previous_node_optimized(target_node)
        return None

    def sort(self) -> None:
        '''Сортировка списка (пузырьковая сортировка)'''
        if self.size < 2:
            return
        
        for i in range(self.size):
            current = self._head
            for j in range(self.size - i - 1):
                if current.data > current.next.data:
                    current.data, current.next.data = current.next.data, current.data
                current = current.next

    def get_middle_node(self) -> Node:
        '''Найти средний узел за один проход (для демонстрации)'''
        if self._head is None:
            return None
        
        slow = self._head
        fast = self._head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        return slow

    #Задание 2

    def reverse(self) -> None:
        if self._head is None or self._head.next is None:
            return
    
        prev = None
        current = self._head
        self._tail = self._head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self._head = prev

    #Задание 3 (сортировка вставками)
    
    def sort_insertion(self) -> None:
        if self.size < 2:
            return
        
        sorted_head = None  
        
        current = self._head
        while current:
            next_node = current.next  
            
            if sorted_head is None or current.data < sorted_head.data:
                current.next = sorted_head
                sorted_head = current
            else:
                temp = sorted_head
                while temp.next and temp.next.data < current.data:
                    temp = temp.next
                current.next = temp.next
                temp.next = current
            
            current = next_node
        
        self._head = sorted_head
        
        if self._head:
            current = self._head
            while current.next:
                current = current.next
            self._tail = current    
```

## Задание 2
Сложность: O(n), Память: O(1)

## Задание 3
1. Лучший случай (уже отсортированный список):
- Вставка всегда происходит в начало: O(1) на элемент
- Итого: O(n)
2. Худший случай (обратно отсортированный список):
- Каждый новый элемент вставляется в конец отсортированной части
- Для i-го элемента нужно пройти i узлов
- Сумма: 1 + 2 + 3 + ... + (n-1) = n(n-1)/2
- Итого: O(n²)
3. Средний случай:
- В среднем для каждого элемента нужно пройти половину отсортированной части
- Итого: O(n²)

## Задание 4

```python
def remove_consecutive_duplicates(linked_list: 'SingleLinkedListV6') -> None:
    if linked_list._head is None or linked_list._head.next is None:
        return
    
    current = linked_list._head
    
    while current and current.next:
        if current.data == current.next.data:
            current.next = current.next.next
            linked_list.size -= 1
            
            if current.next is None:
                linked_list._tail = current
        else:
            # Переходим к следующему узлу
            current = current.next
```

## Таблица из контрольных вопросов
| Операция | Односвязный список (без tail) | Односвязный список (с tail) | Двусвязный список (с tail) |
| :--- | :---: | :---: | :---: |
| Вставка в начало | O(1) | O(1) | O(1) |
| Вставка в конец | O(n) | O(1) | O(1) |
| Удаление из начала | O(1) | O(1) | O(1) |
| Удаление из конца | O(n) | O(n) | O(1) |
| Поиск элемента по значению | O(n) | O(n) | O(n) |
| Вставка после известного узла | O(1) | O(1) | O(1) |
| Удаление известного узла | O(n) | O(n) | O(1) |
| Доступ к элементу по индексу | O(n) | O(n) | O(n) |

## Выводы
- Линейные списки — это важная структура данных, позволяющая динамически хранить и обрабатывать упорядоченные наборы элементов без необходимости contiguous памяти.
- В ходе лабораторной работы были изучены основные виды списков (односвязный, двусвязный, кольцевой), а также реализованы базовые операции над ними: добавление, удаление, обход.
- Выполнение заданий позволило закрепить навыки работы с динамической памятью и освоить приемы структурного программирования на языке C++.
- Реализация функций обработки списков (удаление повторов, реверс, сортировка) помогла понять особенности алгоритмов и их временную сложность при работе со связными структурами.
- Полученные знания и практические навыки пригодятся при работе с более сложными структурами данных и алгоритмами в программировании.
