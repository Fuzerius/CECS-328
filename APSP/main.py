import re
import sys
from typing import List, Tuple, Optional

class APSP:
    def __init__(self, graph_file: str):
        """
        Initialize the All-Pairs Shortest Path solver with Floyd-Warshall algorithm.
        Assumes the graph is undirected (bidirectional edges).
        
        Args:
            graph_file: Path to the graph file containing edge list representation
        """
        self.num_vertices = 1000
        self.edges = []
        self.distances = None
        self.predecessors = None
        
        # Load and parse the graph
        self._load_graph(graph_file)
        
        # Compute all-pairs shortest paths
        self._compute_apsp()
    
    def _load_graph(self, graph_file: str):
        """Load and parse the graph from file."""
        print("Loading graph...")
        
        try:
            with open(graph_file, 'r') as f:
                content = f.read()
            
            # Extract all edge tuples using regex
            # Pattern matches {vertex1, vertex2, weight}
            pattern = r'\{(\d+),\s*(\d+),\s*(\d+)\}'
            matches = re.findall(pattern, content)
            
            for match in matches:
                vertex1 = int(match[0])
                vertex2 = int(match[1])
                weight = int(match[2])
                self.edges.append((vertex1, vertex2, weight))
            
            print(f"Loaded {len(self.edges)} edges")
            
        except FileNotFoundError:
            print(f"Error: Could not find file {graph_file}")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading graph: {e}")
            sys.exit(1)
    
    def _compute_apsp(self):
        """Compute all-pairs shortest paths using Floyd-Warshall algorithm."""
        print("Computing all-pairs shortest paths...")
        
        # Initialize distance matrix
        self.distances = [[float('inf')] * (self.num_vertices + 1) for _ in range(self.num_vertices + 1)]
        self.predecessors = [[None] * (self.num_vertices + 1) for _ in range(self.num_vertices + 1)]
        
        # Distance from vertex to itself is 0
        for i in range(1, self.num_vertices + 1):
            self.distances[i][i] = 0
        
        # Add edges to distance matrix (treat as undirected/bidirectional)
        for vertex1, vertex2, weight in self.edges:
            # Add edge in both directions since graph is undirected
            self.distances[vertex1][vertex2] = weight
            self.distances[vertex2][vertex1] = weight
            self.predecessors[vertex1][vertex2] = vertex1
            self.predecessors[vertex2][vertex1] = vertex2
        
        # Floyd-Warshall algorithm
        for k in range(1, self.num_vertices + 1):
            for i in range(1, self.num_vertices + 1):
                for j in range(1, self.num_vertices + 1):
                    if self.distances[i][k] + self.distances[k][j] < self.distances[i][j]:
                        self.distances[i][j] = self.distances[i][k] + self.distances[k][j]
                        self.predecessors[i][j] = self.predecessors[k][j]
        
        print("All-pairs shortest paths computed successfully!")
    
    def get_shortest_distance(self, start: int, end: int) -> Optional[int]:
        """
        Get the shortest distance between two vertices.
        
        Args:
            start: Starting vertex
            end: Ending vertex
            
        Returns:
            Shortest distance, or None if no path exists
        """
        if not (1 <= start <= self.num_vertices and 1 <= end <= self.num_vertices):
            return None
        
        distance = self.distances[start][end]
        return int(distance) if distance != float('inf') else None
    
    def get_shortest_path(self, start: int, end: int) -> Optional[List[int]]:
        """
        Get the shortest path between two vertices.
        
        Args:
            start: Starting vertex
            end: Ending vertex
            
        Returns:
            List of vertices representing the shortest path, or None if no path exists
        """
        if not (1 <= start <= self.num_vertices and 1 <= end <= self.num_vertices):
            return None
        
        if self.distances[start][end] == float('inf'):
            return None
        
        # Reconstruct path
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = self.predecessors[start][current]
        
        path.reverse()
        return path
    
    def query_shortest_path(self, start: int, end: int) -> None:
        """
        Query and display the shortest path between two vertices.
        
        Args:
            start: Starting vertex
            end: Ending vertex
        """
        print(f"\nQuerying shortest path from vertex {start} to vertex {end}:")
        
        distance = self.get_shortest_distance(start, end)
        if distance is None:
            print("No path exists between these vertices.")
            return
        
        path = self.get_shortest_path(start, end)
        
        print(f"Shortest distance: {distance}")
        print(f"Shortest path: {' -> '.join(map(str, path))}")
        print(f"Path length: {len(path)} vertices")

def main():
    """Main function to run the APSP solver."""
    print("All-Pairs Shortest Path (APSP) Solver")
    print("=" * 50)
    
    # Initialize the APSP solver
    try:
        apsp = APSP("graph.txt")
    except Exception as e:
        print(f"Failed to initialize APSP solver: {e}")
        return
    
    print("\nGraph loaded successfully!")
    print(f"Number of vertices: {apsp.num_vertices}")
    print(f"Number of edges: {len(apsp.edges)}")
    
    # Interactive query loop
    while True:
        try:
            print("\n" + "=" * 50)
            print("Enter your query (or 'quit' to exit):")
            print("Format: start_vertex end_vertex")
            print("Example: 1 5")
            
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            # Parse input
            parts = user_input.split()
            if len(parts) != 2:
                print("Error: Please enter exactly two vertices separated by space.")
                continue
            
            try:
                start = int(parts[0])
                end = int(parts[1])
            except ValueError:
                print("Error: Please enter valid integer vertex numbers.")
                continue
            
            # Validate vertex numbers
            if not (1 <= start <= 1000 and 1 <= end <= 1000):
                print("Error: Vertex numbers must be between 1 and 1000.")
                continue
            
            # Query the shortest path
            apsp.query_shortest_path(start, end)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()