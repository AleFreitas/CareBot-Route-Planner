"""Build the graph hash tables from every city's CSV files and save them to graph.json.

Run this script whenever any file under csv/ changes, and commit graph.json.
Other modules read the graph with load_graph().
"""

import csv
import json
from dataclasses import asdict
from pathlib import Path

from models.graph import Connection, Element, Graph

CSV_DIR = Path(__file__).parent / "csv"
GRAPH_PATH = Path(__file__).parent / "graph.json"

# Files that every city folder inside csv/ must contain
ELEMENTS_FILE = "elements.csv"
CONNECTIONS_FILE = "connections.csv"
INTERCITY_CONNECTIONS_FILE = "intercity_connections.csv"
CONNECTION_FILES = (CONNECTIONS_FILE, INTERCITY_CONNECTIONS_FILE)


def read_rows(path: Path, columns: tuple[str, ...]) -> list[dict[str, str]]:
    """Read a CSV file's rows, failing if its header is not exactly `columns`."""
    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if tuple(reader.fieldnames or ()) != columns:
            raise ValueError(f"{path}: cabeçalho {reader.fieldnames} diferente do esperado {list(columns)}")
        return list(reader)


def load_nodes(city_dirs: list[Path]) -> dict[str, Element]:
    """Build the node label -> Element table. Labels must be unique across all cities."""
    nodes = {}
    for city_dir in city_dirs:
        for row in read_rows(city_dir / ELEMENTS_FILE, Element.CSV_COLUMNS):
            node = Element.from_csv_row(row, city_dir.name)
            if node.label in nodes:
                raise ValueError(f"Label {node.label} repetido em {city_dir.name} e {nodes[node.label].city}")
            nodes[node.label] = node
    return nodes


def parse_connection(row: dict[str, str], source: str, nodes: dict[str, Element]) -> Connection:
    """Convert a CSV row into a Connection, checking that both of its nodes exist.

    `source` is the "<city>/<file>" the row came from, shown in error messages.
    """
    try:
        connection = Connection.from_csv_row(row)
    except ValueError as error:
        raise ValueError(f"{source}: {error}") from error

    for label in (connection.origin, connection.destination):
        if label not in nodes:
            raise ValueError(f"{source}: nó {label} não existe em nenhum {ELEMENTS_FILE}")
    return connection


def load_connections(city_dirs: list[Path], nodes: dict[str, Element]) -> dict[str, list[Connection]]:
    """Build the node label -> outgoing Connections table. Every node is a key, even with no connections."""
    connections = {label: [] for label in nodes}
    for city_dir in city_dirs:
        for file_name in CONNECTION_FILES:
            source = f"{city_dir.name}/{file_name}"
            for row in read_rows(city_dir / file_name, Connection.CSV_COLUMNS):
                connection = parse_connection(row, source, nodes)
                connections[connection.origin].append(connection)
    return connections


def load_graph() -> Graph:
    """Load the graph saved in graph.json (not the CSVs, so regenerate it after changing them)."""
    data = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    return Graph(
        nodes={label: Element(**node) for label, node in data["nodes"].items()},
        connections={
            label: [Connection(**connection) for connection in node_connections]
            for label, node_connections in data["connections"].items()
        },
    )


def main() -> None:
    city_dirs = sorted(path for path in CSV_DIR.iterdir() if path.is_dir())

    # Load every node first, since intercity connections point to nodes of other cities
    nodes = load_nodes(city_dirs)
    connections = load_connections(city_dirs, nodes)

    graph = Graph(nodes=nodes, connections=connections)
    GRAPH_PATH.write_text(json.dumps(asdict(graph), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    connection_count = sum(len(node_connections) for node_connections in connections.values())
    print(f"{len(nodes)} nós e {connection_count} conexões de {len(city_dirs)} cidade(s) salvos em {GRAPH_PATH.name}")


if __name__ == "__main__":
    main()
