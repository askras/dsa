import random
import time
import matplotlib.pyplot as plt

def quicksort(A, low, high):
    if low < high:
        p = partition(A, low, high)
        quicksort(A, low, p - 1)
        quicksort(A, p + 1, high)

def partition(A, low, high):
    pivot = A[high]
    i = low - 1
    for j in range(low, high):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[high] = A[high], A[i + 1]
    return i + 1

def measure_time(sort_func, arr):
    start_time = time.time()
    sort_func(arr, 0, len(arr) - 1)
    end_time = time.time()
    return end_time - start_time

# Размеры массивов
n1 = 1000
n2 = 5000
n3 = 10000
n4 = 100000

# Генерация случайных массивов
arr1 = [random.randint(0, 10000) for _ in range(n1)]
arr2 = [random.randint(0, 10000) for _ in range(n2)]
arr3 = [random.randint(0, 10000) for _ in range(n3)]
arr4 = [random.randint(0, 10000) for _ in range(n4)]

# Измерение времени выполнения
times = []
sizes = [n1, n2, n3, n4]

for arr in [arr1, arr2, arr3, arr4]:
    time_taken = measure_time(quicksort, arr.copy())
    times.append(time_taken)

# Построение графика
plt.plot(sizes, times, marker='o')
plt.xlabel('Размер массива')
plt.ylabel('Время выполнения (секунды)')
plt.title('Зависимость времени выполнения от размера массива (Быстрая сортировка)')
plt.grid(True)
plt.show()