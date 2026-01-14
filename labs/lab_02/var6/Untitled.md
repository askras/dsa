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

### Вариант 6

## Сортировка расческой (Comb Sort)

# 1. Классификация сортировки расчесткой

Сортировка расчесткой является внутренней сортировкой, сортирующей элементы в оперативной памяти. Она относится к адаптивным алгоритмам, так как учитывает уже относительно отсортированные участки массива. Это сортировка на месте (on place), не требующая дополнительной памяти, кроме переменных для индексов и шага. По устойчивости сортировка неустойчивая, поскольку при обмене элементов порядок одинаковых ключей может изменяться. По сложности в худшем и среднем случаях время работы близко к $O(n^2)$, но за счет использования "расчески" значительно быстрее пузырьковой сортировки, особенно на больших массивах.

# 2. Теоретическое описание сортировки расчесткой

Сортировка расчесткой улучшает сортировку пузырьком, уменьшая вероятность "залипания" мелких элементов в конце массива. Основная идея — использовать меняющийся интервал (gap) сравнения пар элементов, с шагом уменьшающимся примерно в 1.3 раза после каждой итерации, пока не дойдет до 1. При каждом проходе элементы, находящиеся на расстоянии gap, сравниваются и при необходимости меняются местами. Как только gap достигает 1, сортировка превращается в обычную пузырьковую, но к этому моменту массив уже сильно упорядочен, что ускоряет сортировку.

# 3. Блок-схема сортировки расчесткой

![](comb.jpeg)


![](LaTeX/comb_sort.png)


# 4. Псевдокод сортировки расчесткой

```python
def comb_sort(arr):
    gap = len(arr)
    shrink = 1.247  # оптимальный коэффициент
    sorted = False

    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        i = 0
        while i + gap < len(arr):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
            i += 1
    return arr

```

# 5. Достоинства и недостатки

**Достоинства:**

- Быстрее пузырьковой сортировки благодаря уменьшению инвертированных пар с большим шагом.
- Простая реализация.
- Работает на месте, не требует дополнительной памяти.

**Недостатки:**

- Неустойчивая сортировка.
- Сложность в худшем случае близка к $O(n^2)$, что медленнее более сложных алгоритмов (быстрой или поразрядной сортировки).
- Эффективность зависит от коэффициента уменьшения gap (обычно 1.3).

***

# 6. Реализовать алгоритмы сортировки согласно номеру индивидуального варианта.

```python
import random
import usage_time
import matplotlib.pyplot as plt
import numpy as np

def comb_sort(arr):
    gap = len(arr)
    shrink = 1.247
    sorted = False
    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        i = 0
        while i + gap < len(arr):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
            i += 1
    return arr

%store comb_sort
```

# 7 Протестировать корректность реализации алгоритма и 8 Провести ручную трассировку алгоритма

```python
def quick_comb_sort_debug(arr):
    gap = len(arr)
    shrink = 1.247
    step = 0
    
    print(f"Начало: {arr}")
    
    while True:
        gap = max(1, int(gap / shrink))
        step += 1
        print(f"\nШаг {step}, gap={gap}:")
        
        swapped = False
        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
                print(f"  Меняем {arr[i+gap]}↔{arr[i]}: {arr}")
        
        if gap == 1 and not swapped:
            break
            
    print(f"\nФинальный результат: {arr}")
    return arr

# Быстрая проверка
test = [6, 2, 8, 1, 5, 3]
print("Быстрая проверка сортировки:")
quick_comb_sort_debug(test.copy())
```

Провести сравнение указанных алгоритмов сортировки массивов, содержащих n1, n2, n3 и n4 элементов.
Каждую функцию сортировки вызывать трижды: для сортировки упорядоченного массива, массива, упорядоченного в обратном порядке и неупорядоченного массива. Сортируемая последовательность для всех методов должна быть одинаковой (сортировать копии одного массива).
Проиллюстрировать эффективность алгоритмов сортировок по заданному критерию. Построить диаграммы указанных зависимостей.

```python
import random
import usage_time
import matplotlib.pyplot as plt
import numpy as np

def comb_sort(arr):
    gap = len(arr)
    shrink = 1.247
    sorted_flag = False
    
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        
        i = 0
        while i + gap < len(arr):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False
            i += 1
    return arr

sizes = [1000, 5000, 10000, 100000]

def generate_arrays(size):
    sorted_arr = list(range(size))
    reversed_arr = list(range(size, 0, -1))
    random_arr = [random.randint(1, size * 10) for _ in range(size)]
    
    return {
        'sorted': sorted_arr,
        'reversed': reversed_arr,
        'random': random_arr
    }

func = usage_time.get_usage_time(ndigits=6)(comb_sort)

results = {
    'sorted': [],
    'reversed': [], 
    'random': []
}

print("ИЗМЕРЕНИЕ ВРЕМЕНИ СОРТИРОВКИ РАСЧЕСКОЙ")
print("=" * 70)

for size in sizes:
    print(f"Размер массива: {size} элементов")
    print("-" * 50)
    
    arrays = generate_arrays(size)
    
    for array_type, arr in arrays.items():
        time_taken = func(arr.copy())
        results[array_type].append(time_taken)
        
        print(f"  {array_type:>8}: {time_taken:.6f} сек")

plt.figure(figsize=(15, 5))

colors = {'sorted': 'green', 'reversed': 'red', 'random': 'blue'}

for i, array_type in enumerate(['sorted', 'reversed', 'random'], 1):
    plt.subplot(1, 3, i)
    plt.plot(sizes, results[array_type], 'o-', color=colors[array_type], 
             linewidth=2, markersize=8)
    
    for size, time in zip(sizes, results[array_type]):
        plt.annotate(f'{time:.4f}с', (size, time), 
                    textcoords="offset points", xytext=(0,10), 
                    ha='center', fontsize=8)
    
    plt.xlabel('Размер массива')
    plt.ylabel('Время, секунды')
    plt.title(f'Тип: {array_type}')
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("СТАТИСТИЧЕСКИЙ АНАЛИЗ")
print("=" * 70)

for array_type in ['sorted', 'reversed', 'random']:
    times = results[array_type]
    print(f"{array_type.upper():>15}:")
    for size, time in zip(sizes, times):
        print(f"  {size:6d} эл.: {time:8.4f} сек")
    
    if len(times) > 1:
        growth = times[-1] / times[0]
        print(f"  Рост времени ({sizes[-1]}/{sizes[0]}): {growth:.2f}x")

print("СРАВНЕНИЕ ЭФФЕКТИВНОСТИ:")
print(f"Упорядоченный массив сортируется в {results['reversed'][-1]/results['sorted'][-1]:.2f} раза медленнее")
print(f"Случайный массив сортируется в {results['random'][-1]/results['sorted'][-1]:.2f} раза медленнее")
```

## Сравнение 

```python
import random
import usage_time
import matplotlib.pyplot as plt
import numpy as np

def comb_sort(arr):
    gap = len(arr)
    shrink = 1.247
    sorted_flag = False
    
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        
        i = 0
        while i + gap < len(arr):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False
            i += 1
    return arr

def radix_sort(arr):
    if not arr:
        return arr
    
    max_num = max(arr)
    exp = 1
    
    while max_num // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10
    
    return arr

def counting_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    
    for i in range(n):
        arr[i] = output[i]

sizes = [1000, 5000, 10000, 100000]

def generate_arrays(size):
    sorted_arr = list(range(size))
    reversed_arr = list(range(size, 0, -1))
    random_arr = [random.randint(1, size * 10) for _ in range(size)]
    
    return {
        'sorted': sorted_arr,
        'reversed': reversed_arr,
        'random': random_arr
    }

comb_func = usage_time.get_usage_time(ndigits=6)(comb_sort)
radix_func = usage_time.get_usage_time(ndigits=6)(radix_sort)

comb_results = {
    'sorted': [],
    'reversed': [], 
    'random': []
}

radix_results = {
    'sorted': [],
    'reversed': [], 
    'random': []
}

print("ИЗМЕРЕНИЕ ВРЕМЕНИ СОРТИРОВКИ РАСЧЕСКОЙ")
print("=" * 70)

for size in sizes:
    print(f"Размер массива: {size} элементов")
    print("-" * 50)
    
    arrays = generate_arrays(size)
    
    for array_type, arr in arrays.items():
        time_taken = comb_func(arr.copy())
        comb_results[array_type].append(time_taken)
        
        print(f"  {array_type:>8}: {time_taken:.6f} сек")

print("\nИЗМЕРЕНИЕ ВРЕМЕНИ ПОРАЗРЯДНОЙ СОРТИРОВКИ")
print("=" * 70)

for size in sizes:
    print(f"Размер массива: {size} элементов")
    print("-" * 50)
    
    arrays = generate_arrays(size)
    
    for array_type, arr in arrays.items():
        time_taken = radix_func(arr.copy())
        radix_results[array_type].append(time_taken)
        
        print(f"  {array_type:>8}: {time_taken:.6f} сек")

plt.figure(figsize=(15, 5))

for i, array_type in enumerate(['sorted', 'reversed', 'random'], 1):
    plt.subplot(1, 3, i)
    
    plt.plot(sizes, comb_results[array_type], 'o-', color='red', 
             linewidth=2, markersize=8, label='Comb Sort')
    
    plt.plot(sizes, radix_results[array_type], 's-', color='blue', 
             linewidth=2, markersize=8, label='Radix Sort')
    
    for j, size in enumerate(sizes):
        plt.annotate(f'{comb_results[array_type][j]:.4f}с', (size, comb_results[array_type][j]), 
                    textcoords="offset points", xytext=(0,10), 
                    ha='center', fontsize=7, color='red')
        plt.annotate(f'{radix_results[array_type][j]:.4f}с', (size, radix_results[array_type][j]), 
                    textcoords="offset points", xytext=(0,-15), 
                    ha='center', fontsize=7, color='blue')
    
    plt.xlabel('Размер массива')
    plt.ylabel('Время, секунды')
    plt.title(f'Тип: {array_type}')
    plt.legend()
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("СТАТИСТИЧЕСКИЙ АНАЛИЗ - СОРТИРОВКА РАСЧЕСКОЙ")
print("=" * 70)

for array_type in ['sorted', 'reversed', 'random']:
    times = comb_results[array_type]
    print(f"{array_type.upper():>15}:")
    for size, time in zip(sizes, times):
        print(f"  {size:6d} эл.: {time:8.4f} сек")
    
    if len(times) > 1:
        growth = times[-1] / times[0]
        print(f"  Рост времени ({sizes[-1]}/{sizes[0]}): {growth:.2f}x")

print("\nСТАТИСТИЧЕСКИЙ АНАЛИЗ - ПОРАЗРЯДНАЯ СОРТИРОВКА")
print("=" * 70)

for array_type in ['sorted', 'reversed', 'random']:
    times = radix_results[array_type]
    print(f"{array_type.upper():>15}:")
    for size, time in zip(sizes, times):
        print(f"  {size:6d} эл.: {time:8.4f} сек")
    
    if len(times) > 1:
        growth = times[-1] / times[0]
        print(f"  Рост времени ({sizes[-1]}/{sizes[0]}): {growth:.2f}x")

print("\nСРАВНЕНИЕ ЭФФЕКТИВНОСТИ:")
print(f"Comb Sort - обратный/упорядоченный: {comb_results['reversed'][-1]/comb_results['sorted'][-1]:.2f}x")
print(f"Comb Sort - случайный/упорядоченный: {comb_results['random'][-1]/comb_results['sorted'][-1]:.2f}x")
print(f"Radix Sort - обратный/упорядоченный: {radix_results['reversed'][-1]/radix_results['sorted'][-1]:.2f}x")
print(f"Radix Sort - случайный/упорядоченный: {radix_results['random'][-1]/radix_results['sorted'][-1]:.2f}x")
print(f"Comb/Radix на случайных данных: {comb_results['random'][-1]/radix_results['random'][-1]:.2f}x")
```

<!-- #region -->
## Поразрядная сортировка
# 1. Классификация алгоритмов сортировки

- Внутренняя сортировка (работает в оперативной памяти)
- Устойчивая сортировка (сохраняет порядок элементов с одинаковыми ключами)
- Использует дополнительную память для промежуточных структур
- Линейная временная сложность при фиксированной длине ключей: $O(n \cdot k)$, где $n$ — количество элементов, $k$ — количество разрядов
- Сортирует методом обхода и группировки по разрядам из системы счисления (основание radix)


# 2. Теоретическое описание алгоритма

Поразрядная сортировка "Radix Sort" обрабатывает элементы по разрядам ключа, сначала группирует их по младшему разряду (LSD) или по старшему (MSD).

Основные шаги:

1. Определяется максимальное количество разрядов у элементов.
2. На каждом шаге выполняется устойчивая сортировка по текущему разряду (например, сортировка подсчётом).
3. После сортировки по всем разрядам массив оказывается полностью отсортированным.

Преимущество — отсутствие прямых сравнений элементов, что ускоряет работу при ограниченной длине ключей.

# 3. Блок-схема алгоритма


![](LaTeX/radix_sort.png)

- Начало
- Найти максимальный элемент и определить количество разрядов $d$
- Цикл по $i = 1 \text{ до } d$:
    - Устойчивая сортировка массива по $i$-му разряду
- Конец — массив отсортирован


# 4. Псевдокод алгоритма (LSD-версия)

```
function radixSort(array A):
    maxVal = max(A)
    d = число_разрядов(maxVal)
    for digit in 1 to d:
        A = stableSortByDigit(A, digit)
    return A
```

Где `stableSortByDigit` — устойчивая сортировка массива по $digit$-му разряду, чаще всего применяется сортировка подсчётом.

# 5. Достоинства и недостатки

| Достоинства | Недостатки |
| :-- | :-- |
| Линейная сложность при фиксированном $k$ | Требует дополнительной памяти для подсчёта |
| Стабильность сортировки | Неэффективна при очень больших или длинных ключах |
| Отсутствие прямых сравнений элементов | Требует знания основания системы счисления |

# 6. Реализовать алгоритмы сортировки согласно номеру индивидуального варианта.
<!-- #endregion -->

```python
def radix_sort(arr):
    if not arr:
        return arr
    
    max_num = max(arr)
    
    exp = 1
    while max_num // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10
    
    return arr

def counting_sort_for_radix(arr, exp):
    """
    Вспомогательная функция для сортировки подсчетом по текущему разряду
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    
    for i in range(n):
        arr[i] = output[i]
```

# 7. Ручная тестировка

```python
def radix_sort_visual(arr):
    print("Начало сортировки")
    print(f"Исходный массив: {arr}")
    
    if not arr:
        return arr
    
    max_num = max(arr)
    print(f"Максимальное число: {max_num}")
    
    exp = 1
    iteration = 1
    
    while max_num // exp > 0:
        print(f"\n--- Итерация {iteration}: разряд {exp} ---")
        arr = counting_sort_visual(arr, exp)
        exp *= 10
        iteration += 1
    
    print(f"\nСортировка завершена!")
    print(f"Результат: {arr}")
    return arr

def counting_sort_visual(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    print("Шаг 1: Подсчет цифр")
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1
        print(f"{arr[i]} -> цифра {digit}")
    
    print(f"Count: {count}")
    
    print("Шаг 2: Преобразование count")
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    print(f"Positions: {count}")
    
    print("Шаг 3: Построение output")
    print(f"Исходный: {arr}")
    
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        position = count[digit] - 1
        output[position] = arr[i]
        count[digit] -= 1
        print(f"{arr[i]} (цифра {digit}) -> позиция {position}")
        print(f"Output: {output}")
    
    print(f"Результат: {output}")
    return output

def simple_radix_sort_visual(arr):
    print(f"Сортируем: {arr}")
    
    if len(arr) <= 1:
        return arr
    
    max_num = max(arr)
    exp = 1
    
    while max_num // exp > 0:
        print(f"\nРазряд: {exp}")
        
        n = len(arr)
        count = [0] * 10
        output = [0] * n
        
        print("Цифры чисел:")
        for num in arr:
            digit = (num // exp) % 10
            count[digit] += 1
            print(f"{num} -> {digit}")
        
        print(f"Count: {count}")
        
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        print(f"Позиции: {count}")
        
        for i in range(n - 1, -1, -1):
            num = arr[i]
            digit = (num // exp) % 10
            pos = count[digit] - 1
            output[pos] = num
            count[digit] -= 1
            print(f"{num} -> позиция {pos}: {output}")
        
        arr = output
        exp *= 10
    
    print(f"\nИтог: {arr}")
    return arr

# Тестирование
if __name__ == "__main__":
    print("ТЕСТ 1:")
    test1 = [170, 45, 75, 90]
    radix_sort_visual(test1.copy())
    
    print("\n" + "="*40 + "\n")
    
    print("ТЕСТ 2:")
    test2 = [42, 17, 89, 5]
    simple_radix_sort_visual(test2.copy())
```

# Пункты 9, 10, 11

```python
import random
import usage_time
import matplotlib.pyplot as plt
import numpy as np

def radix_sort(arr):
    if not arr:
        return arr
    
    max_num = max(arr)
    exp = 1
    
    while max_num // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10
    
    return arr

def counting_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    
    for i in range(n):
        arr[i] = output[i]

sizes = [1000, 2000, 4000, 8000]

def generate_arrays(size):
    sorted_arr = list(range(size))
    reversed_arr = list(range(size, 0, -1))
    random_arr = [random.randint(1, size * 10) for _ in range(size)]
    
    return {
        'sorted': sorted_arr,
        'reversed': reversed_arr,
        'random': random_arr
    }

func = usage_time.get_usage_time(ndigits=6)(radix_sort)

results = {
    'sorted': [],
    'reversed': [], 
    'random': []
}

print("ИЗМЕРЕНИЕ ВРЕМЕНИ ПОРАЗРЯДНОЙ СОРТИРОВКИ")
print("=" * 70)

for size in sizes:
    print(f"Размер массива: {size} элементов")
    print("-" * 50)
    
    arrays = generate_arrays(size)
    
    for array_type, arr in arrays.items():
        time_taken = func(arr.copy())
        results[array_type].append(time_taken)
        
        print(f"  {array_type:>8}: {time_taken:.6f} сек")

plt.figure(figsize=(15, 5))

colors = {'sorted': 'green', 'reversed': 'red', 'random': 'blue'}

for i, array_type in enumerate(['sorted', 'reversed', 'random'], 1):
    plt.subplot(1, 3, i)
    plt.plot(sizes, results[array_type], 'o-', color=colors[array_type], 
             linewidth=2, markersize=8, markerfacecolor='white', markeredgewidth=2)
    
    for size, time in zip(sizes, results[array_type]):
        plt.annotate(f'{time:.4f}с', (size, time), 
                    textcoords="offset points", xytext=(0,10), 
                    ha='center', fontsize=8, fontweight='bold')
    
    plt.xlabel('Размер массива')
    plt.ylabel('Время, секунды')
    plt.title(f'Поразрядная сортировка: {array_type}')
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("СТАТИСТИЧЕСКИЙ АНАЛИЗ")
print("=" * 70)

for array_type in ['sorted', 'reversed', 'random']:
    times = results[array_type]
    print(f"{array_type.upper():>15}:")
    for size, time in zip(sizes, times):
        print(f"  {size:6d} эл.: {time:8.4f} сек")
    
    if len(times) > 1:
        growth = times[-1] / times[0]
        print(f"  Рост времени ({sizes[-1]}/{sizes[0]}): {growth:.2f}x")

print("СРАВНЕНИЕ ЭФФЕКТИВНОСТИ:")
print(f"Обратный порядок сортируется в {results['reversed'][-1]/results['sorted'][-1]:.2f} раза медленнее упорядоченного")
print(f"Случайный массив сортируется в {results['random'][-1]/results['sorted'][-1]:.2f} раза медленнее упорядоченного")
```

<!-- #region -->
1. В чем состоит суть метода сортировки вставками?
Суть метода заключается в том, что массив делится на отсортированную и неотсортированную части. На каждом шаге берется очередной элемент из неотсортированной части и вставляется на правильную позицию в отсортированной части.

2. Какие шаги выполняет алгоритм сортировки вставками?

Начинаем со второго элемента (i = 1)

Сохраняем текущий элемент в временную переменную

Сдвигаем элементы отсортированной части, которые больше текущего элемента, вправо

Вставляем текущий элемент на освободившееся место

Повторяем для всех элементов массива

3. Как программно реализуется сортировка вставками?

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```
4. В чем достоинства и недостатки метода сортировки вставками?
Достоинства: простая реализация, эффективен на небольших массивах, устойчив, адаптивен
Недостатки: O(n²) в худшем случае, неэффективен на больших массивах

5. Приведите практический пример сортировки массива методом вставок
Массив: [5, 2, 4, 6, 1, 3]
Шаги: [2, 5, 4, 6, 1, 3] → [2, 4, 5, 6, 1, 3] → [2, 4, 5, 6, 1, 3] → [1, 2, 4, 5, 6, 3] → [1, 2, 3, 4, 5, 6]

6. В чем состоит суть сортировки методом Шелла?
Суть в сравнении элементов, стоящих на определенном расстоянии друг от друга (с убывающим шагом), что позволяет быстрее перемещать элементы на большие расстояния.

7. За счет чего метод Шелла дает лучшие показатели по сравнению с простейшими методами?
За счет предварительной сортировки элементов на больших расстояниях, что уменьшает количество инверсий и позволяет быстрее упорядочивать массив.

8. Приведите практический пример сортировки массива методом Шелла
Массив: [8, 3, 7, 4, 1, 9, 2, 6, 5]
Шаг 4: [1, 3, 7, 4, 8, 9, 2, 6, 5]
Шаг 2: [1, 3, 2, 4, 5, 6, 7, 9, 8]
Шаг 1: [1, 2, 3, 4, 5, 6, 7, 8, 9]

9. Какой фактор оказывает наибольшее влияние на эффективность сортировки методом Шелла?
Выбор последовательности шагов (интервалов) для сравнения элементов.

10. Какие последовательности шагов группировки рекомендуются для практического использования в методе Шелла?
Последовательность Кнута: 1, 4, 13, 40, 121... или последовательность Седжвика: 1, 8, 23, 77, 281...

11. Как программно реализуется сортировка методом Шелла?

```python
def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr
```
12. В чем состоит суть метода сортировки выбором?
На каждом шаге находится минимальный элемент из неотсортированной части и помещается в конец отсортированной части.

13. Какие шаги выполняет алгоритм сортировки выбором?

Находим минимальный элемент в неотсортированной части

Меняем его местами с первым элементом неотсортированной части

Увеличиваем границу отсортированной части на 1

Повторяем пока весь массив не будет отсортирован

14. Как программно реализуется сортировка выбором?

```python
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```
    
15. В чем достоинства и недостатки метода сортировки выбором?
Достоинства: простая реализация, минимальное количество перестановок
Недостатки: O(n²) в любом случае, неустойчив


16. Приведите практический пример сортировки массива методом выбора
Массив: [64, 25, 12, 22, 11]
Шаги: [11, 25, 12, 22, 64] → [11, 12, 25, 22, 64] → [11, 12, 22, 25, 64] → [11, 12, 22, 25, 64]

17. В чем состоит суть метода сортировки обменом?
Сравниваются соседние элементы и меняются местами, если они находятся в неправильном порядке.

18. Какие шаги выполняет алгоритм сортировки обменом?

Проходим по массиву несколько раз

На каждой итерации сравниваем соседние элементы

Если порядок неправильный - меняем их местами

Повторяем до тех пор, пока массив не будет отсортирован

19. Как программно реализуется сортировка обменом?

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```
20. В чем достоинства и недостатки метода сортировки обменом?
Достоинства: простая реализация, устойчив
Недостатки: O(n²) в худшем случае, медленный на больших массивах

21. Приведите практический пример сортировки массива методом обмена
Массив: [5, 1, 4, 2, 8]
1 проход: [1, 5, 4, 2, 8] → [1, 4, 5, 2, 8] → [1, 4, 2, 5, 8] → [1, 4, 2, 5, 8]
2 проход: [1, 4, 2, 5, 8] → [1, 2, 4, 5, 8] → [1, 2, 4, 5, 8]

22. В чем состоит суть метода быстрой сортировки?
Выбирается опорный элемент, массив разбивается на две части: элементы меньше опорного и элементы больше опорного, затем рекурсивно сортируются обе части.

23. За счет чего метод быстрой сортировки дает лучшие показатели по сравнению с простейшими методами?
За счет принципа "разделяй и властвуй" и в среднем случае времени O(n log n).

24. Что такое опорный элемент в методе быстрой сортировки и как он используется?
Опорный элемент - это элемент, относительно которого происходит разделение массива. Элементы меньше опорного перемещаются влево, больше - вправо.

25. Приведите практический пример быстрой сортировки массива
Массив: [10, 80, 30, 90, 40, 50, 70]
Опорный: 70
Разделение: [10, 30, 40, 50] 70 [80, 90]
Рекурсивная сортировка обеих частей

26. Что можно сказать о применимости метода быстрой сортировки с точки зрения его эффективности?
Эффективен для больших массивов, но может деградировать до O(n²) при неудачном выборе опорного элемента.

27. Какой фактор оказывает решающее влияние на эффективность метода быстрой сортировки?
Выбор опорного элемента.

28. Почему выбор серединного элемента в качестве опорного в методе быстрой сортировки может резко ухудшать эффективность метода?
Если массив уже отсортирован или почти отсортирован, выбор серединного элемента может привести к несбалансированному разделению.

29. Какое правило выбора опорного элемента в методе быстрой сортировки является наилучшим и почему его сложно использовать?
Медиана трех элементов (первого, среднего и последнего). Сложно использовать из-за дополнительных сравнений.

30. Какое простое правило выбора опорного элемента в методе быстрой сортировки рекомендуется использовать на практике?
Случайный выбор или медиана трех.

31. Какие усовершенствования имеет базовый алгоритм метода быстрой сортировки?

Выбор опорного элемента через медиану трех

Использование insertion sort для маленьких подмассивов

Итеративная реализация для избежания переполнения стека

32. Почему быстрая сортировка проще всего программно реализуется с помощью рекурсии?
Рекурсия естественным образом отражает принцип "разделяй и властвуй".

33. Как программно реализуется рекурсивный вариант метода быстрой сортировки?

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```
    
34. Какие особенности имеет не рекурсивная программная реализация метода быстрой сортировки?
Использует стек для хранения границ подмассивов, требует ручного управления памятью.

35. В чем состоит суть метода пирамидальной сортировки?
Строится двоичная куча из элементов массива, затем многократно извлекается максимальный элемент и перестраивается куча.

36. Какой набор данных имеет пирамидальную организацию?
Двоичная куча - полное двоичное дерево, где каждый узел больше (max-heap) или меньше (min-heap) своих потомков.

37. Чем отличаются друг от друга дерево поиска и пирамидальное дерево?
Дерево поиска: левый потомок < родитель < правый потомок
Пирамидальное дерево: родитель > потомков (max-heap) или родитель < потомков (min-heap)

38. Приведите пример пирамидального дерева с целочисленными ключами


```text
        100
       /   \
      19    36
     /  \   /
    17   3 25
```
39. Какие полезные свойства имеет пирамидальное дерево?

Максимальный/минимальный элемент всегда в корне

Эффективные операции вставки и извлечения за O(log n)

40. Какие шаги выполняются при построении пирамидального дерева?

Начинаем с последнего нелистового узла

Просеиваем узел вниз до правильной позиции

Переходим к предыдущему узлу

Повторяем до корня

41. Что такое просеивание элемента через пирамиду?
Процесс перемещения элемента вниз по дереву до тех пор, пока он не займет правильную позицию относительно своих потомков.

42. Приведите практический пример построения пирамидального дерева
Массив: [4, 10, 3, 5, 1]
Построение: [10, 5, 3, 4, 1]

43. Какие шаги выполняются на втором этапе пирамидальной сортировки?

Меняем корень (максимальный элемент) с последним элементом

Уменьшаем размер кучи на 1

Просеиваем новый корень

Повторяем пока куча не пуста

44. Приведите практический пример реализации второго этапа пирамидальной сортировки
Куча: [10, 5, 3, 4, 1]
Шаг 1: [1, 5, 3, 4, 10] → Просеиваем: [5, 4, 3, 1, 10]
Шаг 2: [1, 4, 3, 5, 10] → Просеиваем: [4, 1, 3, 5, 10]
и т.д.

45. Что можно сказать о трудоемкости метода пирамидальной сортировки?
Время: O(n log n) в худшем, среднем и лучшем случае. Память: O(1).
<!-- #endregion -->
