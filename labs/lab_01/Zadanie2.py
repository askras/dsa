# +
# 1
import functools
import timeit
import typing

def get_usage_time(
    *, number: int = 1, setup: str = 'pass', ndigits: int = 3
) -> typing.Callable:
    def decorator(func: typing.Callable) -> typing.Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> float:
            usage_time = timeit.timeit(
                lambda: func(*args, **kwargs),
                setup=setup,
                number=number,
            )
            return round(usage_time / number, ndigits)

        return wrapper

    return decorator


# +
# 2
import random

N = 6

def matrix_generator(n):
    matrix = []
    for i in range(n):
        line = [random.randint(1, 100*N) for j in range(n)]
        matrix.append(line)
    return matrix

def matrix_proizv(n):
    a = matrix_generator(n)
    b = matrix_generator(n)
    c = [[] for i in range(n)]
    for i in range(n):
        for j in range(n):
            element = 0
            for k in range(n): 
                element += a[i][k] * b[k][j]
            c[i].append(element)
    return c


# +
# 3
import matplotlib.pyplot as plt

N = 6

def five_iteration_matrix(n):
    time_of_matrix = []
    matrix_time = get_usage_time(ndigits=5)(matrix_proizv)
    for i in range(5):
        time_of_matrix.append(matrix_time(n))
    average_time_matrix = sum(time_of_matrix)/5
    return average_time_matrix
    
# %matplotlib inline

items = range(1, 10**2*N+1, 10)
times_matrix = []
j = 0
for i in items:
    times_matrix.append(five_iteration_matrix(i))
    print('Среднее время произведения матриц для', i, 'порядка матрицы', times_matrix[j])
    j += 1

plt.figure(figsize=(10, 6))
plt.plot(items, times_matrix)
plt.title('График для произведения матриц')
plt.xlabel('Порядок матрицы')
plt.ylabel('Время, сек')
plt.grid(True)   
# -


