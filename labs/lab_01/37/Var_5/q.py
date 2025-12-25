import time
import matplotlib.pyplot as plt
import numpy as np


# Функции, которые мы будем тестировать
def get_element_by_index(vector, index):
    return vector[index]


def product_of_elements(vector):
    product = 1
    for element in vector:
        product *= element
    return product


def find_min_element(vector):
    min_element = vector[0]
    for element in vector[1:]:
        if element < min_element:
            min_element = element
    return min_element


def harmonic_mean(vector):
    sum_of_inverses = 0.0
    for x in vector:
        sum_of_inverses += 1.0 / x

    vector_length = 0
    for _ in vector:
        vector_length += 1

    harmonic_mean_value = vector_length / sum_of_inverses
    return harmonic_mean_value


# Функция для измерения времени работы функции
def measure_time(func, vector):
    start_time = time.time()
    func(vector)
    end_time = time.time()
    return end_time - start_time


# Генерация векторов разного размера
N = 5
max_n = 10**4 * N
step = 100 * N
vector_sizes = np.arange(1, max_n, step)
times_get_element = []
times_product = []
times_min_element = []
times_harmonic_mean = []

for size in vector_sizes:
    vector = np.random.rand(size)

    # Измеряем время для каждой функции
    times_get_element.append(measure_time(lambda v: get_element_by_index(v, 0), vector))
    times_product.append(measure_time(product_of_elements, vector))
    times_min_element.append(measure_time(find_min_element, vector))
    times_harmonic_mean.append(measure_time(harmonic_mean, vector))

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(vector_sizes, times_get_element, label='get_element_by_index')
plt.plot(vector_sizes, times_product, label='product_of_elements')
plt.plot(vector_sizes, times_min_element, label='find_min_element')
plt.plot(vector_sizes, times_harmonic_mean, label='harmonic_mean')

plt.xlabel('Размер вектора')
plt.ylabel('Время (секунды)')
plt.title('Зависимость времени работы функций от размера вектора')
plt.legend()
plt.grid(True)
plt.show()