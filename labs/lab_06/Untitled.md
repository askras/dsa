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

## Лаба 6

## ЗАДАНИЕ 1: Рекурсивный алгоритм

```python
import math
import sys
from functools import wraps
import time

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def recursive_series_sum(x, n):
    if n == 0:
        return 0
    if n == 1:
        return x
    
    previous_sum = recursive_series_sum(x, n - 1)
    
    current_term = (x ** (2 * n - 1)) / factorial(n)
    
    return previous_sum + current_term

if __name__ == "__main__":
    print("ЗАДАНИЕ 1: Рекурсивный алгоритм")
    print("=" * 40)
    
    test_cases = [(1, 3), (2, 4), (0.5, 5)]
    
    for x, n in test_cases:
        result = recursive_series_sum(x, n)
        print(f"x={x}, n={n}: сумма = {result:.6f}")
```

![]() 


## ЗАДАНИЕ 2: Итеративный алгоритм (без рекурсии)

```python
def iterative_series_sum(x, n):
    if n == 0:
        return 0
    
    total_sum = 0
    current_factorial = 1
    
    for i in range(1, n + 1):
        if i > 1:
            current_factorial *= i
        else:
            current_factorial = 1
        
        exponent = 2 * i - 1
        current_term = (x ** exponent) / current_factorial
        total_sum += current_term
        
        print(f"  Член {i}: x^{exponent}/{i}! = {current_term:.6f}")
    
    return total_sum

if __name__ == "__main__": 
    x = 2
    n = 4
    print(f"Вычисление ряда для x={x}, n={n}:")
    result = iterative_series_sum(x, n)
    print(f"Итоговая сумма: {result:.6f}")
```

## ЗАДАНИЕ 3: Анализ и сравнение алгоритмов
### Часть 3.1: Класс для сбора статистики и декораторы

```python
class SeriesStats:
    def __init__(self):
        self.iterations = 0
        self.max_stack_depth = 0
        self.execution_time = 0
        self.intermediate_results = []
    
    def reset(self):
        self.iterations = 0
        self.max_stack_depth = 0
        self.execution_time = 0
        self.intermediate_results = []

stats = SeriesStats()

def save_intermediate_results(func):
    @wraps(func)
    def wrapper(x, n, depth=0):
        stats.iterations += 1
        stats.max_stack_depth = max(stats.max_stack_depth, depth)
        
        intermediate = {
            'depth': depth,
            'x': x,
            'n': n,
            'timestamp': time.time()
        }
        
        result = func(x, n, depth)
        
        intermediate['result'] = result
        stats.intermediate_results.append(intermediate)
        
        return result
    return wrapper
```

### Часть 3.2: Модернизированные реализации с сохранением результатов

```python
@save_intermediate_results
def recursive_series_sum_with_stats(x, n, depth=0):
    if n == 0:
        return 0
    if n == 1:
        return x
    
    previous_sum = recursive_series_sum_with_stats(x, n - 1, depth + 1)
    current_term = (x ** (2 * n - 1)) / factorial(n)
    
    return previous_sum + current_term

def manual_recursive_with_storage(x, n):
    intermediate_results = []
    stack_depth = 0
    
    def recursive_helper(x_val, n_val, depth):
        nonlocal stack_depth
        stack_depth = max(stack_depth, depth)
        stats.iterations += 1
        
        intermediate_results.append({
            'depth': depth,
            'x': x_val,
            'n': n_val,
            'action': 'before_call'
        })
        
        if n_val == 0:
            result = 0
            intermediate_results.append({
                'depth': depth,
                'result': result,
                'action': 'base_case_0'
            })
            return result
            
        if n_val == 1:
            result = x_val
            intermediate_results.append({
                'depth': depth,
                'result': result,
                'action': 'base_case_1'
            })
            return result
        
        recursive_result = recursive_helper(x_val, n_val - 1, depth + 1)
        current_term = (x_val ** (2 * n_val - 1)) / factorial(n_val)
        final_result = recursive_result + current_term
        
        intermediate_results.append({
            'depth': depth,
            'current_term': current_term,
            'recursive_result': recursive_result,
            'final_result': final_result,
            'action': 'after_call'
        })
        
        return final_result
    
    result = recursive_helper(x, n, 0)
    stats.max_stack_depth = stack_depth
    stats.intermediate_results = intermediate_results
    return result

def iterative_series_sum_with_stats(x, n):
    stats.reset()
    start_time = time.time()
    
    if n == 0:
        stats.execution_time = time.time() - start_time
        return 0
    
    total_sum = 0
    current_factorial = 1
    
    for i in range(1, n + 1):
        stats.iterations += 1
        
        if i > 1:
            current_factorial *= i
        else:
            current_factorial = 1
        
        exponent = 2 * i - 1
        current_term = (x ** exponent) / current_factorial
        total_sum += current_term
        
        stats.intermediate_results.append({
            'iteration': i,
            'term': current_term,
            'sum_so_far': total_sum,
            'factorial': current_factorial
        })
    
    stats.execution_time = time.time() - start_time
    return total_sum
```

### Часть 3.3: Анализ ограничений рекурсии

```python
def analyze_stack_limit():
    original_limit = sys.getrecursionlimit()
    print(f"Текущий лимит рекурсии: {original_limit}")
    
    max_safe_n = 0
    x_test = 2
    
    for i in range(1, original_limit - 100):
        try:
            recursive_series_sum_with_stats(x_test, i)
            max_safe_n = i
        except RecursionError:
            break
    
    return max_safe_n, original_limit
```

### Часть 3.4: Сравнение производительности

```python
def performance_comparison(test_cases):
    results = []
    
    for x, n in test_cases:
        print(f"\nТестирование: x={x}, n={n}")
        print("-" * 40)
        
        stats.reset()
        start_time = time.time()
        result1 = recursive_series_sum_with_stats(x, n)
        recursive_time = time.time() - start_time
        
        print(f"Рекурсивный (с декоратором): {result1:.6f}")
        print(f"  Время: {recursive_time:.6f}с, Итерации: {stats.iterations}, Глубина: {stats.max_stack_depth}")
        
        stats.reset()
        start_time = time.time()
        result2 = manual_recursive_with_storage(x, n)
        manual_recursive_time = time.time() - start_time
        
        print(f"Рекурсивный (ручное сохранение): {result2:.6f}")
        print(f"  Время: {manual_recursive_time:.6f}с, Итерации: {stats.iterations}, Глубина: {stats.max_stack_depth}")
        
        stats.reset()
        result3 = iterative_series_sum_with_stats(x, n)
        iterative_time = stats.execution_time
        
        print(f"Итеративный: {result3:.6f}")
        print(f"  Время: {iterative_time:.6f}с, Итерации: {stats.iterations}")
        
        tolerance = 1e-10
        results_match = (abs(result1 - result2) < tolerance and 
                        abs(result1 - result3) < tolerance)
        
        if results_match:
            print("✓ Все алгоритмы дали одинаковый результат")
        else:
            print("✗ Ошибка: результаты различаются")
        
        results.append({
            'x': x,
            'n': n,
            'recursive_time': recursive_time,
            'manual_recursive_time': manual_recursive_time,
            'iterative_time': iterative_time,
            'recursive_iterations': stats.iterations,
            'stack_depth': stats.max_stack_depth,
            'results_match': results_match
        })
    
    return results
```

### Часть 3.5: Визуализация и вывод результатов

```python
def print_intermediate_results():
    print("\nПромежуточные результаты (последние 5 записей):")
    for i, result in enumerate(stats.intermediate_results[-5:]):
        print(f"  {i+1}: {result}")

def demonstrate_series_calculation():
    x = 2
    n = 4
    
    print("Члены ряда:")
    total = 0
    for i in range(1, n + 1):
        exponent = 2 * i - 1
        fact = factorial(i)
        term = (x ** exponent) / fact
        total += term
        print(f"  {i}. x^{exponent}/{i}! = {x}^{exponent}/{fact} = {term:.6f}")
    
    print(f"\nСумма {n} членов: {total:.6f}")

if __name__ == "__main__":
    print("ЗАДАНИЕ 3: Анализ и сравнение алгоритмов")
    print("=" * 50)
    
    demonstrate_series_calculation()
    
    print("\n1. АНАЛИЗ ОГРАНИЧЕНИЙ РЕКУРСИИ")
    max_safe_n, recursion_limit = analyze_stack_limit()
    print(f"Максимальное безопасное n: {max_safe_n}")
    
    test_cases = [
        (1, 5),    
        (2, 4),    
        (1, 10),   
        (2, 8),    
        (0.5, 6),  
    ]
    
    print("\n2. СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")
    results = performance_comparison(test_cases)
    
    print("\n3. СВОДНАЯ СТАТИСТИКА")
    print("Алгоритм           | Среднее время | Макс. итераций | Макс. глубина")
    print("-" * 75)
    
    recursive_times = [r['recursive_time'] for r in results]
    manual_times = [r['manual_recursive_time'] for r in results]
    iterative_times = [r['iterative_time'] for r in results]
    
    avg_recursive = sum(recursive_times) / len(recursive_times)
    avg_manual = sum(manual_times) / len(manual_times)
    avg_iterative = sum(iterative_times) / len(iterative_times)
    
    max_iterations = max(r['recursive_iterations'] for r in results)
    max_depth = max(r['stack_depth'] for r in results)
    
    print(f"Рекурсивный        | {avg_recursive:.6f}с     | {max_iterations:12} | {max_depth:11}")
    print(f"Ручной рекурсивный | {avg_manual:.6f}с     | {max_iterations:12} | {max_depth:11}")
    print(f"Итеративный        | {avg_iterative:.6f}с     | {max_iterations:12} | {'N/A':11}")
    
    print("\n4. ДЕМОНСТРАЦИЯ ПРОМЕЖУТОЧНЫХ РЕЗУЛЬТАТОВ")
    stats.reset()
    recursive_series_sum_with_stats(2, 4)
    print_intermediate_results()
```

```python

```
