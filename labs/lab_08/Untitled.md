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

## Вараинт 6
### Задание 1, 3

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        self.root = self._insert(self.root, value)
    
    def _insert(self, node, value):
        if node is None:
            return TreeNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node
    
    def search(self, value):
        return self._search(self.root, value)
    
    def _search(self, node, value):
        if node is None or node.value == value:
            return node is not None
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)
    
    def delete(self, value):
        self.root = self._delete(self.root, value)
    
    def _delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete(node.right, temp.value)
        return node
    
    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def pre_order(self):
        result = []
        self._pre_order(self.root, result)
        return result
    
    def _pre_order(self, node, result):
        if node:
            result.append(node.value)
            self._pre_order(node.left, result)
            self._pre_order(node.right, result)
    
    def in_order(self):
        result = []
        self._in_order(self.root, result)
        return result
    
    def _in_order(self, node, result):
        if node:
            self._in_order(node.left, result)
            result.append(node.value)
            self._in_order(node.right, result)
    
    def post_order(self):
        result = []
        self._post_order(self.root, result)
        return result
    
    def _post_order(self, node, result):
        if node:
            self._post_order(node.left, result)
            self._post_order(node.right, result)
            result.append(node.value)
    
    def level_order(self):
        if not self.root:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result
    
    def height(self):
        return self._height(self.root)
    
    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))
    
    def is_empty(self):
        return self.root is None
    
    def print_tree(self):
        self._print_tree(self.root, 0)
    
    def _print_tree(self, node, level):
        if node:
            self._print_tree(node.right, level + 1)
            print("    " * level + str(node.value))
            self._print_tree(node.left, level + 1)
    
    def has_duplicates(self):
        elements = self.in_order()
        return len(elements) != len(set(elements))

def demo_bst():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    
    for val in values:
        bst.insert(val)
    
    print("BST структура:")
    bst.print_tree()
    
    print("Pre-order:", bst.pre_order())
    print("In-order:", bst.in_order())
    print("Post-order:", bst.post_order())
    print("Level-order:", bst.level_order())
    
    print("Высота:", bst.height())
    print("Пустое:", bst.is_empty())
    print("Поиск 40:", bst.search(40))
    print("Поиск 100:", bst.search(100))
    print("Дубликаты:", bst.has_duplicates())

demo_bst()
```

### Задание 2

```python
class AVLTree(BinarySearchTree):
    def _insert(self, node, value):
        if node is None:
            return TreeNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            return node
        
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)
        
        if balance > 1 and value < node.left.value:
            return self._right_rotate(node)
        if balance < -1 and value > node.right.value:
            return self._left_rotate(node)
        if balance > 1 and value > node.left.value:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and value < node.right.value:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        return node
    
    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y
    
    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y
    
    def _get_height(self, node):
        if node is None:
            return 0
        return node.height
    
    def _get_balance(self, node):
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

def demo_avl():
    avl = AVLTree()
    values = [10, 20, 30, 40, 50, 25]
    
    for val in values:
        avl.insert(val)
    
    print("AVL структура:")
    avl.print_tree()
    
    print("In-order:", avl.in_order())
    print("Высота:", avl.height())
    print("Дубликаты:", avl.has_duplicates())

demo_avl()
```

```python

```
