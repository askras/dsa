import timeit
import matplotlib.pyplot as plt
import random

class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return TreeNode(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root

def inorder_traversal(root, result):
    if root:
        inorder_traversal(root.left, result)
        result.append(root.val)
        inorder_traversal(root.right, result)

def tree_sort(A):
    root = None
    for key in A:
        root = insert(root, key)
    result = []
    inorder_traversal(root, result)
    return result

# Функция для генерации случайного массива заданной длины
def generate_random_array(length):
    return [random.randint(0, 1000) for _ in range(length)]

# Функция для замера времени выполнения сортировки
def measure_time(array):
    return timeit.timeit(lambda: tree_sort(array), number=1)

# Длины массивов для тестирования
lengths = [1000, 5000, 10000]

# Списки для хранения результатов
times = []

# Замер времени для каждой длины массива
for length in lengths:
    array = generate_random_array(length)
    time_taken = measure_time(array)
    times.append(time_taken)
    print(f"Length: {length}, Time: {time_taken:.6f} seconds")

# Построение графика
plt.plot(lengths, times, marker='o')
plt.xlabel('Array Length')
plt.ylabel('Time (seconds)')
plt.title('Tree Sort Performance')
plt.grid(True)
plt.show()