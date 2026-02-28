from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from typing import Dict, List, Tuple

import folium

from algorithms import astar, dijkstra


BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "graph_data.json"
OUTPUT_MAP = BASE_DIR / "route_map.html"


def load_graph_data(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_city_lookup(cities: List[dict]) -> Dict[str, Tuple[float, float]]:
    return {city["id"]: (city["lat"], city["lon"]) for city in cities}


def update_traffic_delays(roads: List[dict], variation: float = 0.30) -> None:
    for road in roads:
        base_delay = road.get("base_traffic_delay", road["traffic_delay"])
        road["base_traffic_delay"] = base_delay
        factor = random.uniform(1 - variation, 1 + variation)
        road["traffic_delay"] = max(1, round(base_delay * factor, 2))


def build_adjacency(roads: List[dict]) -> Dict[str, Dict[str, float]]:
    graph: Dict[str, Dict[str, float]] = {}
    for road in roads:
        source = road["from"]
        target = road["to"]
        weight = road["distance"] + road["traffic_delay"]

        graph.setdefault(source, {})[target] = weight
        graph.setdefault(target, {})[source] = weight
    return graph


def haversine_km(city_a: Tuple[float, float], city_b: Tuple[float, float]) -> float:
    lat1, lon1 = city_a
    lat2, lon2 = city_b

    radius = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    sin_dlat = math.sin(dlat / 2)
    sin_dlon = math.sin(dlon / 2)

    a = sin_dlat**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * sin_dlon**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


def make_heuristic(city_lookup: Dict[str, Tuple[float, float]]):
    def heuristic(node: str, goal: str) -> float:
        return haversine_km(city_lookup[node], city_lookup[goal])

    return heuristic


def create_map(
    city_lookup: Dict[str, Tuple[float, float]],
    dijkstra_path: List[str],
    astar_path: List[str],
    output_file: Path,
) -> None:
    center_lat = sum(lat for lat, _ in city_lookup.values()) / len(city_lookup)
    center_lon = sum(lon for _, lon in city_lookup.values()) / len(city_lookup)
    route_map = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    for city, (lat, lon) in city_lookup.items():
        folium.Marker([lat, lon], popup=city).add_to(route_map)

    if dijkstra_path:
        dijkstra_coords = [city_lookup[city] for city in dijkstra_path]
        folium.PolyLine(
            dijkstra_coords,
            color="blue",
            weight=5,
            opacity=0.8,
            tooltip="Dijkstra Path",
        ).add_to(route_map)

    if astar_path:
        astar_coords = [city_lookup[city] for city in astar_path]
        folium.PolyLine(
            astar_coords,
            color="red",
            weight=4,
            opacity=0.8,
            tooltip="A* Path",
        ).add_to(route_map)

    route_map.save(str(output_file))


def run_route_planner(
    start: str,
    goal: str,
    simulate_traffic: bool = False,
    map_output_file: Path = OUTPUT_MAP,
) -> dict:
    data = load_graph_data(DATA_FILE)
    cities = data["cities"]
    roads = data["roads"]

    city_lookup = build_city_lookup(cities)

    if simulate_traffic:
        update_traffic_delays(roads)

    if start not in city_lookup or goal not in city_lookup:
        valid = ", ".join(sorted(city_lookup.keys()))
        raise ValueError(f"Invalid city. Choose from: {valid}")

    graph = build_adjacency(roads)
    heuristic = make_heuristic(city_lookup)

    d_path, d_cost, d_visited = dijkstra(graph, start, goal)
    a_path, a_cost, a_visited = astar(graph, start, goal, heuristic)

    create_map(city_lookup, d_path, a_path, map_output_file)

    return {
        "start": start,
        "goal": goal,
        "dijkstra": {"path": d_path, "cost": d_cost, "visited": d_visited},
        "astar": {"path": a_path, "cost": a_cost, "visited": a_visited},
        "map_file": str(map_output_file),
        "cities": sorted(city_lookup.keys()),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smart Route Planner: Dijkstra vs A*")
    parser.add_argument("--start", default="Delhi", help="Start city")
    parser.add_argument("--goal", default="Varanasi", help="Destination city")
    parser.add_argument(
        "--simulate-traffic",
        action="store_true",
        help="Randomly update traffic delays before route calculation",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_route_planner(
        start=args.start,
        goal=args.goal,
        simulate_traffic=args.simulate_traffic,
        map_output_file=OUTPUT_MAP,
    )

    d_path = result["dijkstra"]["path"]
    d_cost = result["dijkstra"]["cost"]
    d_visited = result["dijkstra"]["visited"]
    a_path = result["astar"]["path"]
    a_cost = result["astar"]["cost"]
    a_visited = result["astar"]["visited"]

    print("\n=== Smart Route Planner ===")
    print(f"From: {args.start} -> To: {args.goal}")

    print("\n[Dijkstra]")
    print(f"Path: {' -> '.join(d_path) if d_path else 'No route found'}")
    print(f"Total Cost (Distance + Traffic): {d_cost:.2f}")
    print(f"Visited Nodes: {d_visited}")

    print("\n[A*]")
    print(f"Path: {' -> '.join(a_path) if a_path else 'No route found'}")
    print(f"Total Cost (Distance + Traffic): {a_cost:.2f}")
    print(f"Visited Nodes: {a_visited}")

    print("\n[Comparison]")
    print(f"Dijkstra visited {d_visited} nodes, A* visited {a_visited} nodes.")

    print(f"\nMap generated: {result['map_file']}")


if __name__ == "__main__":
    main()
