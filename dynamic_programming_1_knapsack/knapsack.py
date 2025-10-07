#!/usr/bin/env python3
"""
Knapsack Problem Solver

This script processes all txt files in the Knapsack/data directory and solves
the 0/1 knapsack problem for each file. The input format is:
{C, {{v_1, w_1, 1}, {v_2, w_2, 1}, ..., {v_n, w_n, 1}}}

Where:
- C: knapsack capacity
- v_i: value of item i
- w_i: weight of item i
- 1: count (always 1 for 0/1 knapsack)
"""

import os
import re
import ast
from typing import List, Tuple


def parse_input_file(file_path: str) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Parse a knapsack input file and return capacity and items.
    
    Args:
        file_path: Path to the input file
        
    Returns:
        Tuple of (capacity, list of (value, weight) tuples)
    """
    with open(file_path, 'r') as f:
        content = f.read().strip()
    
    # Parse the input format: {capacity, {{v1, w1, 1}, {v2, w2, 1}, ...}}
    try:
        # Convert curly braces to square brackets for ast.literal_eval
        # Replace outer braces with brackets
        content = content.replace('{', '[', 1).replace('}', ']', 1)
        # Replace inner braces with brackets
        content = content.replace('{', '[').replace('}', ']')
        
        # Use ast.literal_eval to safely parse the input
        parsed = ast.literal_eval(content)
        capacity = parsed[0]
        items = [(item[0], item[1]) for item in parsed[1]]
        return capacity, items
    except (ValueError, SyntaxError, IndexError) as e:
        print(f"Error parsing {file_path}: {e}")
        return 0, []


def knapsack_01(capacity: int, items: List[Tuple[int, int]]) -> Tuple[int, List[int]]:
    """
    Solve the 0/1 knapsack problem using dynamic programming.
    
    Args:
        capacity: Maximum weight capacity
        items: List of (value, weight) tuples
        
    Returns:
        Tuple of (max_value, list of selected item indices)
    """
    n = len(items)
    if n == 0 or capacity == 0:
        return 0, []
    
    # Create DP table: dp[i][w] = max value using first i items with weight w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Fill the DP table
    for i in range(1, n + 1):
        value, weight = items[i - 1]
        for w in range(capacity + 1):
            # Don't take the item
            dp[i][w] = dp[i - 1][w]
            
            # Take the item if it fits
            if weight <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weight] + value)
    
    # Backtrack to find selected items
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)  # Convert to 0-based indexing
            w -= items[i - 1][1]
    
    return dp[n][capacity], selected_items


def calculate_total_weight(items: List[Tuple[int, int]], selected_indices: List[int]) -> int:
    """Calculate total weight of selected items."""
    return sum(items[i][1] for i in selected_indices)


def solve_knapsack_file(file_path: str) -> None:
    """
    Solve knapsack problem for a single file and print results.
    
    Args:
        file_path: Path to the input file
    """
    filename = os.path.basename(file_path)
    print(f"\n=== Processing {filename} ===")
    
    # Parse input
    capacity, items = parse_input_file(file_path)
    if not items:
        print(f"Failed to parse {filename}")
        return
    
    # Solve knapsack problem
    max_value, selected_indices = knapsack_01(capacity, items)
    
    # Print results
    print(f"Maximum potential profit: {max_value}")


def main():
    """Main function to process all knapsack files."""
    # Use the main data folder
    data_dir = 'data'
    
    if not os.path.exists(data_dir):
        print(f"Data directory not found: {data_dir}")
        return
    
    # Get all txt files in the data directory
    txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    txt_files.sort(key=lambda x: int(x.split('.')[0]))  # Sort numerically
    
    if not txt_files:
        print("No txt files found in data directory")
        return
    
    print(f"Found {len(txt_files)} files to process:")
    for f in txt_files:
        print(f"  - {f}")
    
    # Process each file
    for filename in txt_files:
        file_path = os.path.join(data_dir, filename)
        solve_knapsack_file(file_path)
    
    print(f"\n=== Completed processing all {len(txt_files)} files ===")


if __name__ == "__main__":
    main()


