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

# Лабораторная работа 8


## Задание 1: Бинарное дерево поиска

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def is_empty(self):
        return self.root is None
    
    def insert(self, value):
        if self._is_valid_value(value):
            self.root = self._insert_recursive(self.root, value)
            return True
        return False
    
    def _insert_recursive(self, node, value):
        if node is None:
            return Node(value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        
        return node
    
    def search(self, value):
        if not self._is_valid_value(value):
            return None
        
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node
        
        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def delete(self, value):
        if not self._is_valid_value(value) or self.is_empty():
            return False
        
        if self.search(value) is None:
            return False
        
        self.root = self._delete_recursive(self.root, value)
        return True
    
    def _delete_recursive(self, node, value):
        if node is None:
            return node
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left           
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)
        
        return node
    
    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def preorder_traversal(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def postorder_traversal(self):
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
    
    def height(self):
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        if node is None:
            return -1
        
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        
        return max(left_height, right_height) + 1
    
    def print_tree(self):
        if self.is_empty():
            print("Дерево пустое")
            return
        
        lines = self._build_tree_display()
        for line in lines:
            print(line)
    
    def _build_tree_display(self):
        if self.root is None:
            return []
        
        def _build_recursive(node, prefix="", is_left=True):
            if node is None:
                return []
            
            result = []
            line = prefix + ("└── " if is_left else "├── ") + str(node.value)
            result.append(line)
            
            children = []
            if node.left or node.right:
                if node.left:
                    children.append((node.left, True))
                if node.right:
                    children.append((node.right, False))
            
            for i, (child, is_left_child) in enumerate(children):
                child_prefix = prefix + ("    " if is_left else "│   ")
                child_lines = _build_recursive(child, child_prefix, is_left_child)
                result.extend(child_lines)
            
            return result
        
        return _build_recursive(self.root, "", True)
    
    def _is_valid_value(self, value):
        return value is not None



bst = BinarySearchTree()
    
print("Дерево пустое?", bst.is_empty())
    
values = [50, 30, 70, 20, 40, 60, 80]
for value in values:
        bst.insert(value)
    
print("\nПосле добавления элементов:")
print("Дерево пустое?", bst.is_empty())
    
print("\nСтруктура дерева:")
bst.print_tree()
    
print("\nПрямой обход:", bst.preorder_traversal())
print("Симметричный обход:", bst.inorder_traversal())
print("Обратный обход:", bst.postorder_traversal())
    
search_value = 40
found = bst.search(search_value)
print(f"\nПоиск значения {search_value}: {'найден' if found else 'не найден'}")
    
print(f"Высота дерева: {bst.height()}")
    
delete_value = 30
bst.delete(delete_value)
print(f"\nУдаление значения {delete_value}: успешно")
    
print("\nСтруктура дерева после удаления:")
bst.print_tree()
    
print("\nСимметричный обход после удаления:", bst.inorder_traversal())
print(f"Высота дерева после удаления: {bst.height()}")
```

## Задание 2: AVL-дерево

```python
class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:    
    def __init__(self):
        self.root = None
    
    def is_empty(self):
        return self.root is None
    
    def _get_height(self, node):
        if node is None:
            return 0
        return node.height
    
    def _get_balance(self, node):
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _update_height(self, node):
        if node is not None:
            node.height = 1 + max(self._get_height(node.left), 
                                self._get_height(node.right))
    
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        
        x.right = y
        y.left = T2
        
        self._update_height(y)
        self._update_height(x)
        
        return x
    
    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        
        y.left = x
        x.right = T2
        
        self._update_height(x)
        self._update_height(y)
        
        return y
    
    def insert(self, value):
        if self._is_valid_value(value):
            self.root = self._insert_recursive(self.root, value)
            return True
        return False
    
    def _insert_recursive(self, node, value):
        if node is None:
            return AVLNode(value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node
        
        self._update_height(node)
        
        balance = self._get_balance(node)
        
        
        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)
        
        if balance < -1 and value > node.right.value:
            return self._rotate_left(node)
        
        if balance > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def search(self, value):
        if not self._is_valid_value(value):
            return None
        
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node
        
        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def delete(self, value):
        if not self._is_valid_value(value) or self.is_empty():
            return False
        
        if self.search(value) is None:
            return False
        
        self.root = self._delete_recursive(self.root, value)
        return True
    
    def _delete_recursive(self, node, value):
        if node is None:
            return node
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)
        
        if node is None:
            return node
        
        self._update_height(node)
        
        balance = self._get_balance(node)
        
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)
        
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)
        
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def preorder_traversal(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def postorder_traversal(self):
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
    
    def height(self):
        return self._get_height(self.root)
    
    def print_tree(self):
        if self.is_empty():
            print("Дерево пустое")
            return
        
        lines = self._build_tree_display()
        for line in lines:
            print(line)
    
    def _build_tree_display(self):
        if self.root is None:
            return []
        
        def _build_recursive(node, prefix="", is_left=True):
            if node is None:
                return []
            
            balance = self._get_balance(node)
            node_info = f"{node.value}(h:{node.height},b:{balance})"
            
            result = []
            line = prefix + ("└── " if is_left else "├── ") + node_info
            result.append(line)
            
            children = []
            if node.left or node.right:
                if node.left:
                    children.append((node.left, True))
                if node.right:
                    children.append((node.right, False))
            
            for i, (child, is_left_child) in enumerate(children):
                child_prefix = prefix + ("    " if is_left else "│   ")
                child_lines = _build_recursive(child, child_prefix, is_left_child)
                result.extend(child_lines)
            
            return result
        
        return _build_recursive(self.root, "", True)
    
    def _is_valid_value(self, value):
        return value is not None
    
    def is_balanced(self):
        return self._check_balanced(self.root)
    
    def _check_balanced(self, node):
        if node is None:
            return True
        
        balance = self._get_balance(node)
        if abs(balance) > 1:
            return False
        
        return self._check_balanced(node.left) and self._check_balanced(node.right)


avl = AVLTree()
    
print("AVL-дерево пустое?", avl.is_empty())
    
print("\nДобавление элементов в AVL-дерево:")
values = [10, 20, 30, 40, 50, 25]
    
for value in values:
    avl.insert(value)
    print(f"После добавления {value}:")
    print("Сбалансировано:", avl.is_balanced())
    print("Высота:", avl.height())
    
print("\nСтруктура AVL-дерева:")
avl.print_tree()
    
print("\nПрямой обход:", avl.preorder_traversal())
print("Симметричный обход (отсортированный):", avl.inorder_traversal())
print("Обратный обход:", avl.postorder_traversal())
    
search_value = 30
found = avl.search(search_value)
print(f"\nПоиск значения {search_value}: {'найден' if found else 'не найден'}")
    
print(f"Высота дерева: {avl.height()}")
print(f"Дерево сбалансировано: {avl.is_balanced()}")
    
delete_value = 30
print(f"\nУдаление значения {delete_value}: {'успешно' if avl.delete(delete_value) else 'не удалось'}")
    
print("\nСтруктура AVL-дерева после удаления:")
avl.print_tree()
    
print("\nСимметричный обход после удаления:", avl.inorder_traversal())
print(f"Высота дерева после удаления: {avl.height()}")
print(f"Дерево сбалансировано после удаления: {avl.is_balanced()}")
    
print("\n" + "="*50)
print("Демонстрация балансировки AVL-дерева:")
    
critical_avl = AVLTree()
critical_values = [1, 2, 3, 4, 5, 6, 7]
    
print("\nДобавление последовательности, создающей вырожденное дерево в обычном BST:")
for value in critical_values:
    critical_avl.insert(value)
    print(f"После {value}: высота = {critical_avl.height()}, сбалансировано = {critical_avl.is_balanced()}")
    
print("\nИтоговая структура AVL-дерева:")
critical_avl.print_tree()
print(f"Высота сбалансированного AVL-дерева: {critical_avl.height()}")
print(f"Высота вырожденного BST для тех же данных: {len(critical_values) - 1}")
```

## Задание 3


```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def find_unbalanced_vertices(root):
    result = []
    
    def count_nodes(node):
        if not node:
            return 0
            
        left = count_nodes(node.left)
        right = count_nodes(node.right)
        
        if left != right:
            result.append(node.val)
            
        return left + right + 1
    
    count_nodes(root)
    return result

# ПРОВЕРКА
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.right.left = TreeNode(5)
root.right.right = TreeNode(6)
root.right.left.left = TreeNode(7)

vertices = find_unbalanced_vertices(root)
print("Результат:", vertices)
```

```python

```
