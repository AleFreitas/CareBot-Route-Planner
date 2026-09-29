from models.graph import Graph


def find_best_route(graph: Graph, start: str, goal: str) -> list[str]:
    """Return the best route from start to goal using A*, weighted only by distance.

    The route is the list of node labels from start to goal, both included.
    An empty list means there is no route between the two nodes.
    """
from heapq import heappush, heappop
from math import sqrt

def heuristic(node_a, node_b):
    return sqrt(
        (node_a.latitude - node_b.latitude) ** 2 +
        (node_a.longitude - node_b.longitude) ** 2
    )


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)
    return path


def find_best_route(graph, start: str, goal: str) -> list[str]:
    if start not in graph.nodes or goal not in graph.nodes:
        return []

    open_set = []
    heappush(open_set, (0, start))

    came_from = {}

    g_score = {node: float("inf") for node in graph.nodes}
    g_score[start] = 0

    f_score = {node: float("inf") for node in graph.nodes}
    f_score[start] = heuristic(graph.nodes[start], graph.nodes[goal])

    while open_set:
        _, current = heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for connection in graph.connections[current]:
            # ignora caminhos que o robô não pode andar
            if not connection.robot_walkable:
                continue

            neighbor = connection.destination
            tentative_g = g_score[current] + connection.distance

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(
                    graph.nodes[neighbor],
                    graph.nodes[goal]
                )

                heappush(open_set, (f_score[neighbor], neighbor))

    return []
