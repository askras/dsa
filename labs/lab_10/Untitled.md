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

## Динамическое программирование
### Задача о рюкзаке с возможностью дробить предметы (Fractional Knapsack)

```python
def fractional_knapsack(items, capacity):
    items.sort(key=lambda x: x.price / x.weight, reverse=True)
    total_value = 0.0
    for item in items:
        if capacity >= item.weight:
            total_value += item.price
            capacity -= item.weight
        else:
            total_value += item.price * (capacity / item.weight)
            break
    return total_value

class Item:
    def __init__(self, price, weight):
        self.price = price
        self.weight = weight

items = [Item(60, 15), Item(90, 30), Item(100, 50)]
capacity = 80
print(f"Максимальная стоимость (дробный рюкзак): {fractional_knapsack(items, capacity)}")
```

### Задача о покрытии отрезками (Interval Covering Problem)

```python
def interval_covering(segments, target_start, target_end):
    segments.sort(key=lambda x: x[1])
    result = []
    current_pos = target_start
    i = 0
    while current_pos < target_end:
        best_end = current_pos
        while i < len(segments) and segments[i][0] <= current_pos:
            best_end = max(best_end, segments[i][1])
            i += 1
        if best_end == current_pos:
            return []
        result.append((current_pos, best_end))
        current_pos = best_end
    return result

segments = [(1, 4), (2, 5), (3, 6), (5, 7), (6, 8)]
target = (1, 8)
print(f"Минимальное покрытие: {interval_covering(segments, *target)}")
```

### Задача о нахождении наименьшего пути (Floyd–Warshall)

```python
def floyd_warshall(graph):
    n = len(graph)
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        for j, w in graph[i]:
            dist[i][j] = w

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

graph = [
    [(1, 3), (2, 5)],
    [(2, 1)],
    []
]
print("Матрица кратчайших путей:")
for row in floyd_warshall(graph):
    print(row)
```

### Задача о размене монет (Coin Change, DP-версия)

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

coins = [1, 5, 11]
amount = 15
print(f"Минимальное количество монет для суммы {amount}: {coin_change(coins, amount)}")
```

### Генерация разбиений множества (комбинаторный алгоритм)

```python
def set_partitions(elements):
    result = []

    def backtrack(idx, current_partition):
        if idx == len(elements):
            result.append([list(subset) for subset in current_partition])
            return
        for i in range(len(current_partition)):
            current_partition[i].append(elements[idx])
            backtrack(idx + 1, current_partition)
            current_partition[i].pop()
        current_partition.append([elements[idx]])
        backtrack(idx + 1, current_partition)
        current_partition.pop()

    backtrack(0, [])
    return result

print("Разбиения множества [1, 2, 3]:")
for part in set_partitions([1, 2, 3]):
    print(part)
```

### Оптимизация многомерной функции (генетический алгоритм)

```python
import random

def fitness_function(individual):
    x, y = individual
    return -x**2 - y**2 + 10

def initialize_population(size, bounds=(-10, 10)):
    return [(random.uniform(*bounds), random.uniform(*bounds)) for _ in range(size)]

def tournament_selection(population, tournament_size=5):
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=fitness_function)

def crossover(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def mutate(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        return (individual[0] + random.gauss(0, 0.5), individual[1] + random.gauss(0, 0.5))
    return individual

def genetic_algorithm(generations=100, pop_size=50):
    population = initialize_population(pop_size)
    for _ in range(generations):
        new_pop = []
        for _ in range(pop_size):
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)
            child = crossover(p1, p2)
            child = mutate(child)
            new_pop.append(child)
        population = new_pop
    return max(population, key=fitness_function)

best = genetic_algorithm()
print(f"Лучшее решение: {best}, значение функции: {fitness_function(best)}")
```

```python

```
