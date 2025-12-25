import timeit
import matplotlib.pyplot as plt
import random

def cocktail_sort(A):
    left = 0
    right = len(A) - 1
    swapped = True
    while swapped:
        swapped = False
        for i in range(left, right):
            if A[i] > A[i + 1]:
                A[i], A[i + 1] = A[i + 1], A[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        right -= 1
        for i in range(right, left, -1):
            if A[i] < A[i - 1]:
                A[i], A[i - 1] = A[i - 1], A[i]
                swapped = True
        left += 1

# Функция для генерации случайного массива заданной длины
def generate_random_array(length):
    return [random.randint(0, 1000) for _ in range(length)]

# Функция для замера времени выполнения сортировки
def measure_time(array):
    return timeit.timeit(lambda: cocktail_sort(array), number=1)

# Длины массивов для тестирования
lengths = [ 1000,  5000,10000,100000]

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
plt.title('Cocktail Sort Performance')
plt.grid(True)
plt.show()


