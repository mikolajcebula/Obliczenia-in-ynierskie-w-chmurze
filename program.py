import heapq
import random
from multiprocessing import Pool
import matplotlib.pyplot as plt
import time

def generate_obstacle_grid(n, obstacle_probability):
    # Tworzenie pustej planszy z samymi zerami (wolne miejsca)
    grid = [[0] * n for _ in range(n)]
    
    # Ustawienie 0 na pozycji (0, 0) i (n-1, n-1)
    grid[0][0] = 0
    grid[n-1][n-1] = 0
    
    # Dodawanie przeszkód na planszę z zadanym prawdopodobieństwem
    for i in range(n):
        for j in range(n):
            # Pominięcie ustawionych wartości 0
            if (i, j) == (0, 0) or (i, j) == (n-1, n-1):
                continue
            
            if random.uniform(0, 1) < obstacle_probability:
                grid[i][j] = 1  # 1 oznacza przeszkodę
    
    return grid

def generate_graph_partial(args):
    i, j, n, grid = args
    graph = {}
    
    # Funkcja pomocnicza do sprawdzania, czy punkt znajduje się w granicach planszy
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n
    
    if grid[i][j] != 1:
        graph[(i, j)] = {}
        
        # Sprawdzanie sąsiadów w pionie i poziomie (bez skosów)
        for x, y in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
            if is_valid(x, y) and grid[x][y] != 1:
                graph[(i, j)][(x, y)] = 1  # Waga 1 dla ruchu w pionie i poziomie

    return graph

def generate_graph(grid):
    n = len(grid)
    graph = {}
    
    with Pool() as pool:
        args_list = [(i, j, n, grid) for i in range(n) for j in range(n)]
        results = pool.map(generate_graph_partial, args_list)
        
        for g in results:
            graph.update(g)
            
    return graph

def dijkstra(graph, start, end):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    previous_vertices = {}
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_vertex]:
            continue
        
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
    
    path = []
    current = end
    while current in previous_vertices:
        path.insert(0, current)
        current = previous_vertices[current]
    path.insert(0, start)
    
    return distances[end], path

def visualize_grid(grid, path=None):
    plt.imshow(grid, cmap='binary', interpolation='none')
    
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, color='red', marker='o')

    plt.show()

# Pomiar czasu wykonania programu
start_time = time.time()

# Przykładowa plansza z przeszkodami (1) i wolnymi miejscami (0)
grid = generate_obstacle_grid(10000, 0.1)

# Generowanie grafu
graph = generate_graph(grid)

# Określenie punktu startowego i końcowego
start_point = (0, 0)
end_point = (9999, 9999)

# Obliczenie najkrótszej ścieżki
shortest_distance, path = dijkstra(graph, start_point, end_point)

# Wyświetlanie wyników
print(f"Najkrótsza odległość od {start_point} do {end_point}: {shortest_distance}")
# Pomiar czasu wykonania programu
end_time = time.time()
execution_time = end_time - start_time
print(f"Czas wykonania programu: {execution_time} sekundy")
visualize_grid(grid, path)


