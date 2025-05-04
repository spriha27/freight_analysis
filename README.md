# SmartSupplySim - Logistics ETA Simulator (MVP)

## Goal
This project is a command-line tool that simulates freight logistics ETAs. It uses:
1.  A* search algorithm for finding the shortest path on a network graph.
2.  A *synthetically generated* network graph representing locations and routes.
3.  Data derived from US DOT FAF5 (Freight Analysis Framework) datasets (`FAF5 Total Truck Flows by Commodity_2022.csv`).

The simulator calculates a base ETA based on path cost and average speed. It then *simulates* the impact of traffic congestion by:
*   Sampling a representative route from the cleaned FAF dataset.
*   Comparing the total truck trips on that FAF route to a pre-calculated congestion threshold (e.g., 80th percentile).
*   Adding a fixed delay penalty if the FAF route's traffic exceeds the threshold.
*   Flagging the synthetic path as having a potential bottleneck if a delay was added.

## How to Run

1.  **Setup:**
    *   Clone or download this repository.
    *   Ensure you have Python 3 installed.
    *   Create and activate a virtual environment:
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # macOS/Linux
        # .venv\Scripts\activate.bat # Windows Cmd
        # .venv\Scripts\Activate.ps1 # Windows PowerShell
        ```
    *   Install dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    *   Make sure the cleaned data file (`data/cleaned_faf_data.csv`) exists. If not, you might need to run a cleaning script first (not included in this repo version, assumes pre-cleaned data).

2.  **Run Simulation:**
    Execute the main script from the project's root directory (`smartsupplysim`), providing origin and destination node IDs for the synthetic graph. Node IDs range from 0 to 49 by default.

    ```bash
    ./.venv/bin/python3 src/main.py --origin <start_node_id> --destination <end_node_id>
    ```
    Example:
    ```bash
    ./.venv/bin/python3 src/main.py --origin 0 --destination 42
    ```

    Optional: Specify a different data file path:
    ```bash
    ./.venv/bin/python3 src/main.py --origin 5 --destination 30 --datafile path/to/your/data.csv
    ```

## Limitations (MVP Scope)

*   **Synthetic Graph:** The underlying network is randomly generated and does **not** represent the real-world road network. Nodes are abstract locations (0-49).
*   **Simulated FAF Integration:** The link between the synthetic graph path and the FAF data is **simulated**. Delays are based on the traffic volume of *one randomly selected* FAF route, used as a proxy for overall conditions on the synthetic path. There is no direct mapping of FAF zones or routes to the synthetic graph edges. See `Linking FAF5 Assignment Flow Tables to TransCAD and ArcMap Networks.pdf` for context on real-world linking complexity.
*   **Basic ETA:** Calculation uses a simple average speed and a fixed delay penalty. Real-world factors (time of day, specific road types, weather, driver breaks) are not included.
*   **Bottleneck Flagging:** Only indicates if the simulated FAF traffic exceeded the threshold; doesn't perform complex bottleneck analysis.

## Future Work

*   Integrate with real road network data (e.g., OpenStreetMap using libraries like OSMnx).
*   Implement proper network assignment techniques to map FAF zone-to-zone flows onto the actual road network (requires GIS tools or specialized libraries).
*   Develop a more sophisticated ETA model incorporating real-time data, traffic patterns, and other constraints.
*   Perform actual bottleneck *analysis* based on flow aggregation on network links.
*   Implement dispatch optimization algorithms.
*   Deploy the simulation logic as a scalable service (e.g., using a Go-based REST API on Google Cloud Run, as originally envisioned).