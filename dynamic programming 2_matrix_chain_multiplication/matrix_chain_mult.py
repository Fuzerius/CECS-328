#!/usr/bin/env python3
"""
Matrix Chain Multiplication Problem Solver

This script solves the matrix-chain multiplication problem using dynamic programming
to find the minimum number of scalar multiplications needed to compute the product
of a chain of matrices.

The algorithm uses a bottom-up dynamic programming approach with O(n^3) time complexity.
"""

import re
import os
from typing import List, Tuple


def parse_matrix_dimensions(data: str) -> List[Tuple[int, int]]:
    """
    Parse matrix dimensions from the input string format.
    
    Args:
        data: String in format "{{rows1, cols1}, {rows2, cols2}, ...}"
    
    Returns:
        List of tuples representing (rows, cols) for each matrix
    """
    # Remove outer braces and split by matrix pairs
    data = data.strip()
    if not data.startswith('{{') or not data.endswith('}}'):
        raise ValueError("Invalid input format. Expected format: {{rows1, cols1}, {rows2, cols2}, ...}")
    
    # Find all matrix dimension pairs using regex directly on the full string
    pattern = r'\{(\d+),\s*(\d+)\}'
    matches = re.findall(pattern, data)
    
    if not matches:
        raise ValueError("No valid matrix dimensions found")
    
    # Convert to list of tuples
    dimensions = [(int(rows), int(cols)) for rows, cols in matches]
    
    return dimensions


def matrix_chain_order(dimensions: List[Tuple[int, int]]) -> int:
    """
    Calculate the minimum number of scalar multiplications needed to compute
    the product of a chain of matrices using dynamic programming.
    
    Args:
        dimensions: List of (rows, cols) tuples for each matrix
    
    Returns:
        Minimum number of scalar multiplications
    """
    n = len(dimensions)
    if n <= 1:
        return 0
    
    # Extract dimensions array where dims[i] = rows of matrix i
    # and dims[i+1] = cols of matrix i
    # For matrices A0(p0×p1), A1(p1×p2), ..., An-1(pn-1×pn)
    # we need array [p0, p1, p2, ..., pn]
    dims = []
    dims.append(dimensions[0][0])  # First matrix rows
    for rows, cols in dimensions:
        dims.append(cols)  # Each matrix's columns
    
    # Create DP table
    # dp[i][j] = minimum number of multiplications to compute A[i]...A[j]
    dp = [[0 for _ in range(n)] for _ in range(n)]
    
    # Fill the DP table bottom-up
    # l is the chain length
    for l in range(2, n + 1):  # l goes from 2 to n
        for i in range(n - l + 1):  # i goes from 0 to n-l
            j = i + l - 1  # j is the ending index
            dp[i][j] = float('inf')
            
            # Try all possible splits between i and j
            for k in range(i, j):
                # Cost of multiplying A[i]...A[k] and A[k+1]...A[j]
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
    
    return dp[0][n - 1]


def solve_file(filepath: str) -> int:
    """
    Solve the matrix chain multiplication problem for a single file.
    
    Args:
        filepath: Path to the input file
    
    Returns:
        Minimum number of scalar multiplications
    """
    try:
        with open(filepath, 'r') as f:
            data = f.read().strip()
        
        dimensions = parse_matrix_dimensions(data)
        result = matrix_chain_order(dimensions)
        
        return result
    
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return -1


def main():
    """Main function to process all data files."""
    # Resolve data directory relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    results = []
    
    print("Matrix Chain Multiplication Problem Solver")
    print("=" * 50)
    
    # Process all files from 1.txt to 10.txt
    for i in range(1, 11):
        filename = f"{i}.txt"
        filepath = os.path.join(data_dir, filename)
        
        if os.path.exists(filepath):
            print(f"\nProcessing {filename}...")
            result = solve_file(filepath)
            
            if result >= 0:
                print(f"Minimum multiplications: {result}")
                results.append((filename, result))
            else:
                print(f"Failed to process {filename}")
                results.append((filename, "ERROR"))
        else:
            print(f"File {filename} not found")
            results.append((filename, "NOT_FOUND"))
    
    # Print summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    for filename, result in results:
        print(f"{filename}: {result}")
    
    # Test with the example from the problem description
    print("\n" + "=" * 50)
    print("TESTING WITH EXAMPLE")
    print("=" * 50)
    
    # Example: {{5, 5}, {5, 10}, {10, 13}, {13, 10}}
    example_dimensions = [(5, 5), (5, 10), (10, 13), (13, 10)]
    example_result = matrix_chain_order(example_dimensions)
    print(f"Example input: {{5, 5}}, {{5, 10}}, {{10, 13}}, {{13, 10}}")
    print(f"Expected result: 1550")
    print(f"Calculated result: {example_result}")
    print(f"Test {'PASSED' if example_result == 1550 else 'FAILED'}")


if __name__ == "__main__":
    main()
