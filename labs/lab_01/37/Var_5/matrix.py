import numpy as np

# Генерация случайного размера матрицы
n = np.random.randint(0, 10)

# Генерация случайных матриц A и B размером n x n с неотрицательными элементами
A = np.random.randint(0, 10, size=(n, n))
B = np.random.randint(0, 10, size=(n, n))

# Инициализация результирующей матрицы C
C = np.zeros((n, n))

# Вычисление матричного произведения
for i in range(n):
    for j in range(n):
        for k in range(n):
            C[i, j] += A[i, k] * B[k, j]


print("Результат матричного произведения C:")
print(C)