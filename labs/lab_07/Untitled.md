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

## Алгоритмы на графах

### Задание 1

```python
from collections import deque
import heapq

class Graph:
    def __init__(self, directed=False):
        self.vertices = {}
        self.directed = directed
    
    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = {}
    
    def add_edge(self, vertex1, vertex2, weight=1):
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        
        self.vertices[vertex1][vertex2] = weight
        if not self.directed:
            self.vertices[vertex2][vertex1] = weight
    
    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.vertices and vertex2 in self.vertices[vertex1]:
            del self.vertices[vertex1][vertex2]
            if not self.directed and vertex2 in self.vertices and vertex1 in self.vertices[vertex2]:
                del self.vertices[vertex2][vertex1]
    
    def remove_vertex(self, vertex):
        if vertex in self.vertices:
            for neighbor in list(self.vertices[vertex].keys()):
                self.remove_edge(vertex, neighbor)
            del self.vertices[vertex]
    
    def get_vertices(self):
        return list(self.vertices.keys())
    
    def get_edges(self):
        edges = []
        for vertex in self.vertices:
            for neighbor, weight in self.vertices[vertex].items():
                if self.directed:
                    edges.append((vertex, neighbor, weight))
                else:
                    if vertex < neighbor:
                        edges.append((vertex, neighbor, weight))
        return edges
    
    def bfs(self, start_vertex):
        """Поиск в ширину"""
        if start_vertex not in self.vertices:
            return []
        
        visited = set()
        queue = deque([start_vertex])
        result = []
        
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                for neighbor in self.vertices[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return result
    
    def dfs(self, start_vertex):
        """Поиск в глубину (итеративный)"""
        if start_vertex not in self.vertices:
            return []
        
        visited = set()
        stack = [start_vertex]
        result = []
        
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                for neighbor in reversed(list(self.vertices[vertex].keys())):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    def dijkstra(self, start_vertex, end_vertex):
        """Алгоритм Дейкстры для поиска кратчайшего пути"""
        if start_vertex not in self.vertices or end_vertex not in self.vertices:
            return [], float('inf')
        
        distances = {vertex: float('inf') for vertex in self.vertices}
        previous = {vertex: None for vertex in self.vertices}
        distances[start_vertex] = 0
        
        pq = [(0, start_vertex)]
        
        while pq:
            current_distance, current_vertex = heapq.heappop(pq)
            
            if current_distance > distances[current_vertex]:
                continue
            
            if current_vertex == end_vertex:
                break
            
            for neighbor, weight in self.vertices[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))
        
        path = []
        current = end_vertex
        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        
        if path[0] != start_vertex:
            return [], float('inf')
        
        return path, distances[end_vertex]
    
    def has_eulerian_cycle(self):
        """Проверка наличия эйлерова цикла"""
        if self.directed:
            for vertex in self.vertices:
                in_degree = sum(1 for v in self.vertices if vertex in self.vertices[v])
                out_degree = len(self.vertices[vertex])
                if in_degree != out_degree:
                    return False
            return True
        else:
            for vertex in self.vertices:
                if len(self.vertices[vertex]) % 2 != 0:
                    return False
            return True
    
    def find_eulerian_cycle(self):
        """Поиск эйлерова цикла (алгоритм Флёри)"""
        if not self.has_eulerian_cycle():
            return []
        
        graph_copy = {v: dict(neighbors) for v, neighbors in self.vertices.items()}
        
        start_vertex = next(iter(self.vertices.keys()))
        stack = [start_vertex]
        cycle = []
        
        while stack:
            current_vertex = stack[-1]
            
            if graph_copy[current_vertex]:
                next_vertex = next(iter(graph_copy[current_vertex].keys()))
                stack.append(next_vertex)
                del graph_copy[current_vertex][next_vertex]
                if not self.directed:
                    del graph_copy[next_vertex][current_vertex]
            else:
                cycle.append(stack.pop())
        
        return cycle[::-1]
    
    def hamiltonian_cycle_util(self, path, pos):
        """Вспомогательная функция для поиска гамильтонова цикла"""
        if pos == len(self.vertices):
            last_vertex = path[pos - 1]
            first_vertex = path[0]
            if first_vertex in self.vertices[last_vertex]:
                return True
            else:
                return False
        
        for v in self.vertices:
            if v not in path:
                if pos == 0 or path[pos - 1] in self.vertices and v in self.vertices[path[pos - 1]]:
                    path[pos] = v
                    if self.hamiltonian_cycle_util(path, pos + 1):
                        return True
                    path[pos] = -1
        
        return False
    
    def find_hamiltonian_cycle(self):
        """Поиск гамильтонова цикла"""
        if len(self.vertices) == 0:
            return []
        
        path = [-1] * len(self.vertices)
        path[0] = next(iter(self.vertices.keys()))
        
        if not self.hamiltonian_cycle_util(path, 1):
            return []
        
        return path
    
    def __str__(self):
        result = "Граф:\n"
        for vertex in self.vertices:
            result += f"{vertex}: {self.vertices[vertex]}\n"
        return result
```

### Задание 2

```python
def main():
    """Диалоговое приложение для работы с графом"""
    graph = Graph(directed=False)
    
    while True:
        print("\n=== МЕНЮ РАБОТЫ С ГРАФОМ ===")
        print("1. Добавить вершину")
        print("2. Добавить ребро")
        print("3. Удалить вершину")
        print("4. Удалить ребро")
        print("5. Показать граф")
        print("6. Обход в ширину (BFS)")
        print("7. Обход в глубину (DFS)")
        print("8. Алгоритм Дейкстры")
        print("9. Поиск эйлерова цикла")
        print("10. Поиск гамильтонова цикла")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ").strip()
        
        actions = {
            '1': lambda: add_vertex_handler(graph),
            '2': lambda: add_edge_handler(graph),
            '3': lambda: remove_vertex_handler(graph),
            '4': lambda: remove_edge_handler(graph),
            '5': lambda: show_graph_handler(graph),
            '6': lambda: bfs_handler(graph),
            '7': lambda: dfs_handler(graph),
            '8': lambda: dijkstra_handler(graph),
            '9': lambda: eulerian_cycle_handler(graph),
            '10': lambda: hamiltonian_cycle_handler(graph),
            '0': lambda: exit_handler()
        }
        
        if choice in actions:
            actions[choice]()
        else:
            print("Неверный выбор. Попробуйте снова.")


def add_vertex_handler(graph):
    vertex = input("Введите название вершины: ").strip()
    graph.add_vertex(vertex)
    print(f"Вершина '{vertex}' добавлена")


def add_edge_handler(graph):
    v1 = input("Введите первую вершину: ").strip()
    v2 = input("Введите вторую вершину: ").strip()
    try:
        weight = float(input("Введите вес ребра (по умолчанию 1): ").strip() or 1)
    except ValueError:
        weight = 1
    graph.add_edge(v1, v2, weight)
    print(f"Ребро '{v1}' - '{v2}' с весом {weight} добавлено")


def remove_vertex_handler(graph):
    vertex = input("Введите вершину для удаления: ").strip()
    graph.remove_vertex(vertex)
    print(f"Вершина '{vertex}' удалена")


def remove_edge_handler(graph):
    v1 = input("Введите первую вершину: ").strip()
    v2 = input("Введите вторую вершину: ").strip()
    graph.remove_edge(v1, v2)
    print(f"Ребро '{v1}' - '{v2}' удалено")


def show_graph_handler(graph):
    print("\nТекущий граф:")
    print(graph)
    print("Вершины:", graph.get_vertices())
    print("Рёбра:", graph.get_edges())


def bfs_handler(graph):
    start = input("Введите начальную вершину для BFS: ").strip()
    result = graph.bfs(start)
    print(f"BFS обход: {result}")


def dfs_handler(graph):
    start = input("Введите начальную вершину для DFS: ").strip()
    result = graph.dfs(start)
    print(f"DFS обход: {result}")


def dijkstra_handler(graph):
    start = input("Введите начальную вершину: ").strip()
    end = input("Введите конечную вершину: ").strip()
    path, distance = graph.dijkstra(start, end)
    if path:
        print(f"Кратчайший путь: {' -> '.join(path)}")
        print(f"Длина пути: {distance}")
    else:
        print("Путь не найден")


def eulerian_cycle_handler(graph):
    if graph.has_eulerian_cycle():
        cycle = graph.find_eulerian_cycle()
        print(f"Эйлеров цикл: {' -> '.join(cycle)}")
    else:
        print("Эйлеров цикл не существует")


def hamiltonian_cycle_handler(graph):
    cycle = graph.find_hamiltonian_cycle()
    if cycle:
        print(f"Гамильтонов цикл: {' -> '.join(cycle)}")
    else:
        print("Гамильтонов цикл не найден")


def exit_handler():
    print("Выход из программы")
    exit()


if __name__ == "__main__":
    main()
```

### Задание 3
### Задание 4

```python
def task_4():
    g = Graph(directed=True)
    
    edges = [
        ('1', '3', 13), ('1', '2', 2), ('1', '5', 17), ('1', '4', 25),
        ('2', '4', 3), ('2', '5', 6),
        ('3', '4', 1), ('3', '6', 7),
        ('4', '6', 4), ('4', '5', 1), ('4', '7', 35),
        ('5', '4', 1), ('5', '7', 20),
        ('6', '7', 5)
    ]
    
    for v1, v2, w in edges:
        g.add_edge(v1, v2, w)
    
    print("Граф для задания 4:")
    print(g)
    
    start, end = '1', '6'
    path, distance = g.dijkstra(start, end)
    
    print(f"\nКратчайший путь от {start} до {end}:")
    if path:
        print(f"Путь: {' -> '.join(path)}")
        print(f"Длина пути: {distance}")
        
        print("\nВсе рёбра графа:")
        for edge in g.get_edges():
            print(f"{edge[0]} -> {edge[1]} (вес: {edge[2]})")
    else:
        print("Путь не найден")
    
    return path, distance

print("=== ЗАДАНИЕ 4 ===")
path, distance = task_4()
```

### Задание 5

```python
def task_5():
    g = Graph(directed=True)
    
    edges = [
        ('1', '2', 14), ('1', '6', 8),
        ('2', '3', 5), ('2', '6', 2), ('2', '4', 10), ('2', '5', 2), ('2', '8', 9),
        ('3', '2', 5), ('3', '8', 11),  
        ('4', '5', 3), ('4', '6', 6), ('4', '7', 5),
        ('5', '7', 8), ('5', '8', 1),
        ('6', '7', 5),
        ('7', '8', 7)
    ]
    
    for v1, v2, w in edges:
        g.add_edge(v1, v2, w)
    
    print("Граф для задания 5:")
    print(g)
    
    start, end = '3', '8'
    path, distance = g.dijkstra(start, end)
    
    print(f"\nКратчайший путь от {start} до {end}:")
    if path:
        print(f"Путь: {' -> '.join(path)}")
        print(f"Длина пути: {distance}")
    else:
        print("Путь не найден")
    
    return path, distance

print("=== ЗАДАНИЕ 5 ===")
path, distance = task_5()
```

### Задание 6

```python
import heapq

def dijkstra_algorithm(graph, start, end):
    distances = {vertex: float('inf') for vertex in graph.vertices}
    previous = {vertex: None for vertex in graph.vertices}
    distances[start] = 0
    
    priority_queue = [(0, start)]
    
    print("АЛГОРИТМ ДЕЙКСТРЫ - ШАГИ:")
    
    step = 1
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_vertex]:
            continue
            
        print(f"\nШаг {step}: Обрабатываем вершину '{current_vertex}'")
        print(f"   Текущее расстояние: {current_distance}")
        
        if current_vertex == end:
            print(f"   Достигнута конечная вершина '{end}'")
            break
        
        for neighbor, weight in graph.vertices[current_vertex].items():
            distance = current_distance + weight
            
            print(f"   Проверяем {current_vertex} -> {neighbor} (вес: {weight})")
            print(f"   Новое расстояние до {neighbor}: {distance}")
            
            if distance < distances[neighbor]:
                old_dist = distances[neighbor]
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
                print(f"   Обновлено: {neighbor}: {old_dist} -> {distance}")
            else:
                print(f"   Не обновляем (текущее: {distances[neighbor]})")
        
        step += 1
    
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    
    path.reverse()
    
    if path[0] != start:
        return [], float('inf')
    
    return path, distances[end]

def detailed_dijkstra_demo():
    g = Graph(directed=True)
    
    edges = [
        ('1', '2', 14), ('1', '6', 8),
        ('2', '3', 5), ('2', '6', 2), ('2', '4', 10), ('2', '5', 2), ('2', '8', 9),
        ('3', '2', 5), ('3', '8', 11),
        ('4', '5', 3), ('4', '6', 6), ('4', '7', 5),
        ('5', '7', 8), ('5', '8', 1),
        ('6', '7', 5),
        ('7', '8', 7)
    ]
    
    for v1, v2, w in edges:
        g.add_edge(v1, v2, w)
    
    print("ДЕТАЛЬНАЯ РЕАЛИЗАЦИЯ АЛГОРИТМА ДЕЙКСТРЫ")
    print("=" * 40)
    
    print("\nСтруктура графа:")
    for vertex in sorted(g.vertices.keys()):
        neighbors = g.vertices[vertex]
        if neighbors:
            connections = ", ".join([f"{n}({w})" for n, w in neighbors.items()])
            print(f"   {vertex} -> [{connections}]")
    
    start, end = '3', '8'
    print(f"\nЦель: Найти кратчайший путь от '{start}' до '{end}'")
    
    path, distance = dijkstra_algorithm(g, start, end)
    
    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТЫ:")
    print("=" * 40)
    
    if path:
        print(f"Кратчайший путь найден!")
        print(f"Путь: {' -> '.join(path)}")
        print(f"Длина: {distance}")
        
        print(f"\nПодробный расчет:")
        total = 0
        for i in range(len(path) - 1):
            segment_distance = g.vertices[path[i]][path[i+1]]
            total += segment_distance
            print(f"   {path[i]} -> {path[i+1]} = {segment_distance}")
        print(f"   Общая длина = {total}")
    else:
        print("Путь не найден")
    
    print(f"\nСравнение с другими путями:")
    possible_paths = [
        (['3', '8'], 11),
        (['3', '2', '8'], 5 + 9),
        (['3', '2', '5', '8'], 5 + 2 + 1)
    ]
    
    for p, dist in possible_paths:
        status = "ЛУЧШИЙ" if p == path else ""
        print(f"   {' -> '.join(p):15} = {dist} {status}")
    
    return path, distance

print("=== ЗАДАНИЕ 6 ===")
path, distance = detailed_dijkstra_demo()
```

```python

```
