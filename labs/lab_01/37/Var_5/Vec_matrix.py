import timeit
import random
import matplotlib.pyplot as plt

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

    # Вычисляем длину вектора вручную
    vector_length = 0
    for _ in vector:
        vector_length += 1

    # Вычисляем среднее гармоническое
    harmonic_mean_value = vector_length / sum_of_inverses

    return harmonic_mean_value

def measure_time(func, vector):
    times = []
    for _ in range(5):
        start_time = timeit.default_timer()
        func(vector)
        end_time = timeit.default_timer()
        times.append(end_time - start_time)
    return sum(times) / len(times)

def main():
    N = 5
    max_n = 10**2 * N
    step = 100 * N

    sizes = []
    times_get_element_by_index = []
    times_product_of_elements = []
    times_find_min_element = []
    times_harmonic_mean = []

    for n in range(1, max_n + 1, step):
        vector = [random.randint(1, 100) for _ in range(n)]

        sizes.append(n)
        times_get_element_by_index.append(measure_time(lambda v: get_element_by_index(v, 0), vector))
        times_product_of_elements.append(measure_time(product_of_elements, vector))
        times_find_min_element.append(measure_time(find_min_element, vector))
        times_harmonic_mean.append(measure_time(harmonic_mean, vector))

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_get_element_by_index, label='get_element_by_index')
    plt.plot(sizes, times_product_of_elements, label='product_of_elements')
    plt.plot(sizes, times_find_min_element, label='find_min_element')
    plt.plot(sizes, times_harmonic_mean, label='harmonic_mean')

    plt.xlabel('Количество элементов (n)')
    plt.ylabel('Среднее время выполнения (секунды)')
    plt.title('Зависимость времени выполнения от количества элементов')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()