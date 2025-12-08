# +
#1
class Stack:
    def push(self, x):
        raise NotImplementedError
    def pop(self):
        raise NotImplementedError
    def peek(self):
        raise NotImplementedError
    def isEmpty(self):
        raise NotImplementedError

class Queue:
    def enqueue(self, x):
        raise NotImplementedError
    def dequeue(self):
        raise NotImplementedError
    def peek(self):
        raise NotImplementedError
    def isEmpty(self):
        raise NotImplementedError

class Deque:
    def pushFront(self, x):
        raise NotImplementedError
    def pushBack(self, x):
        raise NotImplementedError
    def popFront(self):
        raise NotImplementedError
    def popBack(self):
        raise NotImplementedError
    def peekFront(self):
        raise NotImplementedError
    def peekBack(self):
        raise NotImplementedError
    def isEmpty(self):
        raise NotImplementedError

class ListNode:
    def __init__(self, data = 0, next_node = None):
        self.data = data
        self.next = next_node

class DoubleListNode:
    def __init__(self, data=0, prev_node=None, next_node=None):
        self.data = data
        self.prev = prev_node
        self.next = next_node


# +
#2
class Massiv_Stack(Stack):
    def __init__(self):
        self.data = []
        
    def push(self, x):
        self.data.append(x)
        
    def pop(self):
        if self.isEmpty():
            raise IndexError("Stack is empty")
        return self.data.pop()
        
    def peek(self):
        if self.isEmpty():
            raise IndexError("Stack is empty")
        return self.data[-1]    
    def isEmpty(self):
        return len(self.data) == 0

    def __str__(self):
        return f"ArrayStack({self.data})"

class LinkedListStack(Stack):
    def __init__(self):
        self.head = None
        
    def push(self, x):
        new_node = ListNode(x)
        new_node.next = self.head
        self.head = new_node
        
    def pop(self):
        if self.isEmpty():
            raise IndexError("Stack is empty")
        
        data = self.head.data
        self.head = self.head.next
        return data
        
    def peek(self):
        if self.isEmpty():
            raise IndexError("Stack is empty")
        return self.head.data
        
    def isEmpty(self):
        return self.head is None

    def __str__(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return f"LinkedListStack({elements})"


# +
#3
class Massiv_Queue(Queue):
    def __init__(self):
        self.data = []
    def enqueue(self, x):
        self.data.append(x)
    def dequeue(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.data.pop(0)
    def peek(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.data[0]
    def isEmpty(self):
        return len(self.data) == 0
    def __str__(self):
        return f"ArrayQueue({self.data})"

class LinkedListQueue(Queue):
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, x):
        new_node = ListNode(x) 
        if self.isEmpty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        if self.isEmpty():
            raise IndexError("Queue is empty") 
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return data

    def peek(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.head.data

    def isEmpty(self):
        return self.head is None

    def __str__(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return f"LinkedListQueue({elements})"


# +
#4
class Massiv_Deque(Deque):
    def __init__(self):
        self.data = []
        
    def pushFront(self, x):
        self.data.insert(0, x)
        
    def pushBack(self, x):
        self.data.append(x)
        
    def popFront(self):
        if self.isEmpty():
            raise IndexError("Deque is empty")
        return self.data.pop(0)
        
    def popBack(self):
        if self.isEmpty():
            raise IndexError("Deque is empty")
        return self.data.pop()
        
    def peekFront(self):
        if self.isEmpty():
            raise IndexError("Deque is empty")
        return self.data[0]
        
    def peekBack(self):
        if self.isEmpty():
            raise IndexError("Deque is empty")
        return self.data[-1]

    def isEmpty(self):
        return len(self.data) == 0

    def __str__(self):
        return f"ArrayDeque({self.data})"

class LinkedListDeque(Deque):
    def __init__(self):
        self.head = None
        self.tail = None
        
    def pushFront(self, x):
        new_node = DoublyListNode(x)
        
        if self.isEmpty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            
    def pushBack(self, x):
        new_node = DoublyListNode(x)
        
        if self.isEmpty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            
    def popFront(self):
        if self.isEmpty():
            raise IndexError("Deque is empty")
        
        data = self.head.data
        
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        return data
        
    def popBack(self):
        if self.isEmpty():
            raise IndexError("Deque is empty")
        
        data = self.tail.data
        
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        return data
        
    def peekFront(self):
        if self.isEmpty():
            raise IndexError("Deque is empty")
        return self.head.data
        
    def peekBack(self):
        if self.isEmpty():
            raise IndexError("Deque is empty")
        return self.tail.data
        
    def isEmpty(self):
        raise self.head is None
        
    def __str__(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return f"LinkedListDeque({elements})"


# +
#5
def brackets_check(n):
    stack = Massiv_Stack()

    bracket_pairs = {'(': ')', '[': ']', '{': '}'}

    for i, char in enumerate(n):
        if char in bracket_pairs:
            stack.push(char)
        elif char in bracket_pairs.values():
            if stack.isEmpty():
                return False
            
            last_open = stack.pop()
            
            if bracket_pairs[last_open] != char:
                return False

    if not stack.isEmpty():
        return False
    
    return True

n = '[[[]]]'
print(brackets_check(n))


# +
#6
def polish_calculator(n):
    stack = Massiv_Stack()

    for i, char in enumerate(n):
        if char.isdigit():
            stack.push(int(char))
        else:                
            b = stack.pop()
            a = stack.pop()
            
            if char == '+':
                result = a + b
            elif char == '-':
                result = a - b
            elif char == '*':
                result = a * b
            elif char == '/':
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = a / b
            
            stack.push(result)
    
    final_result = stack.pop()
    
    return final_result

n = '123+4*+'
print(polish_calculator(n))    


# +
#7
def inf_to_polish(n):
    operators = {'+': 1, '-': 1, '*': 2, '/': 2,'(': 0}
    
    result = []
    stack = Massiv_Stack()
    
    expression = n.replace('(', ' ( ').replace(')', ' ) ')
    expression = expression.replace('+', ' + ').replace('-', ' - ')
    expression = expression.replace('*', ' * ').replace('/', ' / ')

    chars = expression.split()
    
    for char in chars:
        if char.isdigit() or char.isalpha():
            result.append(char)
        
        elif char == '(':
            stack.push(char)
        
        elif char == ')':
            while not stack.isEmpty() and stack.peek() != '(':
                result.append(stack.pop())
            if stack.isEmpty():
                raise ValueError("Несбалансированные скобки")
            
            stack.pop()
        
        elif char in operators:
            while (not stack.isEmpty() and stack.peek() != '(' and operators[stack.peek()] >= operators[char]):                    
                result.append(stack.pop())
            
            stack.push(char)

    while not stack.isEmpty():
        if stack.peek() == '(':
            raise ValueError("Несбалансированные скобки")
        result.append(stack.pop())
    
    final_result = ' '.join(result)
    
    return final_result

n = 'a+(b+c)*d'
print(inf_to_polish(n))
# -


