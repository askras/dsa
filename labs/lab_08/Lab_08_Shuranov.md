# Лабораторная работа 8
# Двоичные деревья поиска (Binary Search Tree)
## Цель работы
Изучение структуры данных «Двоичное дерево поиска», а также основных операций над ним.
## Задачи лабораторной работы
1. Изучение cтруктуры данных дерево
2. Реализация класса дерево
3. Применение дерева для индивидуального задания
## Словесная постановка задачи
1. Изучить как осуществляется балансировка дерева
2. Реализовать свой класс дерева и авл дерева
3. Применить этот класс для решения задачи
## Реализация структуры данных двоичное дерево
Первая часть реализует класс Node для бинарного дерева
``` Python
#1
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
```
Вторая часть реализует класс Derevo с небалансирующемся деревом
``` Python
#2

class Derevo:
    def __init__(self):
        self.root = None
        
    def is_empty(self):
        return self.root is None
        
    def insert(self, value):
        if self.search(value):
            print("Элемент уже существует в дереве")
            return False
            
        new_node = Node(value)
        if self.is_empty():
            self.root = new_node
            return True
        return self.insert_rec(self.root, new_node)

    def insert_rec(self, current, new_node):
        if new_node.value < current.value:
            if current.left is None:
                current.left = new_node
                return True
            else:
                return self.insert_rec(current.left, new_node)
        else:
            if current.right is None:
                current.right = new_node
                return True
            else:
                return self.insert_rec(current.right, new_node)

    def search(self, value):
        return self.search_rec(self.root, value)

    def search_rec(self, current, value):
        if current is None:
            return None
        if current.value == value:
            return current
        elif value < current.value:
            return self.search_rec(current.left, value)
        else:
            return self.search_rec(current.right, value)

    def delete(self, value):
        if self.is_empty():
            print("Дерево пустое")
            return False

        if not self.search(value):
            print("Элемент не найден в дереве")
            return False

        self.root = self.delete_rec(self.root, value)
        return True

    def delete_rec(self, current, value):
        if current is None:
            return None
        if value < current.value:
            current.left = self.delete_rec(current.left, value)
        elif value > current.value:
            current.right = self.delete_rec(current.right, value)
        else:
            if current.left is None:
                return current.right
            elif current.right is None:
                return current.left

            min_node = self.min_find(current.right)
            current.value = min_node.value
            current.right = self.delete_rec(current.right, min_node.value)

        return current

    def min_find(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def height(self):
        return self.height_rec(self.root)

    def height_rec(self, node):
        if node is None:
            return 0
        left_height = self.height_rec(node.left)
        right_height = self.height_rec(node.right)
        return max(left_height, right_height) + 1



    def obhod1(self):
        result = []
        self.obhod1_rec(self.root, result)
        return result

    def obhod2(self):
        result = []
        self.obhod2_rec(self.root, result)
        return result

    def obhod3(self):
        result = []
        self.obhod1_rec(self.root, result)
        return result


    def obhod1_rec(self, node, result):
        result.append(node.value)
        self.obhod1_rec(node.left, result)
        self.obhod1_rec(node.right, result)

    def obhod2_rec(self, node, result):
        self.obhod2_rec(node.left, result)
        result.append(node.value)
        self.obhod2_rec(node.right, result)

    def obhod3_rec(self, node, result):
        self.obhod3_rec(node.left, result)
        self.obhod3_rec(node.right, result)
        result.append(node.value)

    def display(self):
        if self.is_empty():
            print("Дерево пустое")
            return

        queue = [self.root]
        level = 0

        while queue:
            level_size = len(queue)
            level_values = []
            next_level = []

            for node in queue:
                if node is None:
                    level_values.append("None")
                else:
                    level_values.append(node.value)
                    next_level.append(node.left)
                    next_level.append(node.right)
            print(level_values)

            if any(node is not None for node in next_level):
                queue = next_level
                level += 1
            else:
                break
```
Третья часть тестирует данный класс
``` Python
#3
 
d = Derevo()
d.insert(5)
d.insert(1)
d.insert(2)
d.insert(6)
d.display()
```
Четвертая часть реализует класс AvlNode для бинарного дерева с балансировкой
``` Python
#4

class AvlNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1
```
Пятая часть реализует класс AvlDerevo с балансирующемся деревом
``` Python
#5

class AvlDerevo:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        if node is not None:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def right_rotate(self, y):
        x = y.left
        a = x.right
        x.right = y
        y.left = a

        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotate(self, x):
        y = x.right
        a = y.left
        y.left = x
        x.right = a

        self.update_height(x)
        self.update_height(y)
        return y
        
    def is_empty(self):
        return self.root is None
        
    def insert(self, value):
        if self.search(value):
            print("Элемент уже существует в дереве")
            return False
            
        self.root = self.insert_rec(self.root, value)
        return True

    def insert_rec(self, current, value):
        if current is None:
            return AvlNode(value)
            
        if value < current.value:
            current.left = self.insert_rec(current.left, value)
        else:
            current.right = self.insert_rec(current.right, value)

        self.update_height(current)
        balance = self.get_balance(current)

        if balance > 1 and value < current.left.value:
            return self.right_rotate(current)
        if balance < -1 and value > current.right.value:
            return self.left_rotate(current)
        if balance > 1 and value > current.left.value:
            current.left = self.left_rotate(current.left)
            return self.right_rotate(current)
        if balance < -1 and value < current.right.value:
            current.right = self.right_rotate(current.right)
            return self.left_rotate(current)
        
        return current

    def search(self, value):
        return self.search_rec(self.root, value)

    def search_rec(self, current, value):
        if current is None:
            return None
        if current.value == value:
            return current
        elif value < current.value:
            return self.search_rec(current.left, value)
        else:
            return self.search_rec(current.right, value)

    def delete(self, value):
        if self.is_empty():
            print("Дерево пустое")
            return False

        if not self.search(value):
            print("Элемент не найден в дереве")
            return False

        self.root = self.delete_rec(self.root, value)
        return True

    def delete_rec(self, current, value):
        if current is None:
            return None
        if value < current.value:
            current.left = self.delete_rec(current.left, value)
        elif value > current.value:
            current.right = self.delete_rec(current.right, value)
        else:
            if current.left is None:
                return current.right
            elif current.right is None:
                return current.left

            min_node = self.min_find(current.right)
            current.value = min_node.value
            current.right = self.delete_rec(current.right, min_node.value)

        self._update_height(current)
        balance = self.get_balance(current)
        
        if balance > 1 and self.get_balance(current.left) >= 0:
            return self.right_rotate(current)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return current

    def min_find(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def height(self):
        return self.height_rec(self.root)

    def height_rec(self, node):
        if node is None:
            return 0
        left_height = self.height_rec(node.left)
        right_height = self.height_rec(node.right)
        return max(left_height, right_height) + 1

    def display(self):
        if self.is_empty():
            print("Дерево пустое")
            return

        queue = [self.root]
        level = 0

        while queue:
            level_size = len(queue)
            level_values = []
            next_level = []

            for node in queue:
                if node is None:
                    level_values.append("None")
                else:
                    level_values.append(node.value)
                    next_level.append(node.left)
                    next_level.append(node.right)
            print(level_values)

            if any(node is not None for node in next_level):
                queue = next_level
                level += 1
            else:
                break
                
```
Шестая часть тестирует данный класс
``` Python
#6
 
d = AvlDerevo()
d.insert(5)
d.insert(1)
d.insert(2)
d.insert(6)
d.display()
```
Седьмая часть реализует функцию obhod для обхода дерева в ширину
``` Python
#7

from collections import deque

def obhod(tree):
    if tree.is_empty():
        return []

    result = []
    queue = deque([tree.root])

    while queue:
        current_node = queue.popleft()
        result.append(current_node.value)

        if current_node.left is not None:
            queue.append(current_node.left)
        if current_node.right is not None:
            queue.append(current_node.right)

    return result

d = Derevo()
d.insert(5)
d.insert(1)
d.insert(2)
d.insert(6)
print(obhod(d))
```