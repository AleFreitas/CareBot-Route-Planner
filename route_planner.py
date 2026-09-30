from heapq import heappop, heappush
from math import asin, cos, radians, sin, sqrt

from models.graph import Element, Graph

EARTH_RADIUS_METERS = 6_371_000


def heuristic(node_a: Element, node_b: Element) -> float:
    """Straight-line distance in meters between two nodes (haversine formula)."""
    lat_a, lon_a = radians(node_a.latitude), radians(node_a.longitude)
    lat_b, lon_b = radians(node_b.latitude), radians(node_b.longitude)

    h = sin((lat_b - lat_a) / 2) ** 2 + cos(lat_a) * cos(lat_b) * sin((lon_b - lon_a) / 2) ** 2
    return 2 * EARTH_RADIUS_METERS * asin(sqrt(h))


def reconstruct_path(came_from: dict[str, str], current: str) -> list[str]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def find_best_route(graph: Graph, start: str, goal: str) -> list[str]:
    """Return the best route from start to goal using A* on a naive map, where each connection costs only its distance.

    The route is the list of node labels from start to goal, both included.
    An empty list means there is no route between the two nodes.
    """
    if start not in graph.nodes or goal not in graph.nodes:
        return []

    g_score = {node: float("inf") for node in graph.nodes}
    g_score[start] = 0

    f_score = {node: float("inf") for node in graph.nodes}
    f_score[start] = heuristic(graph.nodes[start], graph.nodes[goal])

    open_set = [(f_score[start], start)]
    came_from = {}

    while open_set:
        f, current = heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        # Outdated entry: a shorter path to this node was found after it was pushed
        if f > f_score[current]:
            continue

        for connection in graph.connections[current]:
            neighbor = connection.destination
            tentative_g = g_score[current] + connection.distance

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(graph.nodes[neighbor], graph.nodes[goal])
                heappush(open_set, (f_score[neighbor], neighbor))

    return []
