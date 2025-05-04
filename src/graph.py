import random
import heapq

class Graph:
    """Represents our synthetic network map using an adjacency list."""
    def __init__(self):
        self.edges = {}
        self.nodes = set()

    def add_node(self, node):
        if node not in self.edges:
            self.edges[node] = []
            self.nodes.add(node)

    def add_edge(self, from_node, to_node, weight):
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node].append((to_node, weight))
        self.edges[to_node].append((from_node, weight))

    def get_neighbors(self, node):
        return self.edges.get(node, [])

def create_synthetic_graph(num_nodes=50, edge_probability=0.15):
    """Creates a random graph for simulation."""
    print(f"Creating a synthetic graph with {num_nodes} nodes...")
    graph = Graph()
    for i in range(num_nodes):
        graph.add_node(i)

    all_nodes = list(graph.nodes)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                weight = random.uniform(10, 500)
                graph.add_edge(all_nodes[i], all_nodes[j], weight)

    print(f"Graph created with {len(graph.nodes)} nodes and potential edges.")
    return graph

def heuristic(node, goal):
    """Heuristic function for A*. For synthetic graph, use 0."""
    return 0

def a_star_search(graph, start_node, goal_node):
    """Performs A* search on the graph."""
    if start_node not in graph.nodes or goal_node not in graph.nodes:
        print("Error: Start or goal node not in graph.")
        return None, float('inf')

    pq = [(0 + heuristic(start_node, goal_node), 0, start_node, [start_node])]
    visited_costs = {start_node: 0} 

    while pq:
        _, cost_so_far, current_node, path = heapq.heappop(pq)

        if current_node == goal_node:
            print(f"Path found from {start_node} to {goal_node} with cost {cost_so_far:.2f}")
            return path, cost_so_far

        for neighbor, weight in graph.get_neighbors(current_node):
            new_cost = cost_so_far + weight
            if neighbor not in visited_costs or new_cost < visited_costs[neighbor]:
                visited_costs[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal_node)
                new_path = path + [neighbor]
                heapq.heappush(pq, (priority, new_cost, neighbor, new_path))

    print(f"No path found from {start_node} to {goal_node}.")
    return None, float('inf') 