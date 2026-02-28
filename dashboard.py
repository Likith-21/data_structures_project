from __future__ import annotations

from pathlib import Path

import streamlit as st

from cities_db import get_city_suggestions
from main import DATA_FILE, load_graph_data, run_route_planner
from real_world_routing import calculate_travel_time, create_india_route_map, get_route


st.set_page_config(page_title="Smart Route Planner", layout="wide")
st.title("Smart Route Planner Dashboard")
st.caption("Compare Dijkstra vs A* or route anywhere in India")

tab1, tab2 = st.tabs(["Algorithm Demo (Cities)", "India-Wide Routing"])

with tab1:
    st.subheader("Algorithm Comparison: Dijkstra vs A*")
    
    data = load_graph_data(DATA_FILE)
    cities = sorted(city["id"] for city in data["cities"])

    with st.form("route_form"):
        start_city = st.selectbox("Start City", options=cities, index=0, key="demo_start")
        default_goal_index = len(cities) - 1 if len(cities) > 1 else 0
        goal_city = st.selectbox("Destination City", options=cities, index=default_goal_index, key="demo_goal")
        simulate_traffic = st.checkbox("Simulate Real-Time Traffic", value=True)
        submitted = st.form_submit_button("Find Route")

    if submitted:
        if start_city == goal_city:
            st.warning("Start and destination should be different.")
        else:
            map_file = Path(__file__).parent / "route_map.html"
            result = run_route_planner(
                start=start_city,
                goal=goal_city,
                simulate_traffic=simulate_traffic,
                map_output_file=map_file,
            )

            dijkstra_data = result["dijkstra"]
            astar_data = result["astar"]

            st.subheader("Results")
            col1, col2, col3 = st.columns(3)
            col1.metric("Dijkstra Cost", f"{dijkstra_data['cost']:.2f}")
            col2.metric("A* Cost", f"{astar_data['cost']:.2f}")
            col3.metric("A* Node Savings", dijkstra_data["visited"] - astar_data["visited"])

            st.write("**Dijkstra Path**", " -> ".join(dijkstra_data["path"]) if dijkstra_data["path"] else "No route found")
            st.write("**A* Path**", " -> ".join(astar_data["path"]) if astar_data["path"] else "No route found")
            st.write(
                f"Comparison: Dijkstra visited {dijkstra_data['visited']} nodes, A* visited {astar_data['visited']} nodes."
            )

            if map_file.exists():
                st.subheader("Route Map")
                map_html = map_file.read_text(encoding="utf-8")
                st.components.v1.html(map_html, height=520, scrolling=False)

with tab2:
    st.subheader("Find Routes Anywhere in India")
    st.info("Enter city names to find routes and calculate travel time")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Start Location**")
        start_place = st.text_input(
            "Type city name",
            placeholder="e.g., Mumbai, Delhi, Bangalore...",
            key="start_input",
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("**End Location**")
        end_place = st.text_input(
            "Type city name",
            placeholder="e.g., Chennai, Hyderabad, Pune...",
            key="end_input",
            label_visibility="collapsed"
        )
    
    col_speed, col_verify = st.columns(2)
    with col_speed:
        st.write("**Travel Speed**")
        speed_kmh = st.slider("Speed (km/h)", min_value=20, max_value=150, value=60, step=5, label_visibility="collapsed")
    with col_verify:
        st.write("**Options**")
        verify_coords = st.checkbox("Show geocoded coordinates")
    
    india_submitted = st.button("Get Route & Calculate Time", type="primary")
    
    if india_submitted:
        if not start_place or not end_place:
            st.warning("Please enter both start and end locations.")
        elif start_place.lower() == end_place.lower():
            st.warning("Start and end locations should be different.")
        else:
            with st.spinner("Finding route and calculating distance..."):
                from real_world_routing import get_lat_lon
                
                # Show coordinates if requested
                if verify_coords:
                    start_coords = get_lat_lon(start_place)
                    end_coords = get_lat_lon(end_place)
                    if start_coords and end_coords:
                        st.info(f"**Geocoded Coordinates:**\n- {start_place}: Latitude {start_coords[0]:.4f}, Longitude {start_coords[1]:.4f}\n- {end_place}: Latitude {end_coords[0]:.4f}, Longitude {end_coords[1]:.4f}")
                        # Calculate straight-line distance
                        from real_world_routing import haversine
                        straight_dist = haversine(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
                        st.write(f"**Straight-line distance: {straight_dist:.2f} km** (driving distance will be longer)")
                    else:
                        st.warning("Could not geocode one or both locations. Check spelling and try again.")
                
                route, distance_km = get_route(start_place, end_place)
                if distance_km > 0:
                    travel_time = calculate_travel_time(distance_km, speed_kmh)
                    
                    st.success(f"✓ Route found! Distance: {distance_km:.2f} km at {speed_kmh} km/h")
                    
                    st.subheader("📍 Travel Information")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Distance", f"{distance_km:.2f} km")
                    col2.metric("Speed", f"{speed_kmh} km/h")
                    col3.metric("⏱️ Travel Time", f"{travel_time['hours']}h {travel_time['minutes']}m {travel_time['seconds']}s")
                    
                    st.info(f"**Total Travel Time: {travel_time['total_hours']} hours**\n\nAt an average speed of {speed_kmh} km/h, it will take approximately **{travel_time['hours']} hours and {travel_time['minutes']} minutes** to travel from {start_place} to {end_place}.")
                    
                    india_map_file = Path(__file__).parent / "india_route_map.html"
                    if route:
                        create_india_route_map(start_place, end_place, route, str(india_map_file))
                    
                    st.subheader("🗺️ Route Map")
                    if india_map_file.exists():
                        map_html = india_map_file.read_text(encoding="utf-8")
                        st.components.v1.html(map_html, height=600, scrolling=False)
                else:
                    st.error(f"❌ Could not calculate route distance. Please select from the autocomplete suggestions above.\n\nIf the city is not in the list, try:\n- Different spelling\n- Adding district/state name\n- Nearby major city")
