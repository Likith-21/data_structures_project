# Smart Route Planner

A B.Tech project demonstrating advanced pathfinding algorithms (Dijkstra & A*) with real-world India-wide routing capabilities and an interactive web dashboard.

## Features

### 🎯 Core Algorithms
- **Dijkstra's Algorithm**: Finds shortest path based on distance + traffic weights
- **A* Search**: Optimized pathfinding using haversine heuristic
- **Algorithm Comparison**: See node exploration counts and performance metrics
- **Real-time Traffic Simulation**: Dynamic weight updates for realistic routing

### 🗺️ India-Wide Routing
- Route planning between any Indian cities
- Real driving distances from OSRM (Open Source Routing Machine)
- Interactive maps with Folium/Leaflet
- 200+ major Indian cities supported
- Geocoding via OpenStreetMap Nominatim

### ⏱️ Travel Time Calculator
- User-configurable cruising speed (20-150 km/h)
- Accurate time estimation: hours, minutes, seconds
- Distance vs. time analysis

### 🖥️ Interactive Dashboard
- Built with Streamlit for easy deployment
- Two modes:
  - **Algorithm Demo**: Compare Dijkstra vs A* on preset cities
  - **India-Wide Routing**: Route between any locations
- Visual route comparison on interactive maps
- Real-time calculation and rendering

## Project Structure

```
SmartRoutePlanner/
├── algorithms.py          # Dijkstra & A* implementations
├── main.py               # CLI interface and core planner logic
├── dashboard.py          # Streamlit web interface
├── real_world_routing.py # OSRM integration & geocoding
├── cities_db.py          # Indian cities database
├── graph_data.json       # Sample city network data
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Installation

### Prerequisites
- Python 3.11+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Likith-21/data_structures_project.git
cd data_structures_project/SmartRoutePlanner
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Dashboard (Recommended)

Launch the interactive dashboard:
```bash
streamlit run dashboard.py
```

Then open your browser to `http://localhost:8501`

**Algorithm Demo Tab:**
- Select start and destination cities
- Enable traffic simulation
- Compare Dijkstra vs A* performance

**India-Wide Routing Tab:**
- Enter any Indian city names
- Set your cruising speed
- Get exact distance and travel time

### Command Line Interface

Run algorithm comparison from terminal:
```bash
python main.py --start Delhi --goal Varanasi --simulate-traffic
```

**Options:**
- `--start`: Starting city
- `--goal`: Destination city
- `--simulate-traffic`: Enable random traffic delays

**Example output:**
```
=== Smart Route Planner ===
From: Delhi -> To: Varanasi

[Dijkstra]
Path: Delhi -> Agra -> Lucknow -> Varanasi
Total Cost: 965.10
Visited Nodes: 6

[A*]
Path: Delhi -> Agra -> Lucknow -> Varanasi
Total Cost: 965.10
Visited Nodes: 4

[Comparison]
Dijkstra visited 6 nodes, A* visited 4 nodes.

Map generated: route_map.html
```

## How It Works

### Algorithm Implementations

**Dijkstra's Algorithm:**
- Priority queue-based implementation
- Explores nodes in order of total distance from start
- Guaranteed optimal path

**A* Search:**
- Uses haversine distance as admissible heuristic
- Explores fewer nodes than Dijkstra
- f(n) = g(n) + h(n) where:
  - g(n) = actual cost from start
  - h(n) = straight-line distance to goal

### Data Flow

1. **Graph Loading**: Cities and roads loaded from JSON
2. **Weight Calculation**: `weight = distance + traffic_delay`
3. **Pathfinding**: Both algorithms run simultaneously
4. **Visualization**: Routes rendered on Folium map
5. **Comparison**: Node visit counts and costs displayed

### Real-World Routing

1. **Geocoding**: City names → coordinates (Nominatim API)
2. **Route Calculation**: Coordinates → driving route (OSRM API)
3. **Distance Extraction**: Actual road distance in kilometers
4. **Time Calculation**: `time = distance / speed`

## Technologies Used

- **Python 3.11**: Core language
- **NetworkX**: Graph data structures (Algorithm Demo)
- **Streamlit**: Web dashboard framework
- **Folium**: Interactive map visualization
- **OSRM**: Real-world routing engine
- **OpenStreetMap Nominatim**: Geocoding service
- **Matplotlib**: Plotting support

## Example Routes

### Algorithm Demo (Preset Cities)
- Delhi → Varanasi: ~965 km
- Jaipur → Lucknow: ~570 km
- Mumbai → Delhi: ~1,379 km (via India-Wide mode)

### India-Wide Routing (Any Cities)
- Chittoor City → Chennai: 156 km
- Bangalore → Hyderabad: 561 km
- Mumbai → Bangalore: ~980 km

**Tip**: For accurate geocoding, use full city names like "Chittoor City" or "Bangalore City"

## Performance

- **A* Efficiency**: Typically explores 30-50% fewer nodes than Dijkstra
- **Real-time Routing**: Sub-second response for most queries
- **Map Rendering**: Instant visualization with Folium

## Future Enhancements

- [ ] Multi-stop route optimization
- [ ] Historical traffic pattern analysis
- [ ] Alternative route suggestions
- [ ] Fuel cost estimation
- [ ] REST API for route queries
- [ ] Mobile-responsive UI

## Author

**Likith**  
B.Tech Data Structures Project  
[GitHub Profile](https://github.com/Likith-21)

## License

This project is open source and available for educational purposes.

## Acknowledgments

- OpenStreetMap for geocoding services
- OSRM for routing engine
- Streamlit for the dashboard framework
- NetworkX for graph algorithms

---

**Star ⭐ this repository if you found it helpful!**