import os
from collections import Counter
import heapq


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    """Build a Huffman tree from the given text."""
    if not text:
        return None
    
    # Count frequency of each character
    freq_map = Counter(text)
    
    # Special case: only one unique character
    if len(freq_map) == 1:
        char, freq = list(freq_map.items())[0]
        root = HuffmanNode(char, freq)
        return root
    
    # Create a priority queue (min heap) with nodes
    heap = []
    for char, freq in freq_map.items():
        node = HuffmanNode(char, freq)
        heapq.heappush(heap, node)
    
    # Build the Huffman tree
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        heapq.heappush(heap, merged)
    
    return heap[0]


def build_codes(root, current_code="", codes=None):
    """Build Huffman codes by traversing the tree."""
    if codes is None:
        codes = {}
    
    if root is None:
        return codes
    
    # Leaf node
    if root.char is not None:
        # Special case: if root is the only node (one unique character)
        if current_code == "":
            codes[root.char] = "0"
        else:
            codes[root.char] = current_code
        return codes
    
    # Traverse left and right
    build_codes(root.left, current_code + "0", codes)
    build_codes(root.right, current_code + "1", codes)
    
    return codes


def calculate_huffman_length(text):
    """Calculate the total length in bits of Huffman encoding for the given text."""
    if not text:
        return 0
    
    # Build Huffman tree
    root = build_huffman_tree(text)
    
    # Build codes
    codes = build_codes(root)
    
    # Calculate total length
    total_bits = 0
    for char in text:
        total_bits += len(codes[char])
    
    return total_bits


def process_data_folder(folder_path="data"):
    """Process all txt files in the data folder."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return
    
    # Get all txt files and sort them numerically
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    txt_files.sort(key=lambda x: int(x.split('.')[0]))
    
    for filename in txt_files:
        filepath = os.path.join(folder_path, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Calculate Huffman encoding length
            length = calculate_huffman_length(text)
            
            print(f"{filename} : {length} bits")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    process_data_folder()

