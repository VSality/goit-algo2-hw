from bfs import bfs
from collections import deque
 
#Основна функція для обчислення максимального потоку
def edmonds_karp(capacity, source, sink):
    vertices = len(capacity)
    flow = [[0] * vertices for _ in range(vertices)]  # Потоки
    max_flow = 0

    while True:
        # Поиск пути в остаточной сети (BFS)
        parent = [-1] * vertices  # Массив предков для восстановления пути
        parent[source] = source
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for v in range(vertices):
                # Проверяем остаточную пропускную способность
                if parent[v] == -1 and capacity[u][v] - flow[u][v] > 0:
                    parent[v] = u
                    if v == sink:  # Если достигли стока
                        break
                    queue.append(v)
            else:
                continue
            break

        # Если не нашли путь до стока
        if parent[sink] == -1:
            break

        # Найти минимальную остаточную пропускную способность вдоль пути
        increment = float('Inf')
        v = sink
        while v != source:
            u = parent[v]
            increment = min(increment, capacity[u][v] - flow[u][v])
            v = u

        # Обновить потоки вдоль пути
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += increment
            flow[v][u] -= increment
            v = u

        max_flow += increment

    return max_flow, flow