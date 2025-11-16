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

# Алгоритмы на графах


## Цель работы


Изучение основных алгоритмов на графах.


Асонов Сергей ИУ10-36


# Задание 1

```python
from collections import deque

class Graph:
    def __init__(self, directed=False):
        self.adjacency_list = {}
        self.directed = directed
    
    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            return True
        return False
    
    def add_edge(self, vertex1, vertex2):
        if vertex1 not in self.adjacency_list:
            self.add_vertex(vertex1)
        if vertex2 not in self.adjacency_list:
            self.add_vertex(vertex2)
        
        if vertex2 not in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1].append(vertex2)
        
        if not self.directed and vertex1 not in self.adjacency_list[vertex2]:
            self.adjacency_list[vertex2].append(vertex1)
    
    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.adjacency_list and vertex2 in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1].remove(vertex2)
        
        if not self.directed and vertex2 in self.adjacency_list and vertex1 in self.adjacency_list[vertex2]:
            self.adjacency_list[vertex2].remove(vertex1)
    
    def remove_vertex(self, vertex):
        if vertex in self.adjacency_list:
            for adjacent_vertex in self.adjacency_list[vertex]:
                self.adjacency_list[adjacent_vertex].remove(vertex)
            del self.adjacency_list[vertex]
            return True
        return False
    
    def display(self):
        print("Граф (список смежности):")
        for vertex in sorted(self.adjacency_list.keys()):
            print(f"{vertex}: {sorted(self.adjacency_list[vertex])}")
    
    def dfs(self, start_vertex, target_vertex=None):
        if start_vertex not in self.adjacency_list:
            return []
        
        visited = set()
        stack = [start_vertex]
        result = []
        
        while stack:
            current_vertex = stack.pop()
            
            if current_vertex not in visited:
                visited.add(current_vertex)
                result.append(current_vertex)
                
                if target_vertex and current_vertex == target_vertex:
                    break
                
                for neighbor in reversed(self.adjacency_list[current_vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    def bfs(self, start_vertex, target_vertex=None):
        if start_vertex not in self.adjacency_list:
            return []
        
        visited = set()
        queue = deque([start_vertex])
        result = []
        
        while queue:
            current_vertex = queue.popleft()
            
            if current_vertex not in visited:
                visited.add(current_vertex)
                result.append(current_vertex)
                
                if target_vertex and current_vertex == target_vertex:
                    break
                
                for neighbor in self.adjacency_list[current_vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return result
    
    def find_path_dfs(self, start_vertex, target_vertex):
        if start_vertex not in self.adjacency_list or target_vertex not in self.adjacency_list:
            return None
        
        visited = set()
        stack = [(start_vertex, [start_vertex])]
        
        while stack:
            current_vertex, path = stack.pop()
            
            if current_vertex == target_vertex:
                return path
            
            if current_vertex not in visited:
                visited.add(current_vertex)
                
                for neighbor in reversed(self.adjacency_list[current_vertex]):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))
        
        return None
    
    def find_path_bfs(self, start_vertex, target_vertex):
        if start_vertex not in self.adjacency_list or target_vertex not in self.adjacency_list:
            return None
        
        visited = set()
        queue = deque([(start_vertex, [start_vertex])])
        
        while queue:
            current_vertex, path = queue.popleft()
            
            if current_vertex == target_vertex:
                return path
            
            if current_vertex not in visited:
                visited.add(current_vertex)
                
                for neighbor in self.adjacency_list[current_vertex]:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def get_vertices(self):
        return list(self.adjacency_list.keys())
    
    def get_edges(self):
        edges = []
        for vertex in self.adjacency_list:
            for neighbor in self.adjacency_list[vertex]:
                if not self.directed:
                    if (neighbor, vertex) not in edges:
                        edges.append((vertex, neighbor))
                else:
                    edges.append((vertex, neighbor))
        return edges

def test_graph_operations():
    """Тест основных операций с графом"""
    print("=== ТЕСТ 1: ОСНОВНЫЕ ОПЕРАЦИИ ===")
    g = Graph()
    
    # Добавление вершин и ребер
    g.add_vertex('A')
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('C', 'D')
    
    # Проверка структуры графа
    assert 'A' in g.get_vertices()
    assert 'B' in g.get_vertices()
    assert 'C' in g.get_vertices()
    assert ('A', 'B') in g.get_edges()
    assert ('B', 'C') in g.get_edges()
    
    print("✓ Тест основных операций пройден")

def test_graph_algorithms():
    """Тест алгоритмов обхода"""
    print("=== ТЕСТ 2: АЛГОРИТМЫ ОБХОДА ===")
    g = Graph()
    
    # Создаем граф: A-B-C-D, A-E
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('C', 'D')
    g.add_edge('A', 'E')
    
    # Тест DFS
    dfs_result = g.dfs('A')
    assert dfs_result[0] == 'A'  # Начинается с A
    assert set(dfs_result) == {'A', 'B', 'C', 'D', 'E'}  # Все вершины посещены
    
    # Тест BFS
    bfs_result = g.bfs('A')
    assert bfs_result[0] == 'A'
    assert set(bfs_result) == {'A', 'B', 'C', 'D', 'E'}
    
    # Тест поиска пути
    path = g.find_path_bfs('A', 'D')
    assert path == ['A', 'B', 'C', 'D'] or path == ['A', 'E', 'D']
    
    print("✓ Тест алгоритмов обхода пройден")

# Демонстрация работы
if __name__ == "__main__":
    print("=== ЗАДАНИЕ 1: КЛАСС GRAPH С АЛГОРИТМАМИ ОБХОДА ===")
    
    # Запуск тестов
    test_graph_operations()
    test_graph_algorithms()
    
    print("\n=== ДЕМОНСТРАЦИЯ РАБОТЫ ===")
    
    # Создаем граф
    g = Graph()
    
    # Добавляем вершины и ребра
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('C', 'E')
    g.add_edge('D', 'E')
    g.add_edge('E', 'F')
    
    # Отображаем граф
    g.display()
    
    # Тестируем алгоритмы обхода
    print(f"\nDFS обход от 'A': {g.dfs('A')}")
    print(f"BFS обход от 'A': {g.bfs('A')}")
    
    # Тестируем поиск путей
    print(f"\nПоиск пути от 'A' до 'F' (DFS): {g.find_path_dfs('A', 'F')}")
    print(f"Поиск пути от 'A' до 'F' (BFS): {g.find_path_bfs('A', 'F')}")
    
    print("\n✓ Все тесты пройдены успешно!")
```

## Задание 2 

```python
from collections import deque

class SimpleGraph:
    def __init__(self):
        self.adjacency_list = {}
    
    def add_vertex(self, vertex):
        """Добавить вершину"""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            print(f"✓ Вершина '{vertex}' добавлена")
        else:
            print(f"✗ Вершина '{vertex}' уже существует")
    
    def add_edge(self, vertex1, vertex2):
        """Добавить ребро между двумя вершинами"""
        if vertex1 not in self.adjacency_list:
            self.add_vertex(vertex1)
        if vertex2 not in self.adjacency_list:
            self.add_vertex(vertex2)
        
        if vertex2 not in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1].append(vertex2)
            self.adjacency_list[vertex2].append(vertex1)  # Неориентированный граф
            print(f"✓ Ребро между '{vertex1}' и '{vertex2}' добавлено")
        else:
            print(f"✗ Ребро между '{vertex1}' и '{vertex2}' уже существует")
    
    def show_graph(self):
        """Показать граф"""
        if not self.adjacency_list:
            print("Граф пустой")
            return
        
        print("\nТекущий граф:")
        for vertex in sorted(self.adjacency_list.keys()):
            neighbors = sorted(self.adjacency_list[vertex])
            print(f"  {vertex} соединен с: {neighbors}")
    
    def bfs(self, start_vertex):
        """Обход в ширину (BFS)"""
        if start_vertex not in self.adjacency_list:
            print(f"✗ Вершина '{start_vertex}' не найдена")
            return []
        
        visited = set()
        queue = deque([start_vertex])
        result = []
        
        print(f"\nBFS обход от '{start_vertex}':", end=" ")
        
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                result.append(current)
                print(current, end=" ")
                
                for neighbor in self.adjacency_list[current]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        print()
        return result
    
    def dfs(self, start_vertex):
        """Обход в глубину (DFS)"""
        if start_vertex not in self.adjacency_list:
            print(f"✗ Вершина '{start_vertex}' не найдена")
            return []
        
        visited = set()
        stack = [start_vertex]
        result = []
        
        print(f"\nDFS обход от '{start_vertex}':", end=" ")
        
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                result.append(current)
                print(current, end=" ")
                
                for neighbor in reversed(self.adjacency_list[current]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        print()
        return result
    
    def find_path(self, start_vertex, target_vertex):
        """Найти путь между двумя вершинами"""
        if start_vertex not in self.adjacency_list:
            print(f"✗ Вершина '{start_vertex}' не найдена")
            return None
        if target_vertex not in self.adjacency_list:
            print(f"✗ Вершина '{target_vertex}' не найдена")
            return None
        
        visited = set()
        queue = deque([(start_vertex, [start_vertex])])
        
        while queue:
            current, path = queue.popleft()
            
            if current == target_vertex:
                print(f"✓ Путь от '{start_vertex}' до '{target_vertex}': {' -> '.join(path)}")
                return path
            
            if current not in visited:
                visited.add(current)
                
                for neighbor in self.adjacency_list[current]:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
        
        print(f"✗ Путь от '{start_vertex}' до '{target_vertex}' не найден")
        return None

def test_simple_graph():
    """Простой тест графа"""
    print("=== ПРОСТОЙ ТЕСТ ===")
    g = SimpleGraph()
    
    # Создаем простой граф
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_vertex('C')
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    
    # Проверяем обходы
    g.bfs('A')
    g.dfs('A')
    g.find_path('A', 'C')
    
    print("✓ Простой тест завершен")

def test_path_finding():
    """Тест поиска пути"""
    print("\n=== ТЕСТ ПОИСКА ПУТИ ===")
    g = SimpleGraph()
    
    # Создаем граф: A-B-C-D, A-E
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('C', 'D')
    g.add_edge('A', 'E')
    
    # Ищем путь
    path = g.find_path('A', 'D')
    assert path is not None, "Путь должен существовать"
    assert path[0] == 'A', "Начало пути должно быть A"
    assert path[-1] == 'D', "Конец пути должен быть D"
    
    print("✓ Тест поиска пути завершен")

def main():
    """Главное меню приложения"""
    graph = SimpleGraph()
    
    print("=== ПРОСТОЕ ПРИЛОЖЕНИЕ ДЛЯ РАБОТЫ С ГРАФАМИ ===")
    print("Создавайте графы и изучайте алгоритмы обхода!")
    
    # Создаем пример графа для демонстрации
    print("\nСоздаем пример графа...")
    graph.add_edge('Москва', 'Санкт-Петербург')
    graph.add_edge('Москва', 'Казань')
    graph.add_edge('Санкт-Петербург', 'Псков')
    graph.add_edge('Казань', 'Уфа')
    graph.show_graph()
    
    while True:
        print("\n" + "="*50)
        print("ГЛАВНОЕ МЕНЮ:")
        print("1. Показать граф")
        print("2. Добавить вершину")
        print("3. Добавить ребро")
        print("4. Обход в ширину (BFS)")
        print("5. Обход в глубину (DFS)")
        print("6. Найти путь")
        print("7. Создать новый пример")
        print("0. Выход")
        print("="*50)
        
        choice = input("Выберите действие (0-7): ").strip()
        
        if choice == "1":
            graph.show_graph()
            
        elif choice == "2":
            vertex = input("Введите имя вершины: ").strip()
            graph.add_vertex(vertex)
            
        elif choice == "3":
            v1 = input("Введите первую вершину: ").strip()
            v2 = input("Введите вторую вершину: ").strip()
            graph.add_edge(v1, v2)
            
        elif choice == "4":
            start = input("Введите начальную вершину: ").strip()
            graph.bfs(start)
            
        elif choice == "5":
            start = input("Введите начальную вершину: ").strip()
            graph.dfs(start)
            
        elif choice == "6":
            start = input("Введите начальную вершину: ").strip()
            target = input("Введите конечную вершину: ").strip()
            graph.find_path(start, target)
            
        elif choice == "7":
            graph = SimpleGraph()
            print("Создан новый пустой граф")
            
        elif choice == "0":
            print("До свидания!")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    # Запускаем тесты
    test_simple_graph()
    test_path_finding()
    
    print("\n✓ Все тесты пройдены!")
    print("Запуск приложения...\n")
    
    # Запускаем приложение
    main()
```

## Задание 3 

```python
from collections import deque

class Graph:
    def __init__(self, directed=False):
        self.adjacency_list = {}
        self.directed = directed
    
    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            return True
        return False
    
    def add_edge(self, vertex1, vertex2):
        if vertex1 not in self.adjacency_list:
            self.add_vertex(vertex1)
        if vertex2 not in self.adjacency_list:
            self.add_vertex(vertex2)
        
        if vertex2 not in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1].append(vertex2)
        
        if not self.directed and vertex1 not in self.adjacency_list[vertex2]:
            self.adjacency_list[vertex2].append(vertex1)
    
    def display(self):
        print("Граф (список смежности):")
        for vertex in sorted(self.adjacency_list.keys()):
            print(f"{vertex}: {sorted(self.adjacency_list[vertex])}")
    
    def bfs(self, start_vertex):
        if start_vertex not in self.adjacency_list:
            return []
        
        visited = set()
        queue = deque([start_vertex])
        result = []
        
        while queue:
            current_vertex = queue.popleft()
            
            if current_vertex not in visited:
                visited.add(current_vertex)
                result.append(current_vertex)
                
                for neighbor in self.adjacency_list[current_vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return result
    
    def get_vertices(self):
        return list(self.adjacency_list.keys())

def analyze_connectivity(graph):
    """
    Анализ компонент связности графа
    Возвращает список компонент связности
    """
    if not graph:
        return []
    
    visited = set()
    components = []
    
    for vertex in graph.get_vertices():
        if vertex not in visited:
            component = graph.bfs(vertex)
            components.append(component)
            visited.update(component)
    
    return components

def is_connected_graph(graph):
    """
    Проверка, является ли граф связным
    """
    components = analyze_connectivity(graph)
    return len(components) == 1

def test_connected_graph():
    """Тест связного графа"""
    print("=== ТЕСТ 1: СВЯЗНЫЙ ГРАФ ===")
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    
    components = analyze_connectivity(g)
    assert len(components) == 1, "Связный граф должен иметь 1 компоненту"
    assert is_connected_graph(g) == True, "Граф должен быть связным"
    
    print("✓ Тест связного графа пройден")

def test_disconnected_graph():
    """Тест несвязного графа"""
    print("=== ТЕСТ 2: НЕСВЯЗНЫЙ ГРАФ ===")
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(4, 5)
    g.add_edge(5, 6)
    
    components = analyze_connectivity(g)
    assert len(components) == 2, "Несвязный граф должен иметь 2 компоненты"
    assert is_connected_graph(g) == False, "Граф не должен быть связным"
    
    # Проверяем состав компонент
    component_sizes = [len(comp) for comp in components]
    assert 3 in component_sizes, "Должна быть компонента размера 3"
    
    print("✓ Тест несвязного графа пройден")

def demonstrate_analysis():
    """
    Демонстрация работы анализа связности
    """
    print("=== ЗАДАНИЕ 3: АНАЛИЗ КОМПОНЕНТ СВЯЗНОСТИ ===")
    
    # Создаем тестовые графы
    print("\n1. Связный граф:")
    g1 = Graph()
    g1.add_edge('A', 'B')
    g1.add_edge('A', 'C')
    g1.add_edge('B', 'D')
    g1.add_edge('C', 'E')
    g1.add_edge('D', 'E')
    g1.display()
    
    components1 = analyze_connectivity(g1)
    print(f"Компоненты связности: {components1}")
    print(f"Граф связный: {is_connected_graph(g1)}")
    
    print("\n2. Несвязный граф (2 компоненты):")
    g2 = Graph()
    g2.add_edge('A', 'B')
    g2.add_edge('B', 'C')
    g2.add_edge('D', 'E')
    g2.add_edge('E', 'F')
    g2.display()
    
    components2 = analyze_connectivity(g2)
    print(f"Компоненты связности: {components2}")
    print(f"Граф связный: {is_connected_graph(g2)}")

if __name__ == "__main__":
    # Запуск тестов
    test_connected_graph()
    test_disconnected_graph()
    
    print("\n✓ Все тесты пройдены! Демонстрация работы...")
    
    # Демонстрация работы
    demonstrate_analysis()
```

## Задание 4: Поиск кратчайшего пути BFS (1→6) 

```python
import heapq

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    queue = [(0, start)]
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        if current_distance > distances[current_node]:
            continue
            
        if current_node == end:
            break
            
        for neighbor, weight in graph.get(current_node, []):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    
    # Восстанавливаем путь
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    if distances[end] == float('inf'):
        return None, float('inf')
    return path, distances[end]

# Ориентированный граф
graph = {
    1: [(2, 1), (4, 8), (5, 25), (7, 20)],
    2: [(3, 2), (7, 15)],
    3: [(6, 3)],
    4: [(5, 9)],
    5: [(7, 6)],
    6: [(7, 4)],
    7: []
}

start_vertex = 1
end_vertex = 6

path, distance = dijkstra(graph, start_vertex, end_vertex)

if path:
    print(f"Кратчайший путь из {start_vertex} в {end_vertex}: {' -> '.join(map(str, path))}")
    print(f"Длина пути: {distance}")
else:
    print(f"Пути из {start_vertex} в {end_vertex} не существует")
```

## Задание 5: Алгоритм Дейкстры (2→8)

```python
import heapq

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    queue = [(0, start)]
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        if current_distance > distances[current_node]:
            continue
            
        if current_node == end:
            break
            
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    return path, distances[end]


graph = {
    1: [(2, 12), (7, 2), (3, 20)],
    2: [(1, 12), (8, 12)],
    3: [(1, 20), (8, 3), (4, 17), (5, 12)],
    4: [(3, 17), (5, 5), (7, 11), (6, 6)],
    5: [(3, 12), (4, 5), (7, 16), (6, 13)],
    6: [(4, 6), (5, 13), (7, 4), (8, 17)],
    7: [(1, 2), (4, 11), (5, 16), (6, 4)],
    8: [(2, 12), (3, 3), (6, 17)]
}

start_vertex = 2
end_vertex = 8

path, distance = dijkstra(graph, start_vertex, end_vertex)

print(f"Кратчайший путь из {start_vertex} в {end_vertex}: {' -> '.join(map(str, path))}")
print(f"Длина пути: {distance}")
```

## Задание 6

```python
import heapq

class DijkstraAlgorithm:
    def __init__(self, graph):
        """
        Инициализация алгоритма Дейкстры
        
        Args:
            graph (dict): Граф в формате {вершина: [(сосед, вес), ...]}
        """
        self.graph = graph
        self.distances = {}
        self.previous = {}
        self.visited = set()
    
    def find_shortest_path(self, start, end):
        """
        Поиск кратчайшего пути между вершинами
        
        Args:
            start: Начальная вершина
            end: Конечная вершина
        
        Returns:
            tuple: (путь, длина) или (None, inf) если путь не существует
        """
        # Проверка существования вершин
        if start not in self.graph or end not in self.graph:
            return None, float('inf')
        
        # Инициализация
        self.distances = {node: float('inf') for node in self.graph}
        self.previous = {node: None for node in self.graph}
        self.distances[start] = 0
        self.visited = set()
        
        # Очередь с приоритетом (мин-куча)
        priority_queue = [(0, start)]
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            # Пропускаем устаревшие записи
            if current_distance > self.distances[current_node]:
                continue
                
            # Если достигли конечной вершины
            if current_node == end:
                break
                
            self.visited.add(current_node)
            
            # Обработка соседей текущей вершины
            for neighbor, weight in self.graph.get(current_node, []):
                if neighbor in self.visited:
                    continue
                    
                new_distance = current_distance + weight
                
                # Обновление расстояния если нашли короче
                if new_distance < self.distances[neighbor]:
                    self.distances[neighbor] = new_distance
                    self.previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))
        
        return self._reconstruct_path(start, end)
    
    def _reconstruct_path(self, start, end):
        """Восстановление пути от конечной вершины к начальной"""
        if self.distances[end] == float('inf'):
            return None, float('inf')
            
        path = []
        current = end
        
        # Восстанавливаем путь в обратном порядке
        while current is not None:
            path.append(current)
            current = self.previous[current]
        
        path.reverse()
        
        # Проверка что путь начинается с start
        if path[0] != start:
            return None, float('inf')
            
        return path, self.distances[end]
    
    def print_path_info(self, start, end):
        """Вывод информации о пути"""
        path, distance = self.find_shortest_path(start, end)
        
        if path:
            print(f"Кратчайший путь из {start} в {end}:")
            print(" → ".join(map(str, path)))
            print(f"Длина пути: {distance}")
            print(f"Количество рёбер: {len(path) - 1}")
        else:
            print(f"Пути из {start} в {end} не существует")


# Граф из задания 5 (ориентированный)
graph_task5 = {
    1: [(2, 12), (7, 2), (3, 20)],
    2: [(1, 12), (8, 12)],
    3: [(1, 20), (8, 3), (4, 17), (5, 12)],
    4: [(3, 17), (5, 5), (7, 11), (6, 6)],
    5: [(3, 12), (4, 5), (7, 16), (6, 13)],
    6: [(4, 6), (5, 13), (7, 4), (8, 17)],
    7: [(1, 2), (4, 11), (5, 16), (6, 4)],
    8: [(2, 12), (3, 3), (6, 17)]
}

def main():
    print("Алгоритм Дейкстры - поиск кратчайшего пути")
    print("=" * 50)
    
    # Создаем экземпляр алгоритма
    dijkstra = DijkstraAlgorithm(graph_task5)
    
    # Поиск пути между вершинами 2 и 8
    start_vertex = 2
    end_vertex = 8
    
    print(f"Анализ графа:")
    print(f"Вершины: {list(graph_task5.keys())}")
    print(f"Рёбра:")
    for node in sorted(graph_task5.keys()):
        for neighbor, weight in graph_task5[node]:
            print(f"  {node} → {neighbor} (вес: {weight})")
    print()
    
    # Находим и выводим путь
    dijkstra.print_path_info(start_vertex, end_vertex)
    
    # Дополнительная информация
    print(f"\nРасстояния от вершины {start_vertex}:")
    for node in sorted(dijkstra.distances.keys()):
        dist = dijkstra.distances[node]
        if dist == float('inf'):
            print(f"  до {node}: недостижима")
        else:
            print(f"  до {node}: {dist}")

if __name__ == "__main__":
    main()
```

```python

```
