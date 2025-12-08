# Лабораторная работа 7
# Алгоритмы на графах
## Цель работы
Изучение основных алгоритмов на графах.
## Задачи лабораторной работы
1. Изучение основных алгоритмов на графах
2. Реализация класса граф и различных алгоритмов его обхода
3. Применение алгоритомв для решения задачи
## Словесная постановка задачи
1. Изучить как происходит обход графа
2. Реализовать свой класс граф и оболочку для пользователя
3. Применить этот класс для решения задачи
## Реализация алгоритмов на графах
Первая часть реализует класс Graph
``` Python
#1
class Graph:
    def __init__(self, vershini=None):
        if vershini:
            self.vershini = vershini
        else:
            self.vershini = []
        self.spisok_smeznosti = {vershina: [] for vershina in self.vershini}
        self.vesa_reber = {}

    def add_vershina(self, vershina):
        if vershina not in self.spisok_smeznosti:
            self.vershini.append(vershina)
            self.spisok_smeznosti[vershina] = []
    def add_rebro(self, u, v, ves):
        if u not in self.spisok_smeznosti:
            self.add_vershina(u)
        if v not in self.spisok_smeznosti:
            self.add_vershina(v)
        if v not in self.spisok_smeznosti[u]:
            self.spisok_smeznosti[u].append(v)
        if u not in self.spisok_smeznosti[v]:
            self.spisok_smeznosti[v].append(u)
        self.vesa_reber[(u, v)] = ves
        self.vesa_reber[(v, u)] = ves

    def delete_vershina(self, vershina):
        for sosed in self.spisok_smeznosti[vershina]:
            self.spisok_smeznosti[vershina].remove(vershina)
            if (vershina, sosed) in self.vesa_reber:
                del self.vesa_reber[(vershina, sosed)]
            if (sosed, vershina) in self.vesa_reber:
                del self.vesa_reber[(sosed, vershina)]
        del self.spisok_smeznosti[vershina]
        self.vershini.remove(vershina)
    def delete_rebro(self, u, v):
        self.spisok_smeznosti[u].remove(v)
        self.spisok_smeznosti[v].remove(u)
        if (u, v) in self.vesa_reber:
            del self.vesa_reber[(u, v)]
        if (v, u) in self.vesa_reber:
            del self.vesa_reber[(v, u)]

    def get_vershini(self):
        return self.vershini
    def get_stepen_vershini(self, vershina):
        return len(self.spisok_smeznosti[vershina])
    def get_rebra(self):
        rebra = []
        visited_rebra = set()
        
        for u in self.spisok_smeznosti:
            for v in self.spisok_smeznosti[u]:
                rebro = tuple(sorted((u, v)))
                if rebro not in visited_rebra:
                    rebra.append((u, v))
                    visited_rebra.add(rebro)
        return rebra
    def get_ves_rebra(self, u, v):
        return self.vesa_reber.get((u, v), 1)
    
    def set_ves_rebra(self, u, v, ves):
        self.vesa_reber[(u, v)] = ves
        self.vesa_reber[(v, u)] = ves

    def display(self):
        print("Вершины:", self.vershini)
        print("Рёбра:")
        rebra = self.get_rebra()
        for rebro in rebra:
            print(f"  {rebro[0]} - {rebro[1]}")
        print("\nСписок смежности:")
        for vershina in sorted(self.vershini):
            print(f"  {vershina}: {sorted(self.spisok_smeznosti[vershina])}")

a = Graph()
a.add_vershina('b')
print(a.display())
```
Вторая часть реализует обход графа в глубину
``` Python
#2
def obhod_v_glubinu(graph, start):
    visited = set()
    result = []
    stack = [start]

    while stack:
        vershina = stack.pop()
        if vershina not in visited:
            visited.add(vershina)
            result.append(vershina)
            for sosed in reversed(graph.spisok_smeznosti[vershina]):
                if sosed not in visited:
                    stack.append(sosed)
    return result
```
Третья часть реализует обход графа в ширину
``` Python
#3
from collections import deque

def obhod_v_shirinu(graph, start):
    visited = set()
    result = []
    queue = deque([start])
    visited.add(start)

    while queue:
        vershina = queue.popleft()
        result.append(vershina)

        for sosed in graph.spisok_smeznosti[vershina]:
            if sosed not in visited:
                visited.add(sosed)
                queue.append(sosed)
    return result
```
Четвертая часть реализует приложение для работы с графом
``` Python
#4
def main():
    graph = None

    print("Программа для работы с графами")

    while True:
        print("Меню:")
        print("1. Инициализировать граф")
        print("2. Добавить вершину")
        print("3. Добавить ребро")
        print("4. Удалить вершину")
        print("5. Удалить ребро")
        print("7. Обход в глубину")
        print("6. Показать граф")     
        print("8. Обход в ширину")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            vershini_input = input("Введите вершины через пробел: ").strip()
            vershini = vershini_input.split() if vershini_input else []
            graph = Graph(vershini)
            print("Граф успешно инициализирован!")
            
        elif choice == "2":
            vershina = input("Введите вершину для добавления: ").strip()
            graph.add_vershina(vershina)
            print(f"Вершина '{vershina}' добавлена.")
            
        elif choice == "3":
            u = input("Введите первую вершину: ").strip()
            v = input("Введите вторую вершину: ").strip()
            graph.add_rebro(u, v)
            print(f"Ребро между '{u}' и '{v}' добавлено.")
            
        elif choice == "4":
            vershina = input("Введите вершину для удаления: ").strip()
            graph.remove_vershina(vershina)
            print(f"Вершина '{vershina}' и все связанные ребра удалены.")
            
        elif choice == "5":
            u = input("Введите первую вершину: ").strip()
            v = input("Введите вторую вершину: ").strip()
            graph.remove_rebro(u, v)
            print(f"Ребро между '{u}' и '{v}' удалено.")

        elif choice == "6":
            print("\nТЕКУЩИЙ ГРАФ:")
            graph.display()
            
        elif choice == "7":
            start = input("Введите начальную вершину: ").strip()
            result = obhod_v_glubinu(graph, start)
            print(f"Результат: {result}")
            
        elif choice == "8":
            start = input("Введите начальную вершину: ").strip()
            result = obhod_v_shirinu(graph, start)
            print(f"Результат: {result}")
```
Пятая часть реализует алгоритм Дейкстры
``` Python
#5
import heapq
from collections import deque

def dijkstra(graph, start, end):
    distances = {vershina: float('inf') for vershina in graph.vershini}
    predecessors = {vershina: None for vershina in graph.vershini}
    distances[start] = 0
    
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vershina = heapq.heappop(priority_queue)
        if current_vershina == end:
            break
        if current_distance > distances[current_vershina]:
            continue
        for sosed in graph.spisok_smeznosti[current_vershina]:
            ves = 1
            if hasattr(graph, 'vesa_reber') and (current_vershina, sosed) in graph.vesa_reber:
                ves = graph.vesa_reber[(current_vershina, sosed)]
            
            distance = current_distance + ves
            
            if distance < distances[sosed]:
                distances[sosed] = distance
                predecessors[sosed] = current_vershina
                heapq.heappush(priority_queue, (distance, sosed))
    
    if distances[end] == float('inf'):
        return None, float('inf')
    
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    
    return path, distances[end]
```
Шестая часть позволяет выполнить индивидуальное задание и получить ответ - ('5', '1', '6', '7', 11)
``` Python
#6
graf = Graph()
graf.add_rebro('1', '5', 3)
graf.add_rebro('1', '6', 1)
graf.add_rebro('2', '5', 4)
graf.add_rebro('6', '5', 9)
graf.add_rebro('2', '3', 3)
graf.add_rebro('2', '7', 15)
graf.add_rebro('3', '6', 10)
graf.add_rebro('6', '7', 7)
graf.add_rebro('3', '7', 6)
graf.add_rebro('3', '8', 1)
graf.add_rebro('7', '4', 1)
graf.add_rebro('4', '8', 2)
print(dijkstra(graf, '5', '7'))
```
