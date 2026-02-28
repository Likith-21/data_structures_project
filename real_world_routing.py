from __future__ import annotations

import math
from typing import Dict, List, Tuple

import folium
import requests


def get_lat_lon(place: str) -> Tuple[float, float] | None:
    """Geocode a place name to lat/lon using Nominatim (OpenStreetMap)."""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": f"{place}, India", "format": "json", "limit": 1}
        headers = {"User-Agent": "SmartRoutePlanner/1.0"}
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        results = response.json()
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"])
    except Exception:
        pass
    return None


def get_route(start: str, end: str) -> Tuple[List[Tuple[float, float]] | None, float]:
    """Fetch a route polyline from start to end using OSRM. Returns (route_coords, distance_km)."""
    try:
        start_coord = get_lat_lon(start)
        end_coord = get_lat_lon(end)
        if not start_coord or not end_coord:
            print(f"DEBUG: Could not geocode {start} or {end}")
            return None, 0.0

        print(f"DEBUG: Start coords: {start_coord}, End coords: {end_coord}")
        url = f"http://router.project-osrm.org/route/v1/driving/{start_coord[1]},{start_coord[0]};{end_coord[1]},{end_coord[0]}"
        params = {"overview": "full", "geometries": "geojson"}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"DEBUG: OSRM Response code: {data.get('code')}")
        
        if data.get("code") == "Ok" and data.get("routes"):
            route_data = data["routes"][0]
            coords = route_data.get("geometry", {}).get("coordinates", [])
            distance_meters = route_data.get("distance", 0)
            distance_km = distance_meters / 1000.0
            print(f"DEBUG: Distance from OSRM: {distance_meters} meters = {distance_km} km")
            return [(lon, lat) for lon, lat in coords], distance_km
        else:
            print(f"DEBUG: OSRM returned no routes or error: {data}")
    except Exception as e:
        print(f"DEBUG: Exception in get_route: {e}")
    
    return None, 0.0


def create_india_route_map(
    start: str,
    end: str,
    route: List[Tuple[float, float]] | None,
    output_file: str,
) -> bool:
    """Create an interactive map showing the India-wide route."""
    try:
        start_coord = get_lat_lon(start)
        end_coord = get_lat_lon(end)
        if not start_coord or not end_coord:
            return False

        center_lat = (start_coord[0] + end_coord[0]) / 2
        center_lon = (start_coord[1] + end_coord[1]) / 2

        map_obj = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles="OpenStreetMap",
        )

        folium.Marker(
            location=start_coord,
            popup=f"Start: {start}",
            icon=folium.Icon(color="green", icon="play"),
        ).add_to(map_obj)

        folium.Marker(
            location=end_coord,
            popup=f"End: {end}",
            icon=folium.Icon(color="red", icon="stop"),
        ).add_to(map_obj)

        if route:
            folium.PolyLine(
                locations=[(lat, lon) for lon, lat in route],
                color="blue",
                weight=4,
                opacity=0.8,
                tooltip="Route from OSRM",
            ).add_to(map_obj)

        map_obj.save(output_file)
        return True
    except Exception:
        return False


def calculate_route_distance(route: List[Tuple[float, float]]) -> float:
    """Calculate total distance of a route in kilometers."""
    if not route or len(route) < 2:
        return 0.0

    total_distance = 0.0
    for i in range(len(route) - 1):
        lon1, lat1 = route[i]
        lon2, lat2 = route[i + 1]
        total_distance += haversine(lat1, lon1, lat2, lon2)
    return total_distance


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points in km."""
    R = 6371.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def calculate_travel_time(distance_km: float, speed_kmh: float) -> Dict[str, float | int]:
    """Calculate travel time in hours, minutes, and seconds."""
    if speed_kmh <= 0:
        return {"hours": 0, "minutes": 0, "seconds": 0, "total_hours": 0}
    
    total_hours = distance_km / speed_kmh
    hours = int(total_hours)
    minutes = int((total_hours - hours) * 60)
    seconds = int(((total_hours - hours) * 60 - minutes) * 60)
    
    return {
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "total_hours": round(total_hours, 2),
    }
