from models.graph import Graph


def find_best_route(graph: Graph, start: str, goal: str) -> list[str]:
    """Return the best route from start to goal using A*, weighted only by distance.

    The route is the list of node labels from start to goal, both included.
    An empty list means there is no route between the two nodes.
    """
    # TODO: implement A* over graph.connections using Connection.distance
    return []
