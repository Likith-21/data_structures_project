from __future__ import annotations

import heapq
from typing import Callable, Dict, List, Tuple

Graph = Dict[str, Dict[str, float]]


def reconstruct_path(came_from: Dict[str, str], start: str, goal: str) -> List[str]:
    if goal not in came_from and goal != start:
        return []

    path = [goal]
    current = goal
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def dijkstra(graph: Graph, start: str, goal: str) -> Tuple[List[str], float, int]:
    distances = {node: float("inf") for node in graph}
    distances[start] = 0.0
    came_from: Dict[str, str] = {}

    queue: List[Tuple[float, str]] = [(0.0, start)]
    explored_count = 0

    while queue:
        current_distance, current = heapq.heappop(queue)
        if current_distance > distances[current]:
            continue

        explored_count += 1

        if current == goal:
            break

        for neighbor, weight in graph[current].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                came_from[neighbor] = current
                heapq.heappush(queue, (new_distance, neighbor))

    path = reconstruct_path(came_from, start, goal)
    return path, distances[goal], explored_count


def astar(
    graph: Graph,
    start: str,
    goal: str,
    heuristic: Callable[[str, str], float],
) -> Tuple[List[str], float, int]:
    g_score = {node: float("inf") for node in graph}
    g_score[start] = 0.0

    came_from: Dict[str, str] = {}
    open_queue: List[Tuple[float, float, str]] = [(heuristic(start, goal), 0.0, start)]
    explored_count = 0

    while open_queue:
        _, current_g, current = heapq.heappop(open_queue)
        if current_g > g_score[current]:
            continue

        explored_count += 1

        if current == goal:
            break

        for neighbor, weight in graph[current].items():
            tentative_g = current_g + weight
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                heapq.heappush(open_queue, (tentative_g + heuristic(neighbor, goal), tentative_g, neighbor))

    path = reconstruct_path(came_from, start, goal)
    return path, g_score[goal], explored_count
