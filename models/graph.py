"""Models of the graph: its nodes (elements.csv) and connections (connections.csv, intercity_connections.csv)."""

from dataclasses import dataclass
from typing import ClassVar


def parse_bool(value: str) -> bool:
    if value not in ("true", "false"):
        raise ValueError(f"Valor booleano inválido: {value!r} (use true ou false)")
    return value == "true"


@dataclass
class Element:
    """A node of the graph, from one row of elements.csv."""

    CSV_COLUMNS: ClassVar[tuple[str, ...]] = ("Label", "Address", "Type", "Resident", "Latitude", "Longitude")

    label: str
    city: str
    address: str
    type: str
    resident: str | None
    latitude: float
    longitude: float

    @classmethod
    def from_csv_row(cls, row: dict[str, str], city: str) -> "Element":
        return cls(
            label=row["Label"],
            city=city,
            address=row["Address"],
            type=row["Type"],
            resident=row["Resident"] or None,
            latitude=float(row["Latitude"]),
            longitude=float(row["Longitude"]),
        )


@dataclass
class Connection:
    """An edge of the graph, from one row of connections.csv or intercity_connections.csv."""

    CSV_COLUMNS: ClassVar[tuple[str, ...]] = (
        "From",
        "To",
        "Type",
        "robot_walkable",
        "distance",
        "time",
        "battery_consumption",
        "security",
        "financial_cost",
        "traffic_light",
        "road_holes",
        "traffic_jam",
        "speed_bumps",
    )

    origin: str
    destination: str
    type: str
    robot_walkable: bool
    distance: int
    time: float
    battery_consumption: float
    security: int
    financial_cost: float
    traffic_light: int
    road_holes: int
    traffic_jam: int
    speed_bumps: int

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> "Connection":
        empty = [column for column, value in row.items() if value == ""]
        if empty:
            raise ValueError(f"Conexão {row['From']} -> {row['To']} com colunas vazias: {empty}")

        return cls(
            origin=row["From"],
            destination=row["To"],
            type=row["Type"],
            robot_walkable=parse_bool(row["robot_walkable"]),
            distance=int(row["distance"]),
            time=float(row["time"]),
            battery_consumption=float(row["battery_consumption"]),
            security=int(row["security"]),
            financial_cost=float(row["financial_cost"]),
            traffic_light=int(row["traffic_light"]),
            road_holes=int(row["road_holes"]),
            traffic_jam=int(row["traffic_jam"]),
            speed_bumps=int(row["speed_bumps"]),
        )


@dataclass
class Graph:
    """The graph hash tables: node label -> Element, and node label -> connections leaving that node."""

    nodes: dict[str, Element]
    connections: dict[str, list[Connection]]
