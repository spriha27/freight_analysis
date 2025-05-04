import argparse 
import random   
import time     

from src.data_loader import load_faf_data
from src.graph import create_synthetic_graph, a_star_search

AVERAGE_SPEED_KMPH = 70 
DELAY_PENALTY_HOURS = 0.75 
NUM_SYNTHETIC_NODES = 50 
EDGE_PROBABILITY = 0.15 

def format_time(hours):
    """Converts decimal hours to hours and minutes string."""
    if hours is None or hours == float('inf'):
        return "N/A"
    total_minutes = int(hours * 60)
    h = total_minutes // 60
    m = total_minutes % 60
    return f"{h} hours, {m} minutes"

def run_simulation(origin_node, dest_node, faf_data_filepath):
    """Runs the core simulation logic."""

    faf_df, congestion_threshold = load_faf_data(faf_data_filepath)
    if faf_df is None:
        print("Exiting due to data loading error.")
        return

    if congestion_threshold is None:
         print("Warning: Congestion threshold not available. Delay simulation might be inaccurate.")
         
    sample_size = min(10000, len(faf_df))
    faf_sample = faf_df.sample(n=sample_size).reset_index(drop=True)
    print(f"Using a sample of {sample_size} FAF routes for traffic simulation.")

    graph = create_synthetic_graph(num_nodes=NUM_SYNTHETIC_NODES, edge_probability=EDGE_PROBABILITY)

    if origin_node >= NUM_SYNTHETIC_NODES or dest_node >= NUM_SYNTHETIC_NODES or origin_node < 0 or dest_node < 0:
         print(f"Error: Origin ({origin_node}) or Destination ({dest_node}) node ID is out of range (0-{NUM_SYNTHETIC_NODES-1}).")
         return
    if origin_node == dest_node:
         print("Origin and Destination are the same.")
         return

    print(f"\nSearching for path from node {origin_node} to {dest_node}...")
    path, cost = a_star_search(graph, origin_node, dest_node)

    if path:
        print("--- Route Found ---")
        print(f"Path: {' -> '.join(map(str, path))}")
        print(f"Base Cost (e.g., distance/time units): {cost:.2f}")

        base_eta_hours = cost / AVERAGE_SPEED_KMPH
        print(f"Base Estimated Time (at {AVERAGE_SPEED_KMPH} km/h): {format_time(base_eta_hours)}")

        total_delay_hours = 0
        bottleneck_reason = "None"

        if congestion_threshold is not None and not faf_sample.empty:
            representative_faf_route = faf_sample.sample(1).iloc[0]
            simulated_traffic = representative_faf_route['tot_trips']
            faf_route_id = representative_faf_route['route_id']

            print(f"Simulating traffic based on representative FAF route ID {faf_route_id} (Total Trips: {simulated_traffic:.2f})")

            if simulated_traffic > congestion_threshold:
                print(f"High traffic detected (>{congestion_threshold:.2f}). Applying delay penalty.")
                total_delay_hours = DELAY_PENALTY_HOURS
                bottleneck_reason = f"Simulated congestion based on FAF route {faf_route_id} (Trips: {simulated_traffic:.2f})"
            else:
                print("Simulated traffic volume below congestion threshold.")

        else:
             print("Skipping traffic delay simulation (no threshold or FAF sample data).")


        final_eta_hours = base_eta_hours + total_delay_hours
        print("\n--- Simulation Results ---")
        print(f"Simulated Delay: {format_time(total_delay_hours)}")
        print(f"Potential Bottleneck Reason: {bottleneck_reason}")
        print(f"Final Predicted ETA: {format_time(final_eta_hours)}")

    else:
        print("--- No Route Found ---")
        print(f"Could not find a path between node {origin_node} and node {dest_node}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SmartSupplySim - Logistics ETA Simulator (MVP)")
    parser.add_argument("--origin", type=int, required=True, help="Starting node ID (e.g., 0)")
    parser.add_argument("--destination", type=int, required=True, help="Ending node ID (e.g., 49)")
    parser.add_argument("--datafile", type=str, default="cleaned_dataset.csv", help="Path to the cleaned FAF data CSV file (relative to project root)")

    args = parser.parse_args()

    print("Starting SmartSupplySim...")
    run_simulation(args.origin, args.destination, args.datafile)
    print("\nSimulation finished.")