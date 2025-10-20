import os
import re

class UnionFind:
    """Union-Find (Disjoint Set) data structure for Kruskal's algorithm"""
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
    
    def find(self, x):
        """Find the root of the set containing x with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union two sets containing x and y using rank-based merging"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True

def parse_graph_file(filename):
    """Parse the edge list from the graph file"""
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    # Extract all edges using regex: {v1, v2, weight}
    pattern = r'\{(\d+),\s*(\d+),\s*([\d.]+)\}'
    matches = re.findall(pattern, content)
    
    edges = []
    vertices = set()
    
    for match in matches:
        v1 = int(match[0])
        v2 = int(match[1])
        weight = float(match[2])
        edges.append((weight, v1, v2))
        vertices.add(v1)
        vertices.add(v2)
    
    return edges, vertices

def kruskal_mst(edges, vertices):
    """
    Calculate the minimum spanning tree weight using Kruskal's algorithm
    
    Args:
        edges: List of tuples (weight, v1, v2)
        vertices: Set of all vertices in the graph
    
    Returns:
        Total weight of the minimum spanning tree
    """
    # Sort edges by weight
    edges.sort()
    
    # Initialize Union-Find structure
    uf = UnionFind(vertices)
    
    mst_weight = 0.0
    edges_added = 0
    num_vertices = len(vertices)
    
    # Process edges in order of increasing weight
    for weight, v1, v2 in edges:
        # If adding this edge doesn't create a cycle
        if uf.union(v1, v2):
            mst_weight += weight
            edges_added += 1
            
            # MST has exactly n-1 edges for n vertices
            if edges_added == num_vertices - 1:
                break
    
    return mst_weight

def process_all_files():
    """Process all data files in the current directory"""
    # Get all .txt files and sort them numerically
    files = [f for f in os.listdir('.') if f.endswith('.txt')]
    
    # Sort files numerically (1.txt, 2.txt, ..., 10.txt)
    files.sort(key=lambda x: int(x.split('.')[0]))
    
    print("Minimum Spanning Tree Weights:")
    print("=" * 50)
    
    for filename in files:
        try:
            edges, vertices = parse_graph_file(filename)
            mst_weight = kruskal_mst(edges, vertices)
            print(f"{filename}: {mst_weight:.5f}")
        except Exception as e:
            print(f"{filename}: Error - {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    # Change to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    process_all_files()

