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

# **Стек, Очередь, Дек**


## **Цель работы**


Изучение структур данных «Стек», «Очередь», «Дек», а также основных операций над ними.


Выполнил Асонов Сергей ИУ10-36


## **Краткие теоретические сведения**


Линейные списки являются фундаментальной структурой данных, на основе которой эффективно реализуются другие абстрактные типы данных (АТД). В данном разделе рассматривается реализация стека, очереди и дека с использованием как односвязных, так и двусвязных списков.

<!-- #region jp-MarkdownHeadingCollapsed=true -->
### **Стек (Stack)**
**Стек** — это структура данных, работающая по принципу **LIFO (Last-In, First-Out)** — «последним пришёл — первым ушёл».

**Основные операции:**

push(x) — добавление элемента x на вершину стека.
pop() — удаление и возврат элемента с вершины стека.
peek() (или top()) — возврат элемента с вершины стека без удаления.
isEmpty() — проверка стека на пустоту.
**Реализация на односвязном списке:**

Вершиной стека является **голова** списка. Добавление и удаление элемента выполняются строго с головы.

push(x): Создать новый узел new_node со значением x. Установить new_node.next = head. Переместить голову на new_node.
pop(): Если список пуст — ошибка. Иначе: сохранить значение head.data, переместить голову на head.next, вернуть сохранённое значение.
**Сложность операций:** push, pop, peek, isEmpty выполняются за O(1).

### **Очередь (Queue)**

**Очередь** — это структура данных, работающая по принципу FIFO (First-In, First-Out) — «первым пришёл — первым ушёл».

**Основные операции:**

enqueue(x) (или push) — добавление элемента x в конец очереди.
dequeue() (или pop) — удаление и возврат элемента из начала очереди.
peek() — возврат элемента из начала очереди без удаления.
isEmpty() — проверка очереди на пустоту.
**Реализация на односвязном списке с указателем на хвост:**

**Для эффективного добавления в конец необходимо хранить два указателя:** head (начало очереди) и tail (конец очереди).

enqueue(x): Создать новый узел new_node. Если очередь пуста, установить head = tail = new_node. Иначе: установить tail.next = new_node, затем переместить tail на new_node.

dequeue(): Если очередь пуста — ошибка. Иначе: сохранить значение head.data, переместить голову на head.next. 

**Важно:** если после этого голова стала null, то и tail нужно установить в null (очередь опустела).

**Сложность операций:** enqueue, dequeue, peek, isEmpty выполняются за O(1).

### **Дек (Deque — Double-Ended Queue)**
**Дек** — это двусторонняя очередь, позволяющая добавлять и удалять элементы как в начале, так и в конце.

**Основные операции:**

pushFront(x) — добавление в начало.
pushBack(x) — добавление в конец.
popFront() — удаление из начала.
popBack() — удаление из конца.
peekFront(), peekBack() — просмотр начала/конца.

**Реализация на двусвязном списке:**

Для эффективного удаления с конца (popBack) односвязного списка недостаточно, так как у его последнего элемента нет ссылки на предыдущий. Поэтому дек оптимально реализуется на **двусвязном списке** с двумя указателями: head и tail. * **pushFront(x):** Аналогично добавлению в начало двусвязного списка. Установить связи между new_node и head. * **pushBack(x):** Аналогично добавлению в конец двусвязного списка. Установить связи между tail и new_node. * **popBack():** Если дек не пуст, переместить tail на tail.prev, отсечь старый хвост. Корректно обработать случай, когда в деке只有一个 элемент. * **Сложность операций:** Все основные операции (pushFront, pushBack, popFront, popBack) выполняются за O(1).

**Сравнение реализаций на списках и массивах**

| Критерий | Реализация на списках | Реализация на массивах (динамических) |
|:---|:---|:---|
| **Сложность операций** | `pushBack`/`popBack`, `pushFront`/`popFront` — O(1) | `pushBack`/`popBack` — O(1)*, `pushFront`/`popFront` — O(n) |
| **Память** | Больше: память на хранение указателей. | Меньше: память только на данные (но может быть избыточное выделение). |
| **Локализация данных** | Плохая: узлы в случайных местах памяти (кэш-промахи). | Отличная: данные лежат рядом (кэш-дружественность). |
| **Динамичность** | Истинно динамическая: каждый элемент выделяется отдельно. | Динамическая с резервированием: требует периодического дорогого копирования (reallocation). |


**Вывод:** Реализация стека, очереди и дека на связных списках является более универсальной и надёжной с точки зрения сложности операций, так как не требует операций копирования и расширения массива. Она гарантирует **константное время** выполнения для всех ключевых операций. Однако она проигрывает в потреблении памяти и скорости доступа из-за плохой локализации данных. Реализация на массивах (особенно для стека и очереди с кольцевой организацией) часто быстрее на практике для задач, где размер данных大致 известен, благодаря кэш-дружественности.
<!-- #endregion -->

### **Задание 1**

```python
class BaseStack:
    """Базовый класс для стека"""
    def push(self, item):
        raise NotImplementedError("Метод push должен быть реализован")
    
    def pop(self):
        raise NotImplementedError("Метод pop должен быть реализован")
    
    def peek(self):
        raise NotImplementedError("Метод peek должен быть реализован")
    
    def is_empty(self):
        raise NotImplementedError("Метод is_empty должен быть реализован")
    
    def size(self):
        raise NotImplementedError("Метод size должен быть реализован")


class BaseQueue:
    """Базовый класс для очереди"""
    def enqueue(self, item):
        raise NotImplementedError("Метод enqueue должен быть реализован")
    
    def dequeue(self):
        raise NotImplementedError("Метод dequeue должен быть реализован")
    
    def front(self):
        raise NotImplementedError("Метод front должен быть реализован")
    
    def is_empty(self):
        raise NotImplementedError("Метод is_empty должен быть реализован")
    
    def size(self):
        raise NotImplementedError("Метод size должен быть реализован")


class BaseDeque:
    """Базовый класс для дека"""
    def add_front(self, item):
        raise NotImplementedError("Метод add_front должен быть реализован")
    
    def add_rear(self, item):
        raise NotImplementedError("Метод add_rear должен быть реализован")
    
    def remove_front(self):
        raise NotImplementedError("Метод remove_front должен быть реализован")
    
    def remove_rear(self):
        raise NotImplementedError("Метод remove_rear должен быть реализован")
    
    def peek_front(self):
        raise NotImplementedError("Метод peek_front должен быть реализован")
    
    def peek_rear(self):
        raise NotImplementedError("Метод peek_rear должен быть реализован")
    
    def is_empty(self):
        raise NotImplementedError("Метод is_empty должен быть реализован")
    
    def size(self):
        raise NotImplementedError("Метод size должен быть реализован")


""" 1. Стек на основе массива"""
class ArrayStack(BaseStack):
    def __init__(self):
        self._items = []
    
    def push(self, item):
        """Добавляет элемент на вершину стека"""
        self._items.append(item)
    
    def pop(self):
        """Удаляет и возвращает элемент с вершины стека"""
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._items.pop()
    
    def peek(self):
        """Возвращает элемент с вершины стека без удаления"""
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._items[-1]
    
    def is_empty(self):
        """Проверяет, пуст ли стек"""
        return len(self._items) == 0
    
    def size(self):
        """Возвращает количество элементов в стеке"""
        return len(self._items)
    
    def __str__(self):
        return f"ArrayStack({self._items})"


""" 2. Стек на основе связного списка"""
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedListStack(BaseStack):
    def __init__(self):
        self._top = None
        self._size = 0
    
    def push(self, item):
        """Добавляет элемент на вершину стека"""
        new_node = Node(item)
        new_node.next = self._top
        self._top = new_node
        self._size += 1
    
    def pop(self):
        """Удаляет и возвращает элемент с вершины стека"""
        if self.is_empty():
            raise IndexError("Стек пуст")
        
        data = self._top.data
        self._top = self._top.next
        self._size -= 1
        return data
    
    def peek(self):
        """Возвращает элемент с вершины стека без удаления"""
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._top.data
    
    def is_empty(self):
        """Проверяет, пуст ли стек"""
        return self._top is None
    
    def size(self):
        """Возвращает количество элементов в стеке"""
        return self._size
    
    def __str__(self):
        items = []
        current = self._top
        while current:
            items.append(current.data)
            current = current.next
        return f"LinkedListStack({items})"


""" 3. Очередь на основе массива """
class ArrayQueue(BaseQueue):
    def __init__(self):
        self._items = []
    
    def enqueue(self, item):
        """Добавляет элемент в конец очереди"""
        self._items.append(item)
    
    def dequeue(self):
        """Удаляет и возвращает элемент из начала очереди"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._items.pop(0)
    
    def front(self):
        """Возвращает элемент из начала очереди без удаления"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._items[0]
    
    def is_empty(self):
        """Проверяет, пуста ли очередь"""
        return len(self._items) == 0
    
    def size(self):
        """Возвращает количество элементов в очереди"""
        return len(self._items)
    
    def __str__(self):
        return f"ArrayQueue({self._items})"


""" 4. Очередь на основе связного списка"""
class LinkedListQueue(BaseQueue):
    def __init__(self):
        self._front = None
        self._rear = None
        self._size = 0
    
    def enqueue(self, item):
        """Добавляет элемент в конец очереди"""
        new_node = Node(item)
        
        if self.is_empty():
            self._front = self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        
        self._size += 1
    
    def dequeue(self):
        """Удаляет и возвращает элемент из начала очереди"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        
        data = self._front.data
        self._front = self._front.next
        
        if self._front is None:
            self._rear = None
        
        self._size -= 1
        return data
    
    def front(self):
        """Возвращает элемент из начала очереди без удаления"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._front.data
    
    def is_empty(self):
        """Проверяет, пуста ли очередь"""
        return self._front is None
    
    def size(self):
        """Возвращает количество элементов в очереди"""
        return self._size
    
    def __str__(self):
        items = []
        current = self._front
        while current:
            items.append(current.data)
            current = current.next
        return f"LinkedListQueue({items})"


""" 5. Дек на основе массива"""
class ArrayDeque(BaseDeque):
    def __init__(self):
        self._items = []
    
    def add_front(self, item):
        """Добавляет элемент в начало дека"""
        self._items.insert(0, item)
    
    def add_rear(self, item):
        """Добавляет элемент в конец дека"""
        self._items.append(item)
    
    def remove_front(self):
        """Удаляет и возвращает элемент из начала дека"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._items.pop(0)
    
    def remove_rear(self):
        """Удаляет и возвращает элемент из конца дека"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._items.pop()
    
    def peek_front(self):
        """Возвращает элемент из начала дека без удаления"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._items[0]
    
    def peek_rear(self):
        """Возвращает элемент из конца дека без удаления"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._items[-1]
    
    def is_empty(self):
        """Проверяет, пуст ли дек"""
        return len(self._items) == 0
    
    def size(self):
        """Возвращает количество элементов в деке"""
        return len(self._items)
    
    def __str__(self):
        return f"ArrayDeque({self._items})"


""" 6. Дек на основе связного списка """
class LinkedListDeque(BaseDeque):
    def __init__(self):
        self._front = None
        self._rear = None
        self._size = 0
    
    def add_front(self, item):
        """Добавляет элемент в начало дека"""
        new_node = Node(item)
        
        if self.is_empty():
            self._front = self._rear = new_node
        else:
            new_node.next = self._front
            self._front = new_node
        
        self._size += 1
    
    def add_rear(self, item):
        """Добавляет элемент в конец дека"""
        new_node = Node(item)
        
        if self.is_empty():
            self._front = self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        
        self._size += 1
    
    def remove_front(self):
        """Удаляет и возвращает элемент из начала дека"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        
        data = self._front.data
        self._front = self._front.next
        
        if self._front is None:
            self._rear = None
        
        self._size -= 1
        return data
    
    def remove_rear(self):
        """Удаляет и возвращает элемент из конца дека"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        
        """Если в деке только один элемент"""
        if self._front == self._rear:
            data = self._front.data
            self._front = self._rear = None
            self._size -= 1
            return data
        
        """Находим предпоследний элемент"""
        current = self._front
        while current.next != self._rear:
            current = current.next
        
        data = self._rear.data
        self._rear = current
        self._rear.next = None
        self._size -= 1
        return data
    
    def peek_front(self):
        """Возвращает элемент из начала дека без удаления"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._front.data
    
    def peek_rear(self):
        """Возвращает элемент из конца дека без удаления"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._rear.data
    
    def is_empty(self):
        """Проверяет, пуст ли дек"""
        return self._front is None
    
    def size(self):
        """Возвращает количество элементов в деке"""
        return self._size
    
    def __str__(self):
        items = []
        current = self._front
        while current:
            items.append(current.data)
            current = current.next
        return f"LinkedListDeque({items})"



if __name__ == "__main__":
    print("=== ТЕСТИРОВАНИЕ СТРУКТУР ДАННЫХ ===\n")
    
    """1. Стек на массиве"""
    print("1. Тестирование ArrayStack:")
    stack1 = ArrayStack()
    
    """Тест добавления"""
    stack1.push(1)
    stack1.push(2)
    stack1.push(3)
    assert str(stack1) == "ArrayStack([1, 2, 3])", "Ошибка добавления в стек"
    
    """Тест просмотра"""
    assert stack1.peek() == 3, "Ошибка peek()"
    
    """ Тест удаления"""
    assert stack1.pop() == 3, "Ошибка pop()"
    assert stack1.size() == 2, "Ошибка размера после pop()"
    
    """Тест пустоты"""
    assert not stack1.is_empty(), "Ошибка is_empty()"
    
    """Очистка и проверка пустого стека"""
    stack1.pop()
    stack1.pop()
    assert stack1.is_empty(), "Стек должен быть пустым"
    assert stack1.size() == 0, "Размер должен быть 0"
    
    print("   ✓ Все тесты ArrayStack пройдены\n")
    
    """ 2. Стек на связном списке """
    print("2. Тестирование LinkedListStack:")
    stack2 = LinkedListStack()
    
    """Тест добавления"""
    stack2.push('a')
    stack2.push('b')
    stack2.push('c')
    assert str(stack2) == "LinkedListStack(['c', 'b', 'a'])", "Ошибка добавления в связный стек"
    
    """ Тест просмотра"""
    assert stack2.peek() == 'c', "Ошибка peek() в связном стеке"
    
    """Тест удаления """
    assert stack2.pop() == 'c', "Ошибка pop() в связном стеке"
    assert stack2.size() == 2, "Ошибка размера после pop()"
    
    print("  Все тесты LinkedListStack пройдены\n")
    
    """ 3. Очередь на массиве"""
    print("3. Тестирование ArrayQueue:")
    queue1 = ArrayQueue()
    
    """Тест добавления"""
    queue1.enqueue(10)
    queue1.enqueue(20)
    queue1.enqueue(30)
    assert str(queue1) == "ArrayQueue([10, 20, 30])", "Ошибка добавления в очередь"
    
    """Тест просмотра"""
    assert queue1.front() == 10, "Ошибка front()"
    
    """Тест удаления """
    assert queue1.dequeue() == 10, "Ошибка dequeue()"
    assert queue1.size() == 2, "Ошибка размера после dequeue()"
    assert queue1.front() == 20, "Ошибка front() после dequeue()"
    
    print("    Все тесты ArrayQueue пройдены\n")
    
    """4. Очередь на связном списке"""
    print("4. Тестирование LinkedListQueue:")
    queue2 = LinkedListQueue()
    
    """Тест добавления"""
    queue2.enqueue('x')
    queue2.enqueue('y')
    queue2.enqueue('z')
    assert str(queue2) == "LinkedListQueue(['x', 'y', 'z'])", "Ошибка добавления в связную очередь"
    
    """Тест просмотра"""
    assert queue2.front() == 'x', "Ошибка front() в связной очереди"
    
    """Tест удаления"""
    assert queue2.dequeue() == 'x', "Ошибка dequeue() в связной очереди"
    assert queue2.size() == 2, "Ошибка размера после dequeue()"
    assert queue2.front() == 'y', "Ошибка front() после dequeue()"
    
    print("  Все тесты LinkedListQueue пройдены\n")
    
    """5. Дек на массиве"""
    print("5. Тестирование ArrayDeque:")
    deque1 = ArrayDeque()
    
    """Тест добавления спереди и сзади"""
    deque1.add_front(1)
    deque1.add_rear(2)
    deque1.add_front(0)
    deque1.add_rear(3)
    assert str(deque1) == "ArrayDeque([0, 1, 2, 3])", "Ошибка добавления в дек"
    
    """Тест просмотра"""
    assert deque1.peek_front() == 0, "Ошибка peek_front()"
    assert deque1.peek_rear() == 3, "Ошибка peek_rear()"
    
    """Тест удаления"""
    assert deque1.remove_front() == 0, "Ошибка remove_front()"
    assert deque1.remove_rear() == 3, "Ошибка remove_rear()"
    assert deque1.size() == 2, "Ошибка размера после удалений"
    assert str(deque1) == "ArrayDeque([1, 2])", "Ошибка состояния дека после удалений"
    
    print("  Все тесты ArrayDeque пройдены\n")
    
    """6. Дек на связном списке"""
    print("6. Тестирование LinkedListDeque:")
    deque2 = LinkedListDeque()
    
    """Тест добавления"""
    deque2.add_front(100)
    deque2.add_rear(200)
    deque2.add_front(50)
    deque2.add_rear(300)
    assert str(deque2) == "LinkedListDeque([50, 100, 200, 300])", "Ошибка добавления в связный дек"
    
    """ Тест просмотра"""
    assert deque2.peek_front() == 50, "Ошибка peek_front() в связном деке"
    assert deque2.peek_rear() == 300, "Ошибка peek_rear() в связном деке"
    
    """Тест удаления"""
    assert deque2.remove_front() == 50, "Ошибка remove_front() в связном деке"
    assert deque2.remove_rear() == 300, "Ошибка remove_rear() в связном деке"
    assert deque2.size() == 2, "Ошибка размера после удалений"
    assert str(deque2) == "LinkedListDeque([100, 200])", "Ошибка состояния связного дека после удалений"
    
    print("  Все тесты LinkedListDeque пройдены\n")
    
    """ 7. Тестирование исключений"""
    print("7. Тестирование исключений:")
    
    """Тест пустого стека"""
    empty_stack = ArrayStack()
    try:
        empty_stack.pop()
        assert False, "Должно быть исключение при pop() пустого стека"
    except IndexError:
        pass  #Ожидаемое поведение
    
    """Тест пустой очереди"""
    empty_queue = ArrayQueue()
    try:
        empty_queue.dequeue()
        assert False, "Должно быть исключение при dequeue() пустой очереди"
    except IndexError:
        pass  #Ожидаемое поведение
    
    """Тест пустого дека"""
    empty_deque = ArrayDeque()
    try:
        empty_deque.remove_front()
        assert False, "Должно быть исключение при remove_front() пустого дека"
    except IndexError:
        pass  #Ожидаемое поведение
    
    print("   Все тесты исключений пройдены\n")
    
    print("Все структуры данных работают корректно.")
```

```python
class BaseStack:
    """Базовый класс для стека"""
    def push(self, item):
        raise NotImplementedError("Метод push должен быть реализован")
    
    def pop(self):
        raise NotImplementedError("Метод pop должен быть реализован")
    
    def peek(self):
        raise NotImplementedError("Метод peek должен быть реализован")
    
    def is_empty(self):
        raise NotImplementedError("Метод is_empty должен быть реализован")
    
    def size(self):
        raise NotImplementedError("Метод size должен быть реализован")


class BaseQueue:
    """Базовый класс для очереди"""
    def enqueue(self, item):
        raise NotImplementedError("Метод enqueue должен быть реализован")
    
    def dequeue(self):
        raise NotImplementedError("Метод dequeue должен быть реализован")
    
    def front(self):
        raise NotImplementedError("Метод front должен быть реализован")
    
    def is_empty(self):
        raise NotImplementedError("Метод is_empty должен быть реализован")
    
    def size(self):
        raise NotImplementedError("Метод size должен быть реализован")


class BaseDeque:
    """Базовый класс для дека"""
    def add_front(self, item):
        raise NotImplementedError("Метод add_front должен быть реализован")
    
    def add_rear(self, item):
        raise NotImplementedError("Метод add_rear должен быть реализован")
    
    def remove_front(self):
        raise NotImplementedError("Метод remove_front должен быть реализован")
    
    def remove_rear(self):
        raise NotImplementedError("Метод remove_rear должен быть реализован")
    
    def peek_front(self):
        raise NotImplementedError("Метод peek_front должен быть реализован")
    
    def peek_rear(self):
        raise NotImplementedError("Метод peek_rear должен быть реализован")
    
    def is_empty(self):
        raise NotImplementedError("Метод is_empty должен быть реализован")
    
    def size(self):
        raise NotImplementedError("Метод size должен быть реализован")


""" 1. Стек на основе массива"""
class ArrayStack(BaseStack):
    def __init__(self):
        self._items = []
    
    def push(self, item):
        """Добавляет элемент на вершину стека"""
        self._items.append(item)
    
    def pop(self):
        """Удаляет и возвращает элемент с вершины стека"""
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._items.pop()
    
    def peek(self):
        """Возвращает элемент с вершины стека без удаления"""
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._items[-1]
    
    def is_empty(self):
        """Проверяет, пуст ли стек"""
        return len(self._items) == 0
    
    def size(self):
        """Возвращает количество элементов в стеке"""
        return len(self._items)
    
    def __str__(self):
        return f"ArrayStack({self._items})"


""" 2. Стек на основе связного списка"""
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedListStack(BaseStack):
    def __init__(self):
        self._top = None
        self._size = 0
    
    def push(self, item):
        """Добавляет элемент на вершину стека"""
        new_node = Node(item)
        new_node.next = self._top
        self._top = new_node
        self._size += 1
    
    def pop(self):
        """Удаляет и возвращает элемент с вершины стека"""
        if self.is_empty():
            raise IndexError("Стек пуст")
        
        data = self._top.data
        self._top = self._top.next
        self._size -= 1
        return data
    
    def peek(self):
        """Возвращает элемент с вершины стека без удаления"""
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._top.data
    
    def is_empty(self):
        """Проверяет, пуст ли стек"""
        return self._top is None
    
    def size(self):
        """Возвращает количество элементов в стеке"""
        return self._size
    
    def __str__(self):
        items = []
        current = self._top
        while current:
            items.append(current.data)
            current = current.next
        return f"LinkedListStack({items})"


""" 3. Очередь на основе массива """
class ArrayQueue(BaseQueue):
    def __init__(self):
        self._items = []
    
    def enqueue(self, item):
        """Добавляет элемент в конец очереди"""
        self._items.append(item)
    
    def dequeue(self):
        """Удаляет и возвращает элемент из начала очереди"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._items.pop(0)
    
    def front(self):
        """Возвращает элемент из начала очереди без удаления"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._items[0]
    
    def is_empty(self):
        """Проверяет, пуста ли очередь"""
        return len(self._items) == 0
    
    def size(self):
        """Возвращает количество элементов в очереди"""
        return len(self._items)
    
    def __str__(self):
        return f"ArrayQueue({self._items})"


""" 4. Очередь на основе связного списка"""
class LinkedListQueue(BaseQueue):
    def __init__(self):
        self._front = None
        self._rear = None
        self._size = 0
    
    def enqueue(self, item):
        """Добавляет элемент в конец очереди"""
        new_node = Node(item)
        
        if self.is_empty():
            self._front = self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        
        self._size += 1
    
    def dequeue(self):
        """Удаляет и возвращает элемент из начала очереди"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        
        data = self._front.data
        self._front = self._front.next
        
        if self._front is None:
            self._rear = None
        
        self._size -= 1
        return data
    
    def front(self):
        """Возвращает элемент из начала очереди без удаления"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._front.data
    
    def is_empty(self):
        """Проверяет, пуста ли очередь"""
        return self._front is None
    
    def size(self):
        """Возвращает количество элементов в очереди"""
        return self._size
    
    def __str__(self):
        items = []
        current = self._front
        while current:
            items.append(current.data)
            current = current.next
        return f"LinkedListQueue({items})"


""" 5. Дек на основе массива"""
class ArrayDeque(BaseDeque):
    def __init__(self):
        self._items = []
    
    def add_front(self, item):
        """Добавляет элемент в начало дека"""
        self._items.insert(0, item)
    
    def add_rear(self, item):
        """Добавляет элемент в конец дека"""
        self._items.append(item)
    
    def remove_front(self):
        """Удаляет и возвращает элемент из начала дека"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._items.pop(0)
    
    def remove_rear(self):
        """Удаляет и возвращает элемент из конца дека"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._items.pop()
    
    def peek_front(self):
        """Возвращает элемент из начала дека без удаления"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._items[0]
    
    def peek_rear(self):
        """Возвращает элемент из конца дека без удаления"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._items[-1]
    
    def is_empty(self):
        """Проверяет, пуст ли дек"""
        return len(self._items) == 0
    
    def size(self):
        """Возвращает количество элементов в деке"""
        return len(self._items)
    
    def __str__(self):
        return f"ArrayDeque({self._items})"


""" 6. Дек на основе связного списка """
class LinkedListDeque(BaseDeque):
    def __init__(self):
        self._front = None
        self._rear = None
        self._size = 0
    
    def add_front(self, item):
        """Добавляет элемент в начало дека"""
        new_node = Node(item)
        
        if self.is_empty():
            self._front = self._rear = new_node
        else:
            new_node.next = self._front
            self._front = new_node
        
        self._size += 1
    
    def add_rear(self, item):
        """Добавляет элемент в конец дека"""
        new_node = Node(item)
        
        if self.is_empty():
            self._front = self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        
        self._size += 1
    
    def remove_front(self):
        """Удаляет и возвращает элемент из начала дека"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        
        data = self._front.data
        self._front = self._front.next
        
        if self._front is None:
            self._rear = None
        
        self._size -= 1
        return data
    
    def remove_rear(self):
        """Удаляет и возвращает элемент из конца дека"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        
        """Если в деке только один элемент"""
        if self._front == self._rear:
            data = self._front.data
            self._front = self._rear = None
            self._size -= 1
            return data
        
        """Находим предпоследний элемент"""
        current = self._front
        while current.next != self._rear:
            current = current.next
        
        data = self._rear.data
        self._rear = current
        self._rear.next = None
        self._size -= 1
        return data
    
    def peek_front(self):
        """Возвращает элемент из начала дека без удаления"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._front.data
    
    def peek_rear(self):
        """Возвращает элемент из конца дека без удаления"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self._rear.data
    
    def is_empty(self):
        """Проверяет, пуст ли дек"""
        return self._front is None
    
    def size(self):
        """Возвращает количество элементов в деке"""
        return self._size
    
    def __str__(self):
        items = []
        current = self._front
        while current:
            items.append(current.data)
            current = current.next
        return f"LinkedListDeque({items})"



if __name__ == "__main__":
    print("=== ТЕСТИРОВАНИЕ СТРУКТУР ДАННЫХ ===\n")
    
    """1. Стек на массиве"""
    print("1. Тестирование ArrayStack:")
    stack1 = ArrayStack()
    
    """Тест добавления"""
    stack1.push(1)
    stack1.push(2)
    stack1.push(3)
    assert str(stack1) == "ArrayStack([1, 2, 3])", "Ошибка добавления в стек"
    
    """Тест просмотра"""
    assert stack1.peek() == 3, "Ошибка peek()"
    
    """ Тест удаления"""
    assert stack1.pop() == 3, "Ошибка pop()"
    assert stack1.size() == 2, "Ошибка размера после pop()"
    
    """Тест пустоты"""
    assert not stack1.is_empty(), "Ошибка is_empty()"
    
    """Очистка и проверка пустого стека"""
    stack1.pop()
    stack1.pop()
    assert stack1.is_empty(), "Стек должен быть пустым"
    assert stack1.size() == 0, "Размер должен быть 0"
    
    print("   ✓ Все тесты ArrayStack пройдены\n")
    
    """ 2. Стек на связном списке """
    print("2. Тестирование LinkedListStack:")
    stack2 = LinkedListStack()
    
    """Тест добавления"""
    stack2.push('a')
    stack2.push('b')
    stack2.push('c')
    assert str(stack2) == "LinkedListStack(['c', 'b', 'a'])", "Ошибка добавления в связный стек"
    
    """ Тест просмотра"""
    assert stack2.peek() == 'c', "Ошибка peek() в связном стеке"
    
    """Тест удаления """
    assert stack2.pop() == 'c', "Ошибка pop() в связном стеке"
    assert stack2.size() == 2, "Ошибка размера после pop()"
    
    print("  Все тесты LinkedListStack пройдены\n")
    
    """ 3. Очередь на массиве"""
    print("3. Тестирование ArrayQueue:")
    queue1 = ArrayQueue()
    
    """Тест добавления"""
    queue1.enqueue(10)
    queue1.enqueue(20)
    queue1.enqueue(30)
    assert str(queue1) == "ArrayQueue([10, 20, 30])", "Ошибка добавления в очередь"
    
    """Тест просмотра"""
    assert queue1.front() == 10, "Ошибка front()"
    
    """Тест удаления """
    assert queue1.dequeue() == 10, "Ошибка dequeue()"
    assert queue1.size() == 2, "Ошибка размера после dequeue()"
    assert queue1.front() == 20, "Ошибка front() после dequeue()"
    
    print("    Все тесты ArrayQueue пройдены\n")
    
    """4. Очередь на связном списке"""
    print("4. Тестирование LinkedListQueue:")
    queue2 = LinkedListQueue()
    
    """Тест добавления"""
    queue2.enqueue('x')
    queue2.enqueue('y')
    queue2.enqueue('z')
    assert str(queue2) == "LinkedListQueue(['x', 'y', 'z'])", "Ошибка добавления в связную очередь"
    
    """Тест просмотра"""
    assert queue2.front() == 'x', "Ошибка front() в связной очереди"
    
    """Tест удаления"""
    assert queue2.dequeue() == 'x', "Ошибка dequeue() в связной очереди"
    assert queue2.size() == 2, "Ошибка размера после dequeue()"
    assert queue2.front() == 'y', "Ошибка front() после dequeue()"
    
    print("  Все тесты LinkedListQueue пройдены\n")
    
    """5. Дек на массиве"""
    print("5. Тестирование ArrayDeque:")
    deque1 = ArrayDeque()
    
    """Тест добавления спереди и сзади"""
    deque1.add_front(1)
    deque1.add_rear(2)
    deque1.add_front(0)
    deque1.add_rear(3)
    assert str(deque1) == "ArrayDeque([0, 1, 2, 3])", "Ошибка добавления в дек"
    
    """Тест просмотра"""
    assert deque1.peek_front() == 0, "Ошибка peek_front()"
    assert deque1.peek_rear() == 3, "Ошибка peek_rear()"
    
    """Тест удаления"""
    assert deque1.remove_front() == 0, "Ошибка remove_front()"
    assert deque1.remove_rear() == 3, "Ошибка remove_rear()"
    assert deque1.size() == 2, "Ошибка размера после удалений"
    assert str(deque1) == "ArrayDeque([1, 2])", "Ошибка состояния дека после удалений"
    
    print("  Все тесты ArrayDeque пройдены\n")
    
    """6. Дек на связном списке"""
    print("6. Тестирование LinkedListDeque:")
    deque2 = LinkedListDeque()
    
    """Тест добавления"""
    deque2.add_front(100)
    deque2.add_rear(200)
    deque2.add_front(50)
    deque2.add_rear(300)
    assert str(deque2) == "LinkedListDeque([50, 100, 200, 300])", "Ошибка добавления в связный дек"
    
    """ Тест просмотра"""
    assert deque2.peek_front() == 50, "Ошибка peek_front() в связном деке"
    assert deque2.peek_rear() == 300, "Ошибка peek_rear() в связном деке"
    
    """Тест удаления"""
    assert deque2.remove_front() == 50, "Ошибка remove_front() в связном деке"
    assert deque2.remove_rear() == 300, "Ошибка remove_rear() в связном деке"
    assert deque2.size() == 2, "Ошибка размера после удалений"
    assert str(deque2) == "LinkedListDeque([100, 200])", "Ошибка состояния связного дека после удалений"
    
    print("  Все тесты LinkedListDeque пройдены\n")
    
    """ 7. Тестирование исключений"""
    print("7. Тестирование исключений:")
    
    """Тест пустого стека"""
    empty_stack = ArrayStack()
    try:
        empty_stack.pop()
        assert False, "Должно быть исключение при pop() пустого стека"
    except IndexError:
        pass  #Ожидаемое поведение
    
    """Тест пустой очереди"""
    empty_queue = ArrayQueue()
    try:
        empty_queue.dequeue()
        assert False, "Должно быть исключение при dequeue() пустой очереди"
    except IndexError:
        pass  #Ожидаемое поведение
    
    """Тест пустого дека"""
    empty_deque = ArrayDeque()
    try:
        empty_deque.remove_front()
        assert False, "Должно быть исключение при remove_front() пустого дека"
    except IndexError:
        pass  #Ожидаемое поведение
    
    print("   Все тесты исключений пройдены\n")
    
    print("Все структуры данных работают корректно.")
```

### Сводная таблица временной сложности операций

| Структура | Добавление | Удаление | Просмотр | Пустота | Размер |
|-----------|------------|----------|----------|---------|--------|
| **ArrayStack** | O(1)* | O(1) | O(1) | O(1) | O(1) |
| **LinkedListStack** | O(1) | O(1) | O(1) | O(1) | O(1) |
| **ArrayQueue** | O(1)* | O(n) | O(1) | O(1) | O(1) |
| **LinkedListQueue** | O(1) | O(1) | O(1) | O(1) | O(1) |
| **ArrayDeque** | O(n)/O(1)* | O(n)/O(1) | O(1) | O(1) | O(1) |
| **LinkedListDeque** | O(1)/O(1) | O(1)/O(n) | O(1) | O(1) | O(1) |

### Условные обозначения:

- **\*** - амортизированная сложность
- **Для деков** - сложность указана в формате **спереди/сзади**
  - ArrayDeque: add_front/remove_front **O(n)**, add_rear/remove_rear **O(1)**
  - LinkedListDeque: add_front/remove_front **O(1)**, add_rear **O(1)**, remove_rear **O(n)**

### Ключевые выводы:

1. **Стеки** эффективны в обеих реализациях
2. **Очереди** лучше реализовывать на связных списках
3. **Деки** имеют компромиссы в зависимости от реализации
4. Все структуры имеют O(1) для проверки пустоты и размера


### **Задание 2**

```python
def check_brackets(bracket_string):
    """
    Проверяет своевременность закрытия скобок в строке символов
    """
    stack = []
    bracket_pairs = {')': '(', ']': '[', '}': '{'}
    
    for char in bracket_string:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack:
                return False
            if stack[-1] == bracket_pairs[char]:
                stack.pop()
            else:
                return False
    
    return len(stack) == 0


def run_tests():
    """Запуск 5 тестов"""
    tests = [
        
        ("()", True, "Простые круглые скобки"),
        
        ("()[]{}", True, "Разные типы скобок"),
        
        ("([{}])", True, "Вложенные скобки"),
        
        ("(()", False, "Незакрытая круглая скобка"),
        
        ("([)]", False, "Неправильный порядок скобок")
    ]
    
    print("ТЕСТИРОВАНИЕ ПРОВЕРКИ СКОБОК")
    print("=" * 40)
    
    for i, (test_string, expected, description) in enumerate(tests, 1):
        result = check_brackets(test_string)
        status = " ПРОЙДЕН" if result == expected else " ОШИБКА"
        
        print(f"Тест {i}: {description}")
        print(f"Строка: '{test_string}'")
        print(f"Результат: {result} (ожидалось: {expected})")
        print(f"Статус: {status}")
        print("-" * 40)


def main():
    run_tests()


if __name__ == "__main__":
    main()
```

### Анализ сложности алгоритма проверки скобок

### Детализация операций

| Операция | Сложность | Примечания |
|----------|-----------|------------|
| Создание stack | O(1) | Инициализация пустого списка |
| Создание bracket_pairs | O(1) | Словарь фиксированного размера |
| Цикл for | O(n) | Проход по всем n символам |
| Проверка `char in '([{'` | O(1) | Поиск в строке длины 3 |
| stack.append() | O(1)* | Амортизированная константа |
| stack.pop() | O(1) | Удаление с конца |
| stack[-1] | O(1) | Доступ к последнему элементу |
| bracket_pairs[char] | O(1) | Поиск в словаре |
| len(stack) == 0 | O(1) | Проверка длины списка |

### Пространственная сложность: O(n)

- **В худшем случае** (только открывающие скобки): стек может содержать до **n** элементов
- **Словарь bracket_pairs**: занимает O(1) памяти (фиксированный размер)

### Анализ случаев

### Худший случай
**Строка**: `"((((((((("`
- **Время**: O(n)
- **Память**: O(n)

### Лучший случай
**Строка**: `")"`
- **Время**: O(1) - досрочный выход
- **Память**: O(1)

### Средний случай
**Сбалансированная строка скобок**
- **Время**: O(n)
- **Память**: O(n/2) ≈ O(n)

### Итоговая таблица сложности

| Метрика | Сложность | Обоснование |
|---------|-----------|-------------|
| **Временная** | O(n) | Один проход по строке длиной n |
| **Пространственная** | O(n) | В худшем случае стек размером n |
| **Лучший случай** | O(1) | Некорректная скобка в начале |
| **Худший случай** | O(n) | Все скобки открывающие |

### Вывод

Алгоритм оптимален для данной задачи, так как требует только одного прохода по строке и минимальной дополнительной памяти.

*Примечание: * - амортизированная константная сложность*


### **Задание 3**

```python
def evaluate_postfix(expression):
    """
    Вычисляет значение выражения в обратной польской записи
    """
    stack = []
    operators = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y
    }
    
    for char in expression.split():
        if char.isdigit():
            stack.append(int(char))
        elif char in operators:
            if len(stack) < 2:
                raise ValueError(f"Недостаточно операндов для операции '{char}'")
            
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = operators[char](operand1, operand2)
            stack.append(result)
        else:
            raise ValueError(f"Недопустимый символ: '{char}'")
    
    if len(stack) != 1:
        raise ValueError(f"Некорректное выражение. В стеке осталось {len(stack)} элементов: {stack}")
    
    return stack[0]


def run_five_tests():
    """Запуск 5 тестов """
    tests = [
       
        ("2 3 +", 5, "Простое сложение: 2 + 3"),
        
        ("3 4 2 * +", 11, "Умножение и сложение: 3 + 4*2"),
        
        ("5 1 2 + 4 * +", 17, "Сложное выражение: 5 + (1+2)*4"),
        
        ("8 4 - 2 /", 2, "Вычитание и деление: (8-4)/2"),
        
        ("9 3 / 1 1 + *", 6, "Множественные операции: (9/3)*(1+1)")
    ]
    
    print("5 ТЕСТОВ ВЫЧИСЛЕНИЕ ОБРАТНОЙ ПОЛЬСКОЙ ЗАПИСИ")
    print("=" * 60)
    
    for i, (expression, expected, description) in enumerate(tests, 1):
        result = evaluate_postfix(expression)
        assert result == expected, f"Тест {i} не пройден: {description}. Ожидалось {expected}, получено {result}"
        print(f"Тест {i} ПРОЙДЕН: {description}")
        print(f"   Выражение: '{expression}' = {result}")
    


def main():
    """Основная функция"""
    run_five_tests()


if __name__ == "__main__":
    main()
```

### Анализ сложности алгоритма вычисления обратной польской записи

### Детализация операций

| Операция | Сложность | Примечания |
|----------|-----------|------------|
| `expression.split()` | O(m) | m - длина строки выражения |
| Цикл for | O(n) | Проход по n токенам |
| `char.isdigit()` | O(1) | Проверка строки на цифры |
| `stack.append()` | O(1)* | Амортизированная константа |
| `stack.pop()` | O(1) | Удаление с конца |
| `char in operators` | O(1) | Поиск в словаре из 4 элементов |
| `operators[char]()` | O(1) | Вызов лямбда-функции |
| `len(stack)` | O(1) | Проверка длины списка |
| `int(char)` | O(1) | Конвертация строки в число |

### Пространственная сложность: O(n)

- **Стек**: в худшем случае может содержать до n/2 элементов ≈ O(n)
- **Словарь operators**: O(1) - фиксированный размер
- **Временные переменные**: O(1)

### Анализ случаев

### Худший случай
**Выражение**: `"1 2 3 4 5 6 7 8 9 10 + + + + + + + + +"`
- **Время**: O(n) - все операции в конце
- **Память**: O(n) - стек растет линейно

### Лучший случай
**Выражение**: `"2 3 +"`
- **Время**: O(n) - минимальное выражение
- **Память**: O(1) - мало элементов в стеке

### Средний случай
**Сбалансированное выражение**
- **Время**: O(n)
- **Память**: O(n/2) ≈ O(n)

### Итоговая таблица сложности

| Метрика | Сложность | Обоснование |
|---------|-----------|-------------|
| **Временная** | O(n) | Один проход по n токенам |
| **Пространственная** | O(n) | Стек в худшем случае O(n) |
| **Лучший случай** | O(n) | Минимальное выражение |
| **Худший случай** | O(n) | Все операнды сначала, операции потом |
| **Split операция** | O(m) | m - длина исходной строки |

### Вывод

Алгоритм оптимален для вычисления обратной польской записи. Временная сложность линейна относительно количества токенов, что является наилучшим возможным результатом для данной задачи.

*Примечание: n - количество токенов в выражении после split(), m - длина исходной строки выражения*


### **Задание 4**

```python
def infix_to_postfix(expression):
    """
    Переводит математическое выражение из инфиксной в постфиксную форму
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = []
    output = []
    
    for token in expression:
        if token.isalnum():  
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  
        else:  
            while (stack and stack[-1] != '(' and 
                   precedence.get(token, 0) <= precedence.get(stack[-1], 0)):
                output.append(stack.pop())
            stack.append(token)
    
    while stack:
        output.append(stack.pop())
    
    return ' '.join(output)


def run_five_tests():
    """Запуск 5 тестов перевода из инфиксной в постфиксную форму """
    print("5 ТЕСТОВ ПЕРЕВОДА ИНФИКС → ПОСТФИКС (")
    print("=" * 50)
    
    try:
        result = infix_to_postfix("a+b")
        assert result == "a b +", f"Ожидалось 'a b +', получено '{result}'"
        print(" Тест 1 ПРОЙДЕН: Простое сложение")
        print(f"  a+b → {result}")
    except AssertionError as e:
        print(f" Тест 1 ОШИБКА: {e}")
    
    try:
        result = infix_to_postfix("a+b*c")
        assert result == "a b c * +", f"Ожидалось 'a b c * +', получено '{result}'"
        print(" Тест 2 ПРОЙДЕН: Приоритет умножения")
        print(f"  a+b*c → {result}")
    except AssertionError as e:
        print(f" Тест 2 ОШИБКА: {e}")
    
    try:
        result = infix_to_postfix("(a+b)*c")
        assert result == "a b + c *", f"Ожидалось 'a b + c *', получено '{result}'"
        print(" Тест 3 ПРОЙДЕН: Сложение в скобках с умножением")
        print(f"  (a+b)*c → {result}")
    except AssertionError as e:
        print(f" Тест 3 ОШИБКА: {e}")
    
    try:
        result = infix_to_postfix("a+(b+c)*d")
        assert result == "a b c + d * +", f"Ожидалось 'a b c + d * +', получено '{result}'"
        print(" Тест 4 ПРОЙДЕН: Сложное выражение со скобками")
        print(f"  a+(b+c)*d → {result}")
    except AssertionError as e:
        print(f" Тест 4 ОШИБКА: {e}")
    
    try:
        result = infix_to_postfix("a*b+c*d")
        assert result == "a b * c d * +", f"Ожидалось 'a b * c d * +', получено '{result}'"
        print(" Тест 5 ПРОЙДЕН: Множественное умножение и сложение")
        print(f"  a*b+c*d → {result}")
    except AssertionError as e:
        print(f" Тест 5 ОШИБКА: {e}")
    
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")


def main():
    """Основная функция"""
    run_five_tests()


if __name__ == "__main__":
    main()
```

### Анализ сложности алгоритма преобразования инфикс → постфикс

### Детализация операций

| Операция | Сложность | Примечания |
|----------|-----------|------------|
| Инициализация структур | O(1) | Словарь, два списка |
| Цикл for по expression | O(n) | n символов в выражении |
| `token.isalnum()` | O(1) | Проверка одного символа |
| `output.append()` | O(1)* | Амортизированная константа |
| `stack.append()` | O(1)* | Амортизированная константа |
| `stack.pop()` | O(1) | Удаление с конца |
| `stack[-1]` | O(1) | Доступ к вершине стека |
| `precedence.get()` | O(1) | Поиск в словаре из 4 элементов |
| Вложенные while циклы | O(n) | Суммарно O(n) операций |
| `' '.join(output)` | O(n) | Объединение n элементов |

### Пространственная сложность: O(n)

- **output**: O(n) - содержит все токены выражения  
- **stack**: O(n) - в худшем случае все операторы в стеке
- **precedence**: O(1) - фиксированный словарь

### Анализ случаев

### Худший случай
**Выражение**: `"a+b*c-d/e*f+g"`
- **Время**: O(n)
- **Память**: O(n)

### Лучший случай
**Выражение**: `"a"`
- **Время**: O(n)
- **Память**: O(1)

### Средний случай
**Сбалансированное выражение**
- **Время**: O(n)
- **Память**: O(n)

### Итоговая таблица сложности

| Метрика | Сложность | Обоснование |
|---------|-----------|-------------|
| **Временная** | O(n) | Линейный проход + амортизированные операции |
| **Пространственная** | O(n) | Выходной список и стек O(n) |
| **Лучший случай** | O(n) | Минимальное выражение |
| **Худший случай** | O(n) | Сложное выражение с приоритетами |

### Вывод

Алгоритм Шантинг-ярда оптимален для преобразования инфиксной в постфиксную запись с линейной временной и пространственной сложностью O(n).

<!-- #region -->
### Контрольные вопросы

#### 1. Определение стека и принцип LIFO
**Стек** - это абстрактный тип данных, представляющий коллекцию элементов с ограниченным доступом.  
**Принцип LIFO** (Last-In, First-Out) - последний добавленный элемент извлекается первым.

#### 2. Определение очереди и принцип FIFO
**Очередь** - это абстрактный тип данных, представляющий упорядоченную коллекцию элементов.  
**Принцип FIFO** (First-In, First-Out) - первый добавленный элемент извлекается первым.

#### 3. Определение дека и его отличие
**Дек** (double-ended queue) - это двусторонняя очередь, позволяющая добавлять и удалять элементы с обоих концов.  
**Отличие**: Дек обобщает возможности стека и очереди, предоставляя операции работы с обоими концами.

#### 4. Основные операции АТД
**Стек**:
- `push` - добавление на вершину
- `pop` - удаление с вершины  
- `peek` - просмотр вершины
- `isEmpty` - проверка на пустоту

**Очередь**:
- `enqueue` - добавление в конец
- `dequeue` - удаление из начала
- `peek` - просмотр начала
- `isEmpty` - проверка на пустоту

**Дек**:
- `pushFront` - добавление в начало
- `pushBack` - добавление в конец
- `popFront` - удаление из начала
- `popBack` - удаление из конца
- `peekFront` - просмотр начала
- `peekBack` - просмотр конца
- `isEmpty` - проверка на пустоту

#### 5. Односвязный список для стека
Односвязный список идеально подходит, потому что все операции стека выполняются с одного конца.  
**Голова списка** становится вершиной стека, что позволяет выполнять операции за O(1).

#### 6. Алгоритм push для стека на списке

1. Создать новый узел с данными
2. Установить next нового узла = текущая голова
3. Назначить голову = новый узел

#### 7.Алгоритм pop для стека на списке
 


1. Если стек пуст (head == null) → ошибка
2. Сохранить текущую голову во временной переменной
3. Назначить голову = head.next
4. Вернуть данные из сохраненного узла
#### 8. Необходимость двух указателей для очереди
Хранить head и tail необходимо для эффективного добавления в конец.
Если хранить только head: операция enqueue будет O(n), так как потребуется проход по всему списку до последнего элемента.

#### 9. Алгоритм enqueue для очереди с tail
pseudocode
1. Создать новый узел с данными
2. Если очередь пуста (head == null):
   - head = новый узел
   - tail = новый узел
3. Иначе:
   - tail.next = новый узел
   - tail = новый узел
#### 10. Алгоритм dequeue и важность проверки
pseudocode
1. Если очередь пуста (head == null) → ошибка
2. Сохранить текущий head во временной переменной
3. Назначить head = head.next
4. Если head == null (очередь стала пустой):
   - tail = null
5. Вернуть данные из сохраненного узла
Важность проверки: если не обновить tail при опустошении очереди, он будет указывать на удаленный узел.

#### 11. Двусвязный список для дека
Двусвязный список позволяет эффективно удалять элементы с конца за O(1). В односвязном списке popBack требует O(n) для нахождения предпоследнего элемента.

#### 12. Алгоритм popBack для дека
pseudocode
1. Если дек пуст (tail == null) → ошибка
2. Сохранить текущий tail во временной переменной
3. Назначить tail = tail.prev
4. Если tail == null (остался один элемент):
   - head = null
5. Иначе:
   - tail.next = null
6. Вернуть данные из сохраненного узла
#### 13. Преимущества и недостатки стека на массиве
Преимущества:

Лучшая локальность кэша

Меньше накладных расходов памяти

Недостатки:

Возможная реаллокация с сложностью O(n)

Ограниченный размер (если не динамический)

#### 14. Кольцевой буфер для очереди
Кольцевой буфер - массив, в котором начало и конец замыкаются в кольцо. Позволяет эффективно использовать память и реализовать очередь с O(1) операциями без сдвигов элементов.

#### 15. Сложность операций дека на массиве
pushFront и popFront имеют сложность O(n) на обычном массиве, потому что требуют сдвига всех элементов для освобождения/заполнения позиции в начале.

#### 16. Таблица асимптотической сложности
| Операция | Стек (список) | Очередь (список) | Дек (двусвязный список) | Дек (массив*) |
|----------|---------------|------------------|-------------------------|---------------|
| push/enqueue/pushBack | O(1) | O(1) | O(1) | O(1) |
| pop/dequeue/popBack | O(1) | O(1) | O(1) | O(1) |
| pushFront | O(n) | O(1) | O(1) | O(1) |
| popFront | O(n) | O(1) | O(1) | O(1) |
| peek | O(1) | O(1) | O(1) | O(1) |
| isEmpty | O(1) | O(1) | O(1) | O(1) |
*Амортизированная сложность(Идея — усреднить стоимость более «дорогих» операций по всей последовательности, чтобы средняя стоимость каждой операции оставалась постоянной или ниже.)

#### 17. Константная сложность операций дека
Все операции дека на двусвязном списке имеют O(1), потому что:

Доступ к обоим концам через head и tail

Обновление связей происходит за константное время

Не требуется проход по списку

#### 18. Примеры использования стека
Стек вызовов функций

Проверка скобочных последовательностей

Алгоритм обхода в глубину (DFS)

#### 19. Примеры использования очереди
Очередь печати

Очередь задач в процессоре

Алгоритм обхода в ширину (BFS)

#### 20. Пример использования дека
Система истории браузера:

pushBack - добавление новой страницы

popBack - кнопка "Назад"

pushFront - кнопка "Вперед" (при возврате)

#### 21. Проверка скобочной последовательности

1. Создать пустой стек
2. Для каждого символа в строке:
   - Если открывающая скобка → push в стек
   - Если закрывающая скобка:
     * Если стек пуст → ошибка
     * Если pop из стека ≠ парная скобка → ошибка
3. Если стек не пуст → ошибка
#### 22. Роль очереди в BFS
Очередь хранит вершины для обработки в порядке увеличения расстояния от стартовой вершины, обеспечивая обход "слоями".

#### 23. Порядок извлечения из стека
Операции: push(1), push(2), pop(), push(3), push(4), pop(), pop()
Порядок извлечения: 2, 4, 3

#### 24. Порядок извлечения из очереди
Операции: enqueue(1), enqueue(2), dequeue(), enqueue(3), enqueue(4), dequeue(), dequeue()
Порядок извлечения: 1, 2, 3

#### 25. Ошибка без обновления tail
Если при dequeue не обновлять tail при опустошении очереди, tail продолжит указывать на удаленный узел, что приведет к ошибкам при последующих операциях.

#### 26. Сложность push в стеке на массиве
В худшем случае O(n) из-за реаллокации, когда массив заполнен и требуется:

Выделение нового массива

Копирование всех элементов

#### 27. Преимущества по памяти
Массив: меньше накладных расходов, нет указателей
Список: гибкое использование памяти, нет фрагментации

#### 28. Критерии выбора реализации
Списки предпочтительнее когда:

Неизвестен максимальный размер

Важна предсказуемость операций

Частое изменение размера

Массивы предпочтительнее когда:

Известен максимальный размер

Важна производительность и локальность кэша

Память ограничена
<!-- #endregion -->

```python

```
