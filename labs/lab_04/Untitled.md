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

## Лаборатрная работа №4 
Цели:
- Познакомиться со структурами данных стек, очередь и дек, понять, как они устроены и работают.
- Научиться реализовывать эти структуры на основе массивов и связных списков.
- Изучить основные операции для каждой структуры (добавление, удаление, просмотр элементов).
- На практике применить стек для решения задач: проверка правильности скобок и вычисление выражений в обратной польской записи.
- Освоить перевод математических выражений из обычной записи в постфиксную форму.
### Базовые классы:

```python
class Stack:
    """Базовый класс стека"""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def pop(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def peek(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def is_empty(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def size(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")

class Queue:
    """Базовый класс очереди"""
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def dequeue(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def front(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def is_empty(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def size(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")

class Deque:
    """Базовый класс дека с методами по ТЗ"""
    def __init__(self):
        self.items = []
    
    def insert_left(self, value):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def insert_right(self, value):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def remove_left(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def remove_right(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def get_left(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def get_right(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def is_empty(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
    
    def size(self):
        raise NotImplementedError("Метод должен быть реализован в подклассе")
```

### Задание 1
1. Реализовать стек на основе массива

```python
class ArrayStack(Stack):
    def __init__(self):
        super().__init__()
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self.items.pop()
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self.items[-1]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def __str__(self):
        return f"ArrayStack({self.items})"
```

2. Реализовать стек на основе связного списка.

```python
class Node:
    """Узел связного списка"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListStack(Stack):
    def __init__(self):
        super().__init__()
        self.head = None
        self._size = 0
    
    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Стек пуст")
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return data
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self.head.data
    
    def is_empty(self):
        return self.head is None
    
    def size(self):
        return self._size
    
    def __str__(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return f"LinkedListStack({items})"
```

3. Реализовать очередь на основе массива.

```python
class ArrayQueue(Queue):
    def __init__(self):
        super().__init__()
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self.items.pop(0)
    
    def front(self):
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self.items[0]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def __str__(self):
        return f"ArrayQueue({self.items})"
```

4. Реализовать очередь на основе связного списка.

```python
class LinkedListQueue(Queue):
    def __init__(self):
        super().__init__()
        self.head = None
        self.tail = None
        self._size = 0
    
    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Очередь пуста")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return data
    
    def front(self):
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self.head.data
    
    def is_empty(self):
        return self.head is None
    
    def size(self):
        return self._size
    
    def __str__(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return f"LinkedListQueue({items})"
```

5. Реализовать дек на основе массива.

```python
class ArrayDeque(Deque):
    """Дек на основе массива"""
    def __init__(self):
        super().__init__()
        self.items = []
    
    def insert_left(self, value):
        """Помещает объект на левый конец дека"""
        self.items.insert(0, value)
    
    def insert_right(self, value):
        """Помещает объект на правый конец дека"""
        self.items.append(value)
    
    def remove_left(self):
        """Удаляет первый объект с левого конца дека и возвращает его"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self.items.pop(0)
    
    def remove_right(self):
        """Удаляет первый объект с правого конца дека и возвращает его"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self.items.pop()
    
    def get_left(self):
        """Возвращает первый объект с левого конца дека не удаляя его"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self.items[0]
    
    def get_right(self):
        """Возвращает первый объект с правого конца дека не удаляя его"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self.items[-1]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def __str__(self):
        return f"ArrayDeque({self.items})"
```

6. Реализовать дек на основе связного списка.

```python
class LinkedListDeque(Deque):
    """Дек на основе связного списка с методами по ТЗ"""
    def __init__(self):
        super().__init__()
        self.head = None
        self.tail = None
        self._size = 0
    
    def insert_left(self, value):
        """Помещает объект на левый конец дека"""
        new_node = DoublyNode(value)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1
    
    def insert_right(self, value):
        """Помещает объект на правый конец дека"""
        new_node = DoublyNode(value)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
    
    def remove_left(self):
        """Удаляет первый объект с левого конца дека и возвращает его"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        data = self.head.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self._size -= 1
        return data
    
    def remove_right(self):
        """Удаляет первый объект с правого конца дека и возвращает его"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        data = self.tail.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self._size -= 1
        return data
    
    def get_left(self):
        """Возвращает первый объект с левого конца дека не удаляя его"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self.head.data
    
    def get_right(self):
        """Возвращает первый объект с правого конца дека не удаляя его"""
        if self.is_empty():
            raise IndexError("Дек пуст")
        return self.tail.data
    
    def is_empty(self):
        return self.head is None
    
    def size(self):
        return self._size
    
    def __str__(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return f"LinkedListDeque({items})"
```

### Задание 2
Используя операции со стеком, написать программу, проверяющую своевременность закрытия скобок «(, ), [, ] ,{, }» в строке символов (строка состоит из одних скобок этих типов).

В процессе решения анализируются символы строки. Если встречена одна из открывающихся скобок, то она записывается в стек. При обнаружении закрывающейся скобки, соответствующей скобке, находящейся в вершине стека, последняя удаляется. При несоответствии скобки выдается сообщение об ошибке, которое фиксируется в логической переменной.

```python
def check_brackets(expression):
    """
    Проверяет корректность расстановки скобок в выражении
    Возвращает True если скобки расставлены правильно, False в противном случае
    """
    stack = ArrayStack()
    brackets = {'(': ')', '[': ']', '{': '}'}
    
    for char in expression:
        if char in brackets.keys(): 
            stack.push(char)
        elif char in brackets.values():
            if stack.is_empty():
                return False
            opening_bracket = stack.pop()
            if brackets[opening_bracket] != char:
                return False
    
    return stack.is_empty()

def test_bracket_checker():
    test_cases = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
        ("((()))", True),
        ("((())", False),
        ("", True)
    ]
    
    print("Тестирование проверки скобочной последовательности:")
    print("=" * 55)
    print(f"{'Выражение':<15} {'Результат':<10} {'Ожидалось':<10} {'Статус':<6}")
    print("-" * 55)
    
    for expr, expected in test_cases:
        result = check_brackets(expr)
        status = "✓" if result == expected else "✗"
        print(f"{expr:<15} {str(result):<10} {str(expected):<10} {status:<6}")
    
    print("=" * 55)

test_bracket_checker()
```

### Задание 3

Написать программу вычисления значения выражения, представленного в обратной польской записи (в постфиксной записи). Выражение состоит из цифр от 1 до 9 и знаков операции.

| Обычная (инфиксная) запись | Обратная польская (постфиксная) запись |
|:---|:---|
| (a+b) * c    | a b + c *       |
|  a + (b+c)*d | a b c + d * +   |

Просматривая строку, анализируем очередной символ, если это:
 - цифра, то записываем ее в стек;
 - знак, то читаем два элемента из стека, выполняем математическую операцию, определяемую этим знаком, и заносим результат в стек.

После просмотра всей строки в стеке должен оставаться один элемент, он и является решением задачи.

```python
def evaluate_rpn(expression):
    """
    Вычисляет значение выражения в обратной польской записи
    """
    stack = ArrayStack()
    operators = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y
    }
    
    for token in expression.split():
        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            stack.push(float(token))
        elif token in operators:
            if stack.size() < 2:
                raise ValueError("Недостаточно операндов для операции")
            y = stack.pop()
            x = stack.pop()
            result = operators[token](x, y)
            stack.push(result)
        else:
            raise ValueError(f"Неизвестный токен: {token}")
    
    if stack.size() != 1:
        raise ValueError("Некорректное выражение")
    
    return stack.pop()

def test_rpn_evaluator():
    test_cases = [
        ("3 4 +", 7),
        ("5 2 * 3 +", 13),
        ("10 5 / 2 *", 4),
        ("4 2 + 3 * 6 -", 12),
        ("1 2 + 4 * 3 +", 15)
    ]
    
    print("Тестирование вычисления RPN выражений:")
    print("-" * 50)
    for expr, expected in test_cases:
        result = evaluate_rpn(expr)
        status = "Правильно" if abs(result - expected) < 1e-9 else "Не правиильно"
        print(f"{status} '{expr}' = {result} (ожидалось: {expected})")
    print()

test_rpn_evaluator()
```

### Задание 4
Реализовать перевод математических выражений из инфиксной в постфиксную форму записи.

```python
def infix_to_postfix(expression):
    """
    Переводит инфиксное выражение в постфиксную запись (обратную польскую)
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    
    output = []
    stack = ArrayStack()
    
    for token in expression.split():
        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            output.append(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                output.append(stack.pop())
            stack.pop()  
        elif token in precedence:
            while (not stack.is_empty() and 
                   stack.peek() != '(' and 
                   precedence.get(stack.peek(), 0) >= precedence[token]):
                output.append(stack.pop())
            stack.push(token)
    
    while not stack.is_empty():
        output.append(stack.pop())
    
    return ' '.join(output)

def test_infix_to_postfix():
    test_cases = [
        ("3 + 4", "3 4 +"),
        ("3 + 4 * 2", "3 4 2 * +"),
        ("( 3 + 4 ) * 2", "3 4 + 2 *"),
        ("3 + 4 * 2 / ( 1 - 5 )", "3 4 2 * 1 5 - / +"),
        ("a + b * c", "a b c * +")
    ]
    
    print("Тестирование перевода из инфиксной в постфиксную запись:")
    print("-" * 50)
    for infix, expected_postfix in test_cases:
        result = infix_to_postfix(infix)
        status = "Правиьно" if result == expected_postfix else "Не правильно"
        print(f"{status} '{infix}' -> '{result}' (ожидалось: '{expected_postfix}')")
    print()

test_infix_to_postfix()
```

### Контрольные вопросы 

| Операция | Стек (список) | Очередь (список) | Дек (двусвязный список) | Дек (массив) |
| :--- | :---: | :---: | :---: | :---: |
| `push` / `enqueue` / `pushBack` | **O(1)** | **O(1)** | **O(1)** | **O(1)*** |
| `pop` / `dequeue` / `popBack` | **O(1)** | **O(1)** | **O(1)** | **O(1)*** |
| `pushFront` | — | — | **O(1)** | **O(n)** |
| `popFront` | — | — | **O(1)** | **O(n)** |
| `peek` / `front` / `back` | **O(1)** | **O(1)** | **O(1)** | **O(1)** |
| `isEmpty` | **O(1)** | **O(1)** | **O(1)** | **O(1)** |


