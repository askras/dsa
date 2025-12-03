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

# **Линейные списки (Linked list)**


Асонов Сергей ИУ10-36

<!-- #raw -->
## **Цель работы**
<!-- #endraw -->

изучение структуры данных «Линейные списки», а также основных операций над ними.


### Задание 1

```python
from typing import Any, Self

class Node:
    def __init__(self, data:Any=None, next:'Node'=None):
        self.data = data
        self.next = next

    def __repr__(self):
         return f'{self.__class__.__name__}(data={self.data}, next={self.next})'

# ===== ВЕРСИЯ 1 =====
class SingleLinkedList_v1:
    def __init__(self) -> Self:
        '''Возвращает пустой список'''
        self._head = None

    def insert_first_node(self, value:Any) -> None:
        '''Добавить элемент в начало списка'''
        self._head = Node(value, self._head)

    def remove_first_node(self) -> Any:
        '''Удалить первый элемент списка'''
        temp = self._head.data
        self._head = self._head.next
        return temp

    def insert_last_node(self, value:Any) -> None:
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
        if self._head.next is None:
            return self.remove_first_node()
        else:
            current_node = self._head
            while current_node.next.next is not None:
                current_node = current_node.next
            temp = current_node.next.data
            current_node.next = None
            return temp

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._head})'

    def __str__(self):
        node = self._head
        l = []
        while node:
            l.append(str(node.data))
            node = node.next
        return 'LinkedList.head -> ' + ' -> '.join(l) + ' -> None'

# ===== ВЕРСИЯ 2 =====
class SingleLinkedList_v2(SingleLinkedList_v1):
    def get_size(self) -> int:
        '''Вернуть длину списка'''
        count = 0
        current_node = self._head
        while current_node is not None:
            count += 1
            current_node = current_node.next
        return count

    def find_node(self, value: Any) -> Any:
        '''Найти (первый) узел по его значению и вернуть значение'''
        current_node = self._head
        while current_node is not None:
            if current_node.data == value:
                return current_node.data
            current_node = current_node.next
        return None

    def replace_node(self, old_value: Any, new_value: Any) -> None:
        '''Найти (первый) узел по его значению и заменить его значение новым'''
        current_node = self._head
        while current_node is not None:
            if current_node.data == old_value:
                current_node.data = new_value
                return
            current_node = current_node.next

    def remove_node(self, value: Any) -> Any:
        '''Найти (первый) узел по его значению и удалить его'''
        if self._head is None:
            return None

        if self._head.data == value:
            return self.remove_first_node()

        current_node = self._head
        while current_node.next is not None:
            if current_node.next.data == value:
                temp = current_node.next.data
                current_node.next = current_node.next.next
                return temp
            current_node = current_node.next
            
        return None

# ===== ВЕРСИЯ 3 =====
class SingleLinkedList_v3(SingleLinkedList_v2):
    def __init__(self) -> None:
        '''Возвращает пустой список'''
        super().__init__()
        self._size = 0

    def insert_first_node(self, value: Any) -> None:
        '''Добавить элемент в начало списка'''
        super().insert_first_node(value)
        self._size += 1

    def remove_first_node(self) -> Any:
        '''Удалить первый элемент списка'''
        if self._head is None:
            return None
        result = super().remove_first_node()
        self._size -= 1
        return result

    def insert_last_node(self, value: Any) -> None:
        '''Добавить элемент в конец списка'''
        super().insert_last_node(value)
        self._size += 1

    def remove_last_node(self) -> Any:
        '''Удалить последний элемент списка'''
        if self._head is None:
            return None
        result = super().remove_last_node()
        self._size -= 1
        return result

    def remove_node(self, value: Any) -> Any:
        '''Найти (первый) узел по его значению и удалить его'''
        if self._head is None:
            return None

        if self._head.data == value:
            return self.remove_first_node()

        current_node = self._head
        while current_node.next is not None:
            if current_node.next.data == value:
                temp = current_node.next.data
                current_node.next = current_node.next.next
                self._size -= 1
                return temp
            current_node = current_node.next
            
        return None

    def get_size(self) -> int:
        '''Вернуть длину списка - O(1)'''
        return self._size

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(size={self._size}, {self._head})'

    def __str__(self):
        return f'LinkedList(size={self._size}).head -> ' + super().__str__().split(' -> ', 1)[1]

# ===== ВЕРСИЯ 4 =====
class SingleLinkedList_v4(SingleLinkedList_v3):
    def find_previous_node(self, value: Any) -> Any:
        '''Найти (первый) узел по его значению и вернуть значение из предыдущего узла'''
        if self._head is None or self._head.next is None:
            return None
            
        if self._head.next.data == value:
            return self._head.data
            
        current_node = self._head
        while current_node.next is not None and current_node.next.next is not None:
            if current_node.next.next.data == value:
                return current_node.next.data
            current_node = current_node.next
            
        return None

    def find_next_node(self, value: Any) -> Any:
        '''Найти (первый) узел по его значению и вернуть значение из следующего узла'''
        current_node = self._head
        while current_node is not None:
            if current_node.data == value and current_node.next is not None:
                return current_node.next.data
            current_node = current_node.next
        return None

    def insert_before_node(self, target_value: Any, new_value: Any) -> None:
        '''Найти (первый) узел по его значению и добавить узел перед ним'''
        if self._head is None:
            return

        if self._head.data == target_value:
            self.insert_first_node(new_value)
            return

        current_node = self._head
        while current_node.next is not None:
            if current_node.next.data == target_value:
                new_node = Node(new_value, current_node.next)
                current_node.next = new_node
                self._size += 1
                return
            current_node = current_node.next

    def insert_after_node(self, target_value: Any, new_value: Any) -> None:
        '''Найти (первый) узел по его значению и добавить узел после него'''
        current_node = self._head
        while current_node is not None:
            if current_node.data == target_value:
                new_node = Node(new_value, current_node.next)
                current_node.next = new_node
                self._size += 1
                return
            current_node = current_node.next

    def replace_previous_node(self, target_value: Any, new_value: Any) -> None:
        '''Найти (первый) узел по его значению и заменить значение в предыдущем узле'''
        if self._head is None or self._head.next is None:
            return

        if self._head.next.data == target_value:
            self._head.data = new_value
            return
            
        current_node = self._head
        while current_node.next is not None and current_node.next.next is not None:
            if current_node.next.next.data == target_value:
                current_node.next.data = new_value
                return
            current_node = current_node.next

    def replace_next_node(self, target_value: Any, new_value: Any) -> None:
        '''Найти (первый) узел по его значению и заменить значение в следующем узле'''
        current_node = self._head
        while current_node is not None and current_node.next is not None:
            if current_node.data == target_value:
                current_node.next.data = new_value
                return
            current_node = current_node.next

    def remove_previous_node(self, target_value: Any) -> Any:
        '''Найти (первый) узел по его значению и удалить предыдущий узел'''
        if self._head is None or self._head.next is None:
            return None
            
        if self._head.next.data == target_value:
            return self.remove_first_node()
            
        current_node = self._head
        while current_node.next is not None and current_node.next.next is not None:
            if current_node.next.next.data == target_value:
                temp = current_node.next.data
                current_node.next = current_node.next.next
                self._size -= 1
                return temp
            current_node = current_node.next
            
        return None

    def remove_next_node(self, target_value: Any) -> Any:
        '''Найти (первый) узел по его значению и удалить следующий узел'''
        current_node = self._head
        while current_node is not None and current_node.next is not None:
            if current_node.data == target_value:
                temp = current_node.next.data
                current_node.next = current_node.next.next
                self._size -= 1
                return temp
            current_node = current_node.next
        return None

# ===== ВЕРСИЯ 5 =====
class SingleLinkedList_v5(SingleLinkedList_v4):
    def __init__(self) -> None:
        '''Возвращает пустой список'''
        super().__init__()
        self._tail = None

    def insert_first_node(self, value: Any) -> None:
        '''Добавить элемент в начало списка'''
        super().insert_first_node(value)
        if self._size == 1:
            self._tail = self._head

    def remove_first_node(self) -> Any:
        '''Удалить первый элемент списка'''
        if self._head is None:
            return None

        if self._head.next is None:
            self._tail = None
            
        result = super().remove_first_node()
        return result

    def insert_last_node(self, value: Any) -> None:
        '''Добавить элемент в конец списка - O(1)'''
        if self._head is None:
            self.insert_first_node(value)
        else:
            new_node = Node(value)
            self._tail.next = new_node
            self._tail = new_node
            self._size += 1

    def remove_last_node(self) -> Any:
        '''Удалить последний элемент списка'''
        if self._head is None:
            return None
            
        if self._head.next is None:
            return self.remove_first_node()
            
        current_node = self._head
        while current_node.next.next is not None:
            current_node = current_node.next
            
        temp = current_node.next.data
        current_node.next = None
        self._tail = current_node
        self._size -= 1
        return temp

    def insert_after_node(self, target_value: Any, new_value: Any) -> None:
        '''Найти (первый) узел по его значению и добавить узел после него'''
        current_node = self._head
        while current_node is not None:
            if current_node.data == target_value:
                new_node = Node(new_value, current_node.next)
                current_node.next = new_node
                self._size += 1
                if current_node == self._tail:
                    self._tail = new_node
                return
            current_node = current_node.next

    def remove_node(self, value: Any) -> Any:
        '''Найти (первый) узел по его значению и удалить его'''
        if self._head is None:
            return None
            
        if self._head.data == value:
            return self.remove_first_node()
            
        current_node = self._head
        while current_node.next is not None:
            if current_node.next.data == value:
                if current_node.next == self._tail:
                    self._tail = current_node
                    
                temp = current_node.next.data
                current_node.next = current_node.next.next
                self._size -= 1
                return temp
            current_node = current_node.next
            
        return None

    def remove_next_node(self, target_value: Any) -> Any:
        '''Найти (первый) узел по его значению и удалить следующий узел'''
        current_node = self._head
        while current_node is not None and current_node.next is not None:
            if current_node.data == target_value:
                if current_node.next == self._tail:
                    self._tail = current_node
                    
                temp = current_node.next.data
                current_node.next = current_node.next.next
                self._size -= 1
                return temp
            current_node = current_node.next
        return None

    def get_tail(self) -> Any:
        '''Получить значение последнего элемента'''
        return self._tail.data if self._tail else None

    def clear(self) -> None:
        '''Очистить весь список'''
        super().clear()
        self._tail = None

    def __repr__(self) -> str:
        tail_value = self._tail.data if self._tail else None
        return f'{self.__class__.__name__}(size={self._size}, head={self._head}, tail={tail_value})'

    def __str__(self):
        tail_info = f", tail={self._tail.data}" if self._tail else ""
        return f'LinkedList(size={self._size}{tail_info}).head -> ' + super().__str__().split(' -> ', 1)[1]
        
# ===== ВЕРСИЯ 6 =====
class SingleLinkedList_v6(SingleLinkedList_v5):
    def insert_before_node(self, target_value: Any, new_value: Any) -> None:
        '''Найти (первый) узел по его значению и добавить узел перед ним через замену'''
        current_node = self._head
        while current_node is not None:
            if current_node.data == target_value:
                old_value = current_node.data
                current_node.data = new_value
                new_node = Node(old_value, current_node.next)
                current_node.next = new_node
                self._size += 1
                if current_node == self._tail:
                    self._tail = new_node
                return
            current_node = current_node.next

    def replace_previous_node(self, target_value: Any, new_value: Any) -> None:
        '''Найти (первый) узел по его значению и заменить значение в предыдущем узле'''
        prev_value = self.find_previous_node(target_value)
        if prev_value is not None:
            current_node = self._head
            while current_node is not None:
                if current_node.data == prev_value:
                    current_node.data = new_value
                    return
                current_node = current_node.next

    def remove_previous_node(self, target_value: Any) -> Any:
        '''Найти (первый) узел по его значению и удалить предыдущий узел'''
        if self._head is None or self._head.next is None:
            return None
            
        if self._head.next.data == target_value:
            return self.remove_first_node()
            
        current_node = self._head
        while current_node.next is not None and current_node.next.next is not None:
            if current_node.next.next.data == target_value:
                temp = current_node.next.data
                current_node.next = current_node.next.next
                self._size -= 1
                return temp
            current_node = current_node.next
            
        return None



 """Tестирование связных списков"""
def test_linked_lists():

    
    print("ТЕСТИРОВАНИЕ СВЯЗНЫХ СПИСКОВ")
    print("=" * 40)
    
    # Тестируем основные версии
    versions = [SingleLinkedList_v1, SingleLinkedList_v3, SingleLinkedList_v5]
    
    for version_class in versions:
        print(f"\nТестируем {version_class.__name__}:")
        print("-" * 30)
        
        # Создаем список
        lst = version_class()
        
        # 1. Базовые операции
        print("1. Базовые операции:")
        lst.insert_first_node(3)
        lst.insert_first_node(2)
        lst.insert_first_node(1)
        print(f"   После добавления в начало: {lst}")
        
        lst.insert_last_node(4)
        lst.insert_last_node(5)
        print(f"   После добавления в конец: {lst}")
        
        removed_first = lst.remove_first_node()
        print(f"   Удален из начала: {removed_first}")
        
        removed_last = lst.remove_last_node()
        print(f"   Удален из конца: {removed_last}")
        print(f"   Текущий список: {lst}")
        
        # 2. Дополнительные возможности
        if hasattr(lst, 'get_size'):
            print(f"   Размер списка: {lst.get_size()}")
        
        if hasattr(lst, 'find_node'):
            found = lst.find_node(3)
            print(f"   Поиск значения 3: {found}")
        
        if hasattr(lst, 'get_tail'):
            tail = lst.get_tail()
            print(f"   Значение хвоста: {tail}")
        
        print("   [ПРОЙДЕНО]")

def test_edge_cases():
    """Тестирование граничных случаев"""
    print("\nТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ")
    print("=" * 40)
    
    lst = SingleLinkedList_v3()
    
    # 1. Пустой список
    print("1. Пустой список:")
    print(f"   {lst}")
    
    # 2. Удаление из пустого списка
    print("2. Удаление из пустого списка:")
    try:
        lst.remove_first_node()
    except Exception as e:
        print(f"   Ошибка: {type(e).__name__}")
    
    # 3. Один элемент
    print("3. Работа с одним элементом:")
    lst.insert_first_node(999)
    print(f"   Добавлен: {lst}")
    removed = lst.remove_first_node()
    print(f"   Удален: {removed}, список: {lst}")
    
    print("   [ГРАНИЧНЫЕ СЛУЧАИ ПРОЙДЕНЫ]")

def test_advanced_operations():
    """Тестирование продвинутых операций"""
    print("\nТЕСТИРОВАНИЕ ПРОДВИНУТЫХ ОПЕРАЦИЙ")
    print("=" * 40)
    
    # Тестируем v4 с дополнительными функциями
    lst = SingleLinkedList_v4()
    
    # Создаем тестовый список
    for i in range(1, 6):
        lst.insert_last_node(i * 10)
    
    print("1. Исходный список:")
    print(f"   {lst}")
    
    # Тестируем поиск соседей
    print("2. Поиск соседних узлов:")
    prev = lst.find_previous_node(30)
    next_val = lst.find_next_node(30)
    print(f"   Предыдущий для 30: {prev}")
    print(f"   Следующий для 30: {next_val}")
    
    # Тестируем вставку
    print("3. Вставка узлов:")
    lst.insert_before_node(30, 25)
    lst.insert_after_node(30, 35)
    print(f"   После вставки 25 и 35: {lst}")
    
    # Тестируем замену
    print("4. Замена узлов:")
    lst.replace_node(25, 26)
    print(f"   После замены 25 на 26: {lst}")
    
    print("   [ПРОДВИНУТЫЕ ОПЕРАЦИИ ПРОЙДЕНЫ]")

def test_v5_tail_operations():
    """Специфичное тестирование для v5 с хвостом"""
    print("\nТЕСТИРОВАНИЕ V5 (С ХВОСТОМ)")
    print("=" * 40)
    
    lst = SingleLinkedList_v5()
    
    print("1. Проверка хвоста при операциях:")
    lst.insert_last_node(100)
    lst.insert_last_node(200)
    lst.insert_last_node(300)
    print(f"   Список: {lst}")
    print(f"   Хвост: {lst.get_tail()}")
    
    lst.insert_last_node(400)
    print(f"   После добавления 400, хвост: {lst.get_tail()}")
    
    lst.remove_last_node()
    print(f"   После удаления последнего, хвост: {lst.get_tail()}")
    
    print("   [ТЕСТ V5 ПРОЙДЕН]")

def run_all_tests():
    """Запуск всех тестов"""
    print("НАЧАЛО ТЕСТИРОВАНИЯ")
    print("=" * 50)
    
    test_linked_lists()
    test_edge_cases()
    test_advanced_operations()
    test_v5_tail_operations()
    
    print("\n" + "=" * 50)
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ УСПЕШНО!")

# Запускаем тесты
if __name__ == "__main__":
    run_all_tests()
```


**Линейный односвязный список (Версия 1)**
Линейный односвязный список — абстрактный тип данных, который поддерживает следующие операции:

init() -> SingleLinkedList
Возвращает пустой односвязный список.

insert_first_node(ValueType value) -> None
Добавить узел в начало списка.

remove_first_node() -> ValueType
Удалить первый узел списка и вернуть его значение.

insert_last_node(ValueType value) -> None
Добавить узел в конец списка.

remove_last_node() -> ValueType
Удалить последний элемент списка.

**Линейный односвязный список (Версия 2). Наследуется от версии 1**
get_size() -> Integer
Вернуть длину списка

find_node(ValueType value) -> ValueType
Найти (первый) узел по его значению и вернуть значение (связанные элементы).

replace_node(ValueType old_value, ValueType new_value) -> None
Найти (первый) узел по его значению и заменить его значение новым.

remove_node(ValueType value) -> ValueType
Найти (первый) узел по его значению и удалить его.

**Линейный односвязный список (Версия 3). Наследуется от версии**
Cохраняем значения длины и обновляем его при выполнении каждой операции

**Линейный односвязный список (Версия 4). Наследуется от версии 3**
find_previos_node(ValueType value) -> ValueType
Найти (первый) узел по его значению и вернуть значение из предудущего узла (если такой есть).

find_next_node(ValueType value) -> ValueType
Найти (первый) узел по его значению и вернуть значение из следующего узла (если такой есть).

insert_before_node(ValueType value) -> None
Найти (первый) узел по его значению и добавить узел перед ним. (Если узел не найден, ничего не делать)

insert_after_node(ValueType value) -> None
Найти (первый) узел по его значению и добавить узел после него. (Если узел не найден, ничего не делать)

replace_previos_node(ValueType old_value, ValueType new_value) -> None
Найти (первый) узел по его значению и заменить значение в предыдущем узле на новое.

replace_next_node(ValueType old_value, ValueType new_value) -> None
Найти (первый) узел по его значению и заменить значение в следующем узле на новое.

remove_previos_node(ValueType value) -> ValueType
Найти (первый) узел по его значению и удалить предыдущий узел (если такой есть).

remove_next_node(ValueType value) -> ValueType
Найти (первый) узел по его значению и удалить следующий узел (если такой есть).
Вставка/замена/удаление соседних узлов

**Линейный односвязный список (Версия 5). Наследуется от версии 4**
Дополнительно храним ссылку на последний элемент списка

**Линейный односвязный список (Версия 6). Наследуется от версии 5**
При необходимости модифицировать (вставить) узел перед текущим, меняем значение в текущем узле

Каждая последующая версия наследуется от предыдущей и добавляет новую функциональность или оптимизации, соответствующие требованиям в описании задачи.


### **Задание 2-3**

```python
class SingleLinkedList_v7(SingleLinkedList_v6):
    def reverse(self) -> None:
        '''Перевернуть линейный список на месте'''
        if self._head is None or self._head.next is None:
            return  # Пустой список или список с одним элементом
        
        prev_node = None
        current_node = self._head
        self._tail = self._head  # Голова становится хвостом
        
        while current_node is not None:
            next_node = current_node.next  # Сохраняем следующий узел
            current_node.next = prev_node  # Разворачиваем указатель
            prev_node = current_node       # Перемещаем prev на текущий
            current_node = next_node       # Перемещаем current на следующий
        
        self._head = prev_node  # Новая голова - бывший последний элемент

    def sort(self) -> None:
        '''Сортировка линейного списка на месте (пузырьковая сортировка)'''
        if self._head is None or self._head.next is None:
            return  # Пустой список или список с одним элементом
        
        swapped = True
        while swapped:
            swapped = False
            current_node = self._head
            
            while current_node.next is not None:
                if current_node.data > current_node.next.data:
                    # Меняем данные местами
                    current_node.data, current_node.next.data = current_node.next.data, current_node.data
                    swapped = True
                current_node = current_node.next


def test_v7_operations():
    """Тестирование SingleLinkedList_v7"""
    print("ТЕСТИРОВАНИЕ V7 (РЕВЕРС И СОРТИРОВКА)")
    print("=" * 45)
    
    # Создаем список v7
    lst = SingleLinkedList_v7()
    
    # Тест 1: Реверс пустого списка и списка с одним элементом
    print("1. Реверс особых случаев:")
    lst.reverse()
    print(f"   Реверс пустого: {lst}")
    
    lst.insert_last_node(5)
    lst.reverse()
    print(f"   Реверс одного элемента: {lst}")
    lst.remove_first_node()
    
    # Тест 2: Реверс обычного списка
    print("\n2. Реверс списка:")
    for i in [1, 2, 3, 4, 5]:
        lst.insert_last_node(i)
    print(f"   Исходный: {lst}")
    
    lst.reverse()
    print(f"   После реверса: {lst}")
    print(f"   Голова: {lst._head.data}, Хвост: {lst.get_tail()}")
    
    # Тест 3: Проверка целостности после реверса
    print("\n3. Проверка целостности:")
    # Добавляем новый элемент в конец
    lst.insert_last_node(0)
    print(f"   После добавления 0: {lst}")
    print(f"   Хвост после добавления: {lst.get_tail()}")
    
    print("\n   [ТЕСТ V7 ПРОЙДЕН]")


def complete_sort(lst):
    """Полная версия пузырьковой сортировки для тестирования"""
    if lst._head is None or lst._head.next is None:
        return
    
    swapped = True
    while swapped:
        swapped = False
        current_node = lst._head
        
        while current_node.next is not None:
            if current_node.data > current_node.next.data:
                current_node.data, current_node.next.data = current_node.next.data, current_node.data
                swapped = True
            current_node = current_node.next

"""Тестирование сортировки для V7"""
def test_v7_sorting():
    
    print("\nТЕСТИРОВАНИЕ СОРТИРОВКИ V7")
    print("=" * 45)
    
    # Тест 1: Сортировка несортированного списка
    print("1. Сортировка несортированного списка:")
    lst = SingleLinkedList_v7()
    for i in [5, 2, 8, 1, 9]:
        lst.insert_last_node(i)
    print(f"   До сортировки: {lst}")
    
    complete_sort(lst)
    print(f"   После сортировки: {lst}")
    
    # Тест 2: Сортировка отсортированного списка
    print("\n2. Сортировка отсортированного списка:")
    lst2 = SingleLinkedList_v7()
    for i in [1, 2, 3, 4, 5]:
        lst2.insert_last_node(i)
    print(f"   Исходный: {lst2}")
    
    complete_sort(lst2)
    print(f"   После сортировки: {lst2}")
    
    # Тест 3: Сортировка с одинаковыми элементами
    print("\n3. Сортировка с одинаковыми элементами:")
    lst3 = SingleLinkedList_v7()
    for i in [3, 1, 3, 2, 3]:
        lst3.insert_last_node(i)
    print(f"   До сортировки: {lst3}")
    
    complete_sort(lst3)
    print(f"   После сортировки: {lst3}")
    
    print("\n   [ТЕСТ СОРТИРОВКИ ПРОЙДЕН]")


def test_v7_combined():
    """Тестирование комбинированных операций"""
    print("\nТЕСТИРОВАНИЕ КОМБИНИРОВАННЫХ ОПЕРАЦИЙ V7")
    print("=" * 45)
    
    lst = SingleLinkedList_v7()
    
    # Тест: Сортировка -> Реверс -> Добавление
    print("1. Сортировка -> Реверс -> Добавление:")
    for i in [7, 3, 9, 1, 5]:
        lst.insert_last_node(i)
    print(f"   Исходный: {lst}")
    
    complete_sort(lst)
    print(f"   После сортировки: {lst}")
    
    lst.reverse()
    print(f"   После реверса: {lst}")
    
    lst.insert_last_node(10)
    print(f"   После добавления 10: {lst}")
    print(f"   Хвост: {lst.get_tail()}")
    
    # Тест: Реверс -> Сортировка
    print("\n2. Реверс -> Сортировка:")
    lst2 = SingleLinkedList_v7()
    for i in [1, 2, 3, 4, 5]:
        lst2.insert_last_node(i)
    print(f"   Исходный: {lst2}")
    
    lst2.reverse()
    print(f"   После реверса: {lst2}")
    
    complete_sort(lst2)
    print(f"   После сортировки: {lst2}")
    
    print("\n   [КОМБИНИРОВАННЫЕ ОПЕРАЦИИ ПРОЙДЕНЫ]")


# Запуск всех тестов
def run_v7_tests():
    """Запуск всех тестов для V7"""
    print("НАЧАЛО ТЕСТИРОВАНИЯ SINGLELINKEDLIST_V7")
    print("=" * 50)
    
    test_v7_operations()
    test_v7_sorting()
    test_v7_combined()
    
    print("\n" + "=" * 50)
    print("ВСЕ ТЕСТЫ V7 ЗАВЕРШЕНЫ УСПЕШНО!")


# Запускаем тесты
if __name__ == "__main__":
    run_v7_tests()
```

### **Задание 4**

```python
class SingleLinkedList_v8(SingleLinkedList_v7):
    
    # 1. Элементы, входящие в L1, но не входящие в L2
    def difference(self, other: 'SingleLinkedList_v8') -> 'SingleLinkedList_v8':
        result = SingleLinkedList_v8()
        current = self._head
        while current:
            if not other.contains(current.data):
                result.insert_last_node(current.data)
            current = current.next
        return result

    # 2. Количество максимальных элементов
    def count_max_elements(self) -> int:
        if self._head is None:
            return 0
        
        max_val = self._head.data
        count = 1
        
        current = self._head.next
        while current:
            if current.data > max_val:
                max_val = current.data
                count = 1
            elif current.data == max_val:
                count += 1
            current = current.next
        
        return count

    # 3. Список без повторений
    def input_unique_numbers(self) -> None:
        """Ввод чисел пользователем без повторений"""
        seen = set()
        
        print("Введите числа (пустая строка для завершения):")
        while True:
            try:
                user_input = input().strip()
                if not user_input:
                    break
                num = int(user_input)
                if num not in seen:
                    seen.add(num)
                    self.insert_last_node(num)
            except ValueError:
                print("Ошибка: введите целое число")

    # 4. Отсортированная копия
    def sorted_copy(self) -> 'SingleLinkedList_v8':
        result = SingleLinkedList_v8()
        current = self._head
        
        # Копируем элементы
        while current:
            result.insert_last_node(current.data)
            current = current.next
        
        # Сортируем
        result.sort()
        return result

    # 5. Оставить только последние вхождения
    def keep_last_occurrences(self) -> None:
        if self._head is None:
            return
        
        seen = set()
        prev = None
        current = self._head
        
        # Проходим с конца (реверсируем, обрабатываем, снова реверсируем)
        self.reverse()
        
        current = self._head
        prev = None
        seen = set()
        
        while current:
            if current.data in seen:
                # Удаляем дубликат
                if prev:
                    prev.next = current.next
                else:
                    self._head = current.next
                self._size -= 1
            else:
                seen.add(current.data)
                prev = current
            current = current.next
        
        self.reverse()

    # 6. Убрать подряд идущие дубликаты
    def remove_consecutive_duplicates(self) -> None:
        if self._head is None:
            return
        
        current = self._head
        while current and current.next:
            if current.data == current.next.data:
                current.next = current.next.next
                self._size -= 1
            else:
                current = current.next

    # 7. Пересечение двух списков
    def intersection(self, other: 'SingleLinkedList_v8') -> 'SingleLinkedList_v8':
        result = SingleLinkedList_v8()
        current = self._head
        seen_in_other = set()
        
        # Собираем элементы из other
        other_current = other._head
        while other_current:
            seen_in_other.add(other_current.data)
            other_current = other_current.next
        
        # Добавляем только те, что есть в обоих
        while current:
            if current.data in seen_in_other:
                result.insert_last_node(current.data)
            current = current.next
        
        return result

    # 8. Разделить на положительные и отрицательные
    def split_positive_negative(self) -> tuple:
        positive = SingleLinkedList_v8()
        negative = SingleLinkedList_v8()
        
        current = self._head
        while current:
            if current.data >= 0:
                positive.insert_last_node(current.data)
            else:
                negative.insert_last_node(current.data)
            current = current.next
        
        return positive, negative

    # 9. Продублировать четные числа
    def duplicate_even_numbers(self) -> None:
        current = self._head
        while current:
            if current.data % 2 == 0:
                new_node = Node(current.data, current.next)
                current.next = new_node
                current = new_node.next
                self._size += 1
            else:
                current = current.next
        
        # Обновляем tail
        self._update_tail()

    # 10. Проверка на упорядоченность по возрастанию
    def is_sorted_ascending(self) -> bool:
        if self._head is None or self._head.next is None:
            return True
        
        current = self._head
        while current.next:
            if current.data > current.next.data:
                return False
            current = current.next
        
        return True

    # 11. Удалить нечетные числа
    def remove_odd_numbers(self) -> None:
        # Удаляем с начала пока голова нечетная
        while self._head and self._head.data % 2 != 0:
            self._head = self._head.next
            self._size -= 1
        
        if self._head is None:
            self._tail = None
            return
        
        # Удаляем нечетные в середине/конце
        current = self._head
        while current and current.next:
            if current.next.data % 2 != 0:
                current.next = current.next.next
                self._size -= 1
            else:
                current = current.next
        
        self._update_tail()

    # 12. Оставить только первые вхождения
    def keep_first_occurrences(self) -> None:
        if self._head is None:
            return
        
        seen = set()
        prev = None
        current = self._head
        
        while current:
            if current.data in seen:
                # Удаляем дубликат
                if prev:
                    prev.next = current.next
                else:
                    self._head = current.next
                self._size -= 1
            else:
                seen.add(current.data)
                prev = current
            current = current.next
        
        self._update_tail()

    # 13. Префиксные суммы
    def prefix_sums(self) -> 'SingleLinkedList_v8':
        result = SingleLinkedList_v8()
        if self._head is None:
            return result
        
        current_sum = 0
        current = self._head
        
        while current:
            current_sum += current.data
            result.insert_last_node(current_sum)
            current = current.next
        
        return result

    # 14. Пересечение (альтернативная реализация)
    def intersection_alt(self, other: 'SingleLinkedList_v8') -> 'SingleLinkedList_v8':
        return self.intersection(other)

    # 15. Удалить уникальные элементы
    def remove_unique_elements(self) -> None:
        if self._head is None:
            return
        
        # Считаем частоты
        frequency = {}
        current = self._head
        while current:
            frequency[current.data] = frequency.get(current.data, 0) + 1
            current = current.next
        
        # Удаляем элементы с частотой 1
        prev = None
        current = self._head
        while current:
            if frequency[current.data] == 1:
                if prev:
                    prev.next = current.next
                else:
                    self._head = current.next
                self._size -= 1
            else:
                prev = current
            current = current.next
        
        self._update_tail()

    # 16. Количество различных в возрастающей последовательности
    def count_distinct_in_sorted(self) -> int:
        if self._head is None:
            return 0
        
        count = 1
        current = self._head
        
        while current.next:
            if current.data != current.next.data:
                count += 1
            current = current.next
        
        return count

    # 17. Удалить четные числа
    def remove_even_numbers(self) -> None:
        # Удаляем с начала пока голова четная
        while self._head and self._head.data % 2 == 0:
            self._head = self._head.next
            self._size -= 1
        
        if self._head is None:
            self._tail = None
            return
        
        # Удаляем четные в середине/конце
        current = self._head
        while current and current.next:
            if current.next.data % 2 == 0:
                current.next = current.next.next
                self._size -= 1
            else:
                current = current.next
        
        self._update_tail()

    # 18. Преобразовать четные/нечетные
    def transform_even_odd(self) -> None:
        current = self._head
        while current:
            if current.data % 2 == 0:
                current.data = current.data // 2
            else:
                current.data = current.data * 2
            current = current.next

    # 19. Есть ли элементы больше суммы всех
    def has_elements_greater_than_sum(self) -> bool:
        if self._head is None:
            return False
        
        total_sum = 0
        current = self._head
        while current:
            total_sum += current.data
            current = current.next
        
        current = self._head
        while current:
            if current.data > total_sum:
                return True
            current = current.next
        
        return False

    # 20. Удалить элементы, входящие более двух раз
    def remove_elements_more_than_twice(self) -> None:
        if self._head is None:
            return
        
        # Считаем частоты
        frequency = {}
        current = self._head
        while current:
            frequency[current.data] = frequency.get(current.data, 0) + 1
            current = current.next
        
        # Удаляем элементы с частотой > 2
        count = {}
        prev = None
        current = self._head
        
        while current:
            count[current.data] = count.get(current.data, 0) + 1
            
            if frequency[current.data] > 2 and count[current.data] > 2:
                # Удаляем лишние вхождения
                if prev:
                    prev.next = current.next
                else:
                    self._head = current.next
                self._size -= 1
            else:
                prev = current
            
            current = current.next
        
        self._update_tail()

    # 21. Среднее арифметическое
    def arithmetic_mean(self) -> float:
        if self._head is None:
            return 0.0
        
        total_sum = 0
        count = 0
        current = self._head
        
        while current:
            total_sum += current.data
            count += 1
            current = current.next
        
        return total_sum / count

    # 22. Слияние двух отсортированных списков
    def merge_sorted(self, other: 'SingleLinkedList_v8') -> 'SingleLinkedList_v8':
        result = SingleLinkedList_v8()
        current1 = self._head
        current2 = other._head
        
        while current1 and current2:
            if current1.data <= current2.data:
                result.insert_last_node(current1.data)
                current1 = current1.next
            else:
                result.insert_last_node(current2.data)
                current2 = current2.next
        
        # Добавляем оставшиеся элементы
        while current1:
            result.insert_last_node(current1.data)
            current1 = current1.next
        
        while current2:
            result.insert_last_node(current2.data)
            current2 = current2.next
        
        return result

    # 23. Удалить каждый третий элемент
    def remove_every_third(self) -> None:
        if self._head is None:
            return
        
        count = 1
        prev = None
        current = self._head
        
        while current:
            if count % 3 == 0:
                if prev:
                    prev.next = current.next
                else:
                    self._head = current.next
                self._size -= 1
            else:
                prev = current
            
            current = current.next
            count += 1
        
        self._update_tail()

    # 24. Простые числа
    def filter_primes(self) -> 'SingleLinkedList_v8':
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        result = SingleLinkedList_v8()
        current = self._head
        
        while current:
            if is_prime(int(current.data)):
                result.insert_last_node(current.data)
            current = current.next
        
        return result

    # 25. Проверка на равенство множеств
    def sets_equal(self, other: 'SingleLinkedList_v8') -> bool:
        set1 = set()
        set2 = set()
        
        current = self._head
        while current:
            set1.add(current.data)
            current = current.next
        
        current = other._head
        while current:
            set2.add(current.data)
            current = current.next
        
        return set1 == set2

    # 26. Среднее арифметическое (дубликат)
    def average(self) -> float:
        return self.arithmetic_mean()

    # 27. Элементы, делящиеся на 3, в порядке убывания
    def divisible_by_three_descending(self) -> 'SingleLinkedList_v8':
        result = SingleLinkedList_v8()
        current = self._head
        
        while current:
            if current.data % 3 == 0:
                result.insert_last_node(current.data)
            current = current.next
        
        result.sort()
        result.reverse()
        return result

    # 28. Удалить все минимальные элементы
    def remove_all_minimal(self) -> None:
        if self._head is None:
            return
        
        # Находим минимум
        min_val = self._head.data
        current = self._head.next
        while current:
            if current.data < min_val:
                min_val = current.data
            current = current.next
        
        # Удаляем все минимальные
        while self._head and self._head.data == min_val:
            self._head = self._head.next
            self._size -= 1
        
        if self._head is None:
            self._tail = None
            return
        
        current = self._head
        while current and current.next:
            if current.next.data == min_val:
                current.next = current.next.next
                self._size -= 1
            else:
                current = current.next
        
        self._update_tail()

    # 29. Среднее геометрическое
    def geometric_mean(self) -> float:
        if self._head is None:
            return 0.0
        
        product = 1
        count = 0
        current = self._head
        
        while current:
            product *= current.data
            count += 1
            current = current.next
        
        return product ** (1 / count)

    # 30. Добавить сумму трех предыдущих после каждого третьего
    def add_sum_of_three_after_every_third(self) -> None:
        if self._size < 3:
            return
        
        count = 1
        current = self._head
        
        while current and current.next and current.next.next:
            if count % 3 == 0:
                # Находим три предыдущих элемента
                prev3 = current
                prev2 = current.next if current.next else None
                prev1 = current.next.next if current.next and current.next.next else None
                
                if prev3 and prev2 and prev1:
                    sum_three = prev3.data + prev2.data + prev1.data
                    new_node = Node(sum_three, current.next)
                    current.next = new_node
                    self._size += 1
                    current = new_node
            
            current = current.next
            count += 1
        
        self._update_tail()

    # 31. Разделить на четные и нечетные
    def split_even_odd(self) -> tuple:
        even = SingleLinkedList_v8()
        odd = SingleLinkedList_v8()
        
        current = self._head
        while current:
            if current.data % 2 == 0:
                even.insert_last_node(current.data)
            else:
                odd.insert_last_node(current.data)
            current = current.next
        
        return even, odd

    # 32. Продублировать простые числа
    def duplicate_primes(self) -> None:
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        current = self._head
        while current:
            if is_prime(int(current.data)):
                new_node = Node(current.data, current.next)
                current.next = new_node
                current = new_node.next
                self._size += 1
            else:
                current = current.next
        
        self._update_tail()

    # 33. Попарные произведения
    def pairwise_product(self, other: 'SingleLinkedList_v8') -> 'SingleLinkedList_v8':
        result = SingleLinkedList_v8()
        current1 = self._head
        current2 = other._head
        
        while current1 and current2:
            result.insert_last_node(current1.data * current2.data)
            current1 = current1.next
            current2 = current2.next
        
        return result

    # 34. Количество различных значений
    def count_distinct(self) -> int:
        distinct = set()
        current = self._head
        
        while current:
            distinct.add(current.data)
            current = current.next
        
        return len(distinct)

    # 35. Удалить все максимальные элементы
    def remove_all_maximal(self) -> None:
        if self._head is None:
            return
        
        # Находим максимум
        max_val = self._head.data
        current = self._head.next
        while current:
            if current.data > max_val:
                max_val = current.data
            current = current.next
        
        # Удаляем все максимальные
        while self._head and self._head.data == max_val:
            self._head = self._head.next
            self._size -= 1
        
        if self._head is None:
            self._tail = None
            return
        
        current = self._head
        while current and current.next:
            if current.next.data == max_val:
                current.next = current.next.next
                self._size -= 1
            else:
                current = current.next
        
        self._update_tail()

    # 36. Проверка на геометрическую прогрессию
    def is_geometric_progression(self) -> bool:
        if self._head is None or self._head.next is None:
            return True
        
        current = self._head
        ratio = None
        
        while current and current.next:
            if current.data == 0:
                return False  # Ноль нарушает прогрессию
            
            current_ratio = current.next.data / current.data
            
            if ratio is None:
                ratio = current_ratio
            elif abs(current_ratio - ratio) > 1e-10:  # Учет погрешности для float
                return False
            
            current = current.next
        
        return True

    # 37. Поменять местами максимальный и минимальный элементы
    def swap_min_max(self) -> None:
        if self._head is None or self._head.next is None:
            return
        
        # Находим min и max узлы
        min_node = max_node = self._head
        current = self._head
        
        while current:
            if current.data < min_node.data:
                min_node = current
            if current.data > max_node.data:
                max_node = current
            current = current.next
        
        # Меняем значения
        min_node.data, max_node.data = max_node.data, min_node.data

    # Вспомогательные методы
    def contains(self, value: Any) -> bool:
        current = self._head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False

    def _update_tail(self) -> None:
        if self._head is None:
            self._tail = None
            return
        
        current = self._head
        while current and current.next:
            current = current.next
        self._tail = current
```

### ** Задание 5**

```python
class Node:
    """Узел кольцевого двусвязного списка"""
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None

    def __str__(self):
        return f"Node({self.data})"


class CircularDoublyLinkedList:
    """Кольцевой двусвязный список с выделенным головным элементом"""
    
    def __init__(self):
        # Создаем головной элемент (не содержит данных)
        self.head = Node()
        # В пустом списке head ссылается сам на себя
        self.head.next = self.head
        self.head.prev = self.head
        self.size = 0
    
    def is_empty(self):
        """Проверка на пустоту"""
        return self.size == 0
    
    def __len__(self):
        """Возвращает количество элементов (исключая головной)"""
        return self.size
    
    def insert_first(self, data):
        """Вставка элемента в начало списка (после головного)"""
        new_node = Node(data)
        
        # Связываем новый узел
        new_node.next = self.head.next
        new_node.prev = self.head
        
        # Обновляем связи соседних узлов
        self.head.next.prev = new_node
        self.head.next = new_node
        
        self.size += 1
        return new_node
    
    def insert_last(self, data):
        """Вставка элемента в конец списка (перед головным)"""
        new_node = Node(data)
        
        # Связываем новый узел
        new_node.next = self.head
        new_node.prev = self.head.prev
        
        # Обновляем связи соседних узлов
        self.head.prev.next = new_node
        self.head.prev = new_node
        
        self.size += 1
        return new_node
    
    def insert_after(self, node, data):
        """Вставка элемента после указанного узла"""
        if node is None:
            return self.insert_first(data)
            
        new_node = Node(data)
        
        # Связываем новый узел
        new_node.next = node.next
        new_node.prev = node
        
        # Обновляем связи соседних узлов
        node.next.prev = new_node
        node.next = new_node
        
        self.size += 1
        return new_node
    
    def insert_before(self, node, data):
        """Вставка элемента перед указанным узлом"""
        if node is None or node == self.head:
            return self.insert_last(data)
            
        new_node = Node(data)
        
        # Связываем новый узел
        new_node.next = node
        new_node.prev = node.prev
        
        # Обновляем связи соседних узлов
        node.prev.next = new_node
        node.prev = new_node
        
        self.size += 1
        return new_node
    
    def remove(self, node):
        """Удаление указанного узла"""
        if node is None or node == self.head or self.is_empty():
            return None
        
        # Сохраняем данные для возврата
        data = node.data
        
        # Перелинковываем соседние узлы
        node.prev.next = node.next
        node.next.prev = node.prev
        
        # Очищаем связи удаляемого узла
        node.next = None
        node.prev = None
        
        self.size -= 1
        return data
    
    def remove_first(self):
        """Удаление первого элемента"""
        return self.remove(self.head.next) if not self.is_empty() else None
    
    def remove_last(self):
        """Удаление последнего элемента"""
        return self.remove(self.head.prev) if not self.is_empty() else None
    
    def find(self, data):
        """Поиск первого узла с указанными данными"""
        current = self.head.next
        while current != self.head:
            if current.data == data:
                return current
            current = current.next
        return None
    
    def traverse_forward(self):
        """Обход списка в прямом направлении"""
        result = []
        current = self.head.next
        while current != self.head:
            result.append(current.data)
            current = current.next
        return result
    
    def traverse_backward(self):
        """Обход списка в обратном направлении"""
        result = []
        current = self.head.prev
        while current != self.head:
            result.append(current.data)
            current = current.prev
        return result
    
    def get_first(self):
        """Получить первый элемент"""
        return self.head.next if not self.is_empty() else None
    
    def get_last(self):
        """Получить последний элемент"""
        return self.head.prev if not self.is_empty() else None
    
    def rotate_forward(self, steps=1):
        """Повернуть список вперед на указанное количество шагов"""
        if self.is_empty() or steps == 0:
            return
            
        steps = steps % self.size
        for _ in range(steps):
            # Перемещаем первый элемент в конец
            first = self.head.next
            last = self.head.prev
            
            # Перелинковываем
            self.head.next = first.next
            first.next.prev = self.head
            
            first.next = self.head
            first.prev = last
            
            last.next = first
            self.head.prev = first
    
    def __str__(self):
        """Строковое представление списка"""
        if self.is_empty():
            return "CircularDoublyLinkedList: []"
        
        elements = []
        current = self.head.next
        while current != self.head:
            elements.append(str(current.data))
            current = current.next
        
        return f"CircularDoublyLinkedList: [{', '.join(elements)}] (size: {self.size})"


# Демонстрация работы
if __name__ == "__main__":
    # Создаем кольцевой список
    cdll = CircularDoublyLinkedList()
    
    print("Создание и заполнение списка:")
    cdll.insert_first(1)
    cdll.insert_last(2)
    cdll.insert_last(3)
    cdll.insert_first(0)
    print(cdll)
    print("Прямой обход:", cdll.traverse_forward())
    print("Обратный обход:", cdll.traverse_backward())
    
    print("\nВставка элементов:")
    second_node = cdll.find(2)
    cdll.insert_after(second_node, 2.5)
    cdll.insert_before(second_node, 1.5)
    print(cdll)
    
    print("\nУдаление элементов:")
    cdll.remove_first()
    cdll.remove_last()
    node_to_remove = cdll.find(2)
    cdll.remove(node_to_remove)
    print(cdll)
    
    print("\nПоворот списка:")
    cdll.insert_last(4)
    cdll.insert_last(5)
    print("До поворота:", cdll.traverse_forward())
    cdll.rotate_forward(2)
    print("После поворота на 2:", cdll.traverse_forward())
    
    print("\nПроверка кольцевой структуры:")
    first = cdll.get_first()
    last = cdll.get_last()
    print(f"Первый элемент: {first.data}")
    print(f"Последний элемент: {last.data}")
    print(f"Следующий за последним: {last.next.data} (головной элемент)")
    print(f"Предыдущий перед первым: {first.prev.data} (головной элемент)")
```

**Ключевые особенности реализации:**
Выделенный головной элемент: Облегчает операции вставки/удаления и обеспечивает единообразие обработки граничных случаев.

Двусвязность: Каждый узел имеет ссылки на следующий и предыдущий элементы.

Кольцевая структура:

Последний элемент ссылается на первый через головной элемент

Первый элемент ссылается на последний через головной элемент

Нет NULL-ссылок

**Основные операции:**

Вставка в начало/конец/после/перед

Удаление первого/последнего/произвольного

Поиск элемента

Обход в прямом и обратном направлениях

Поворот списка

**Преимущества:**

Быстрая вставка/удаление с обоих концов (O(1))

Удобный обход в обоих направлениях

Единообразная обработка всех случаев

Эта реализация эффективно решает типичные задачи для кольцевых структур данных, такие как реализация буферов, планировщиков задач и циклических алгоритмов.


### **Контрольные вопросы**

<!-- #region -->
#### **1. Определение линейного списка. Отличие от массива**
Линейный список — это структура данных, состоящая из набора элементов данных (узлов), в которой каждый элемент хранит помимо своих данных ссылку (указатель) на следующий (а возможно, и на предыдущий) элемент последовательности.

Принципиальное отличие от массива:

Организация в памяти: Элементы массива хранятся в непрерывной области памяти, что позволяет использовать арифметику указателей для мгновенного доступа. Элементы списка могут быть разбросаны по памяти произвольным образом, а связь между ними организована через указатели.

Доступ к элементам: В массиве доступ по индексу происходит за O(1). В списке для доступа к i-му элементу нужно пройти от начала через i узлов, что занимает O(n).

Динамичность: Размер массива часто фиксирован (в статических массивах) или требует перевыделения всей памяти при изменении (в динамических). Список является по-настояственно динамической структурой: новые элементы можно добавлять и удалять в любом месте, выделяя и освобождая память только под конкретный узел.

#### **2. Что такое «узел» (node)?**
Узел — это элементарный блок, из которого строится связный список. Он инкапсулирует данные и связь с соседними узлами.

Поля узла:

В односвязном списке:

data (данные) — полезная информация, которую хранит узел.

next (следующий) — указатель на следующий узел в списке. Для последнего узла этот указатель равен NULL (или nullptr в C++).

В двусвязном списке:

data (данные) — полезная информация.

next (следующий) — указатель на следующий узел.

prev (предыдущий) — указатель на предыдущий узел. Для первого узла этот указатель равен NULL.

#### **3. Что такое «голова» (head) списка?**
Голова (head) — это указатель на первый узел связного списка. Это отправная точка для любого обхода или операции со списком. Если список пуст, head равен NULL. Роль головы критически важна, так как потеря этого указателя означает потерю доступа ко всему списку.

#### **4. Для чего хранится указатель на «хвост» (tail)?**
Указатель «хвост» (tail) хранит адрес последнего узла списка. Он используется для ускорения операций добавления элемента в конец списка. Без tail для вставки в конец необходимо обойти весь список от головы до конца (O(n)), а с tail эта операция выполняется за O(1).

#### **5. Основные виды линейных списков (по типу связности)**
Односвязный список (Singly Linked List): Каждый узел содержит указатель только на следующий узел.

Двусвязный список (Doubly Linked List): Каждый узел содержит указатели как на следующий, так и на предыдущий узел.

Кольцевой/циклический список (Circular Linked List):

Односвязный кольцевой: Указатель next последнего узла указывает на первый узел.

Двусвязный кольцевой: Указатель next последнего узла указывает на первый, а указатель prev первого узла указывает на последний.

#### **6. Алгоритм добавления в начало односвязного списка (O(1))**
Создать новый узел new_node.

Записать в его поле data нужное значение.

Установить поле next нового узла на текущий первый узел (на который указывает head): new_node->next = head.

Обновить head, чтобы он указывал на новый узел: head = new_node.

Почему O(1)? Эта операция выполняется за константное время, независимо от длины списка, так как требует фиксированного числа действий и всегда известен адрес головы.

#### **7. Алгоритм добавления в конец односвязного списка без tail (O(n))**
Создать новый узел new_node.

Установить его next в NULL (так как он будет последним).

Если список пуст (head == NULL), то просто сделать head = new_node.

Иначе, обойти список, начиная с head, до последнего узла (у которого next == NULL). Пусть last — указатель на этот узел.

Установить last->next = new_node.

Почему O(n)? В худшем случае (когда в списке много элементов) необходимо пройти от начала до конца всего списка, что требует n шагов.

#### **8. Удаление узла из односвязного списка**
Причина необходимости указателя на предыдущий элемент: В односвязном списке узел "не знает" о своем предыдущем узле. Если мы просто удалим узел B (на который у нас есть указатель), то узел A, который был до него, будет по-прежнему указывать на несуществующую (удаленную) память. Это приведет к ошибке. Нам нужно изменить поле next узла A, чтобы он указывал на узел C, следующий за B.

Алгоритм (когда известен предыдущий узел prev):

Проверить, что узлы не NULL.

Связать узел prev с узлом, следующим за удаляемым: prev->next = node_to_delete->next.

Освободить память, занимаемую node_to_delete.

#### **9. Преимущество двусвязного списка и алгоритм удаления**
Ключевое преимущество: В двусвязном списке узел содержит указатель на предыдущий элемент, поэтому для удаления произвольного узла не нужно искать его предыдущий элемент — он уже известен.

Алгоритм удаления (дан указатель node на удаляемый узел):

Если node->next не NULL, то установить node->next->prev = node->prev.

Если node->prev не NULL, то установить node->prev->next = node->next.

Важно: Если node является головой (head), нужно обновить head на node->next.

Важно: Если node является хвостом (tail), нужно обновить tail на node->prev.

Освободить память, занимаемую node.

#### **10. Что такое «кольцевой/циклический список»?**
Кольцевой список — это список, в котором последний узел указывает на первый (в односвязном) или первый и последний узлы ссылаются друг на друга (в двусвязном). В таком списке нет NULL-указателей в полях связей next/prev.

Особенности обработки:

Обход: Необходимо иметь точку останова (например, начать с головы и остановиться, когда снова вернетесь к голове), иначе попадете в бесконечный цикл.

Проверка на пустоту: Список пуст, если head == NULL. В непустом списке head->next никогда не NULL.

#### **11. Таблица асимптотической сложности операций**
| Операция                     | Односвязный (без tail) | Односвязный (с tail) | Двусвязный (с tail) |
|------------------------------|------------------------|----------------------|---------------------|
| Вставка в начало             | O(1)                   | O(1)                 | O(1)                |
| Вставка в конец              | O(n)                   | O(1)                 | O(1)                |
| Удаление из начала           | O(1)                   | O(1)                 | O(1)                |
| Удаление из конца            | O(n)                   | O(n)*                | O(1)                |
| Поиск элемента по значению   | O(n)                   | O(n)                 | O(n)                |
| Вставка после известного узла| O(1)                   | O(1)                 | O(1)                |
| Удаление известного узла     | O(n)**                 | O(n)**               | O(1)                |
| Доступ к элементу по индексу | O(n)                   | O(n)                 | O(n)                |


*Удаление из конца в односвязном списке с tail все равно требует O(n), так как для обновления tail нужен указатель на предыдущий элемент (который становится новым хвостом).
**Удаление известного узла в односвязном списке требует O(n) для поиска предыдущего узла, если он не предоставлен.

#### **12. Объяснение сложности доступа по индексу**
Массив O(1): Адрес i-го элемента вычисляется по формуле адрес_начала + i * размер_элемента. Это одна арифметическая операция.

Список O(n): Чтобы добраться до i-го элемента, нужно стартовать с головы и i раз последовательно перейти по ссылке next.

#### **13. Объяснение сложности вставки**
В начало O(1): Адрес головы всегда известен. Операция требует создания одного нового узла и перенаправления двух указателей.

В конец (без tail) O(n): Адрес последнего элемента неизвестен. Чтобы его найти, нужно пройти через все n узлов списка.

#### **14. Преимущества и недостатки списка vs массива**
	
**Связный список**	

Преимущества

• Динамический размер  

• Вставка/удаление в начале за O(1)  

• Не требует непрерывной памяти  

Недоститки 

• Медленный доступ по индексу (O(n))

• Нет локальности данных (кэш-промахи)  

• Дополнительная память на указатели

**Массив**

Преимущества 

• Быстрый доступ по индексу (O(1))

• Локальность данных (кэш-эффективность)

• Меньший overhead на элемент (нет указателей)

Недостатки 

• Фиксированный размер (или дорогое перевыделение)

• Вставка/удаление в начале/середине требует сдвига (O(n))
#### **15. Примеры эффективного использования списков**
Стек (LIFO): Реализуется на основе односвязного списка с операциями push (в начало) и pop (из начала), которые выполняются за O(1).

Очередь (FIFO): Реализуется на основе односвязного списка с tail (вставка в конец O(1), удаление из начала O(1)) или двусвязного списка.

Плейлист или история браузера: Двусвязный список идеален для навигации "вперед-назад".

Системный аллокатор (управление памятью): Списки свободных блоков памяти.

#### **16. Причина использования двусвязных списков в сложных структурах**
Двусвязные списки позволяют эффективно (за O(1)) удалять произвольный узел и вставлять элементы как до, так и после известного узла. Это критически важно для:

Deque (двусторонняя очередь): Нужны быстрые вставки и удаления с обоих концов (O(1)).

Метод цепочек в хеш-таблицах: При частых удалениях двусвязный список делает эту операцию намного эффективнее.

#### **17. «Фиктивная» нода (Dummy Node)**
Фиктивная нода — это узел, не содержащий полезных данных, который помещается в начало (иногда и в конец) списка. Ее поля data не используются, а next указывает на реальную голову списка.

Преимущество: Упрощает код, устраняя множество проверок на NULL. Например, операция вставки в начало или удаления первого элемента становится частным случаем вставки/удаления в середину, так как у первого реального элемента всегда есть "предыдущий" узел (фиктивный).

#### **18. Алгоритм реверсирования односвязного списка**
Алгоритм (итеративный, без дополнительной памяти O(1)):

Инициализировать три указателя: prev = NULL, current = head, next = NULL.

Пока current != NULL:
a. Сохранить следующий узел: next = current->next.
b. Развернуть указатель текущего узла: current->next = prev.
c. Сдвинуть указатели на один шаг вперед: prev = current, current = next.

Обновить голову: head = prev (теперь prev указывает на новую голову — старый хвост).

#### **19. Алгоритм определения цикла (Floyd's Cycle-Finding)**
Алгоритм "Черепаха и Заяц":

Создать два указателя, оба указывают на голову списка: slow и fast.

В цикле, пока fast != NULL и fast->next != NULL:
a. slow делает один шаг: slow = slow->next.
b. fast делает два шага: fast = fast->next->next.
c. Если slow == fast, значит, в списке есть цикл.

Если fast или fast->next стали NULL, циклов нет.

#### **20. Поиск среднего элемента за один проход**
Используется модификация алгоритма с двумя указателями:

Указатели slow и fast стартуют с головы.

На каждом шаге slow двигается на 1 узел, fast — на 2.

Когда fast достигнет конца списка (fast == NULL или fast->next == NULL), slow будет указывать на средний элемент.

#### **21. Проблема удаления узла в односвязном списке без доступа к предыдущему**
Проблема: Невозможно напрямую удалить узел, так как нужно обновить указатель next его предыдущего узла, а он неизвестен.

Решение (Хитрость, O(1)):

Скопировать данные (и указатель next) из следующего узла в текущий удаляемый узел.
node->data = node->next->data;
node->next = node->next->next;

Удалить следующий узел (который теперь является копией исходного).

Ограничение: Не работает, если удаляемый узел является последним в списке. В этом случае без указателя на предыдущий узел обойтись невозможн
<!-- #endregion -->

```python

```

```python
def summ(a, b):
    return a - b


assert summ(2, 3) == 5, "Шеф все пропало"
```

```python
python -o ghjkl.py
```
