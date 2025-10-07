import sys
import re
import numpy as np
import os
import glob

def parse_matrix_from_file(file_path):
    """Parse matrix from a text file with format: {{row1}, {row2}, {row3}}"""
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
        
        # Handle the nested brace format {{row1}, {row2}, {row3}}
        # First remove the outermost braces
        content = content.strip()
        if content.startswith('{{') and content.endswith('}}'):
            content = content[1:-1]  # Remove outer braces, keep inner structure
        
        # Find all rows in curly braces
        pattern = r'\{([^}]+)\}'
        matches = re.findall(pattern, content)
        
        matrix = []
        for match in matches:
            try:
                # Split by comma and convert to float
                row = [float(x.strip()) for x in match.split(',')]
                matrix.append(row)
            except ValueError:
                print(f"Warning: Skipping invalid row: {{{match}}}")
        
        return np.array(matrix)
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def add_matrices(A, B):
    """Add two matrices"""
    return A + B

def subtract_matrices(A, B):
    """Subtract two matrices"""
    return A - B

def strassen_multiply(A, B):
    """
    Multiply two matrices using Strassen's algorithm
    Time complexity: O(n^log2(7)) ≈ O(n^2.807)
    """
    n = A.shape[0]
    
    # Base case: if matrix is small enough, use standard multiplication
    if n <= 64:  # Threshold for switching to standard multiplication
        return np.dot(A, B)
    
    # Ensure matrices are square and power of 2
    if n % 2 != 0:
        # Pad matrices to make them even-sized
        new_size = n + 1
        A_padded = np.zeros((new_size, new_size))
        B_padded = np.zeros((new_size, new_size))
        A_padded[:n, :n] = A
        B_padded[:n, :n] = B
        result = strassen_multiply(A_padded, B_padded)
        return result[:n, :n]
    
    # Divide matrices into quadrants
    mid = n // 2
    
    A11 = A[:mid, :mid]
    A12 = A[:mid, mid:]
    A21 = A[mid:, :mid]
    A22 = A[mid:, mid:]
    
    B11 = B[:mid, :mid]
    B12 = B[:mid, mid:]
    B21 = B[mid:, :mid]
    B22 = B[mid:, mid:]
    
    # Calculate the 7 products using Strassen's formulas
    M1 = strassen_multiply(add_matrices(A11, A22), add_matrices(B11, B22))
    M2 = strassen_multiply(add_matrices(A21, A22), B11)
    M3 = strassen_multiply(A11, subtract_matrices(B12, B22))
    M4 = strassen_multiply(A22, subtract_matrices(B21, B11))
    M5 = strassen_multiply(add_matrices(A11, A12), B22)
    M6 = strassen_multiply(subtract_matrices(A21, A11), add_matrices(B11, B12))
    M7 = strassen_multiply(subtract_matrices(A12, A22), add_matrices(B21, B22))
    
    # Calculate result quadrants
    C11 = add_matrices(subtract_matrices(add_matrices(M1, M4), M5), M7)
    C12 = add_matrices(M3, M5)
    C21 = add_matrices(M2, M4)
    C22 = add_matrices(subtract_matrices(add_matrices(M1, M3), M2), M6)
    
    # Combine quadrants into result matrix
    result = np.zeros((n, n))
    result[:mid, :mid] = C11
    result[:mid, mid:] = C12
    result[mid:, :mid] = C21
    result[mid:, mid:] = C22
    
    return result

def select_file_from_data():
    """Let user select a file from data2 folder"""
    data_folder = "data"
    
    if not os.path.exists(data_folder):
        print("Error: 'data' folder not found.")
        return None
    
    # Get all txt files in data folder
    txt_files = glob.glob(os.path.join(data_folder, "*.txt"))
    
    if not txt_files:
        print("Error: No txt files found in data folder.")
        return None
    
    # Sort files alphabetically
    txt_files.sort()
    
    print("\nAvailable matrix files in data folder:")
    for i, file_path in enumerate(txt_files, 1):
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        print(f"{i:2d}. {filename} ({file_size:,} bytes)")
    
    while True:
        try:
            choice = input(f"\nSelect a file (1-{len(txt_files)}): ").strip()
            if not choice:
                continue
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(txt_files):
                return txt_files[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(txt_files)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None

def main():
    """Main function to multiply matrices and calculate sum"""
    print("=== Matrix Multiplication using Strassen's Algorithm ===")
    
    # Let user select first matrix file
    print("\nSelect first matrix file:")
    file1 = select_file_from_data()
    if file1 is None:
        return
    
    # Let user select second matrix file
    print("\nSelect second matrix file:")
    file2 = select_file_from_data()
    if file2 is None:
        return
    
    print(f"\nSelected files:")
    print(f"  Matrix 1: {os.path.basename(file1)}")
    print(f"  Matrix 2: {os.path.basename(file2)}")
    
    # Parse matrices from files
    print("\nParsing matrices...")
    matrix1 = parse_matrix_from_file(file1)
    matrix2 = parse_matrix_from_file(file2)
    
    if matrix1 is None or matrix2 is None:
        print("Error: Could not parse matrices from files.")
        return
    
    print(f"Matrix 1 size: {matrix1.shape}")
    print(f"Matrix 2 size: {matrix2.shape}")
    
    # Check if matrices can be multiplied
    if matrix1.shape[1] != matrix2.shape[0]:
        print(f"Error: Cannot multiply matrices of sizes {matrix1.shape} and {matrix2.shape}")
        print("Number of columns in first matrix must equal number of rows in second matrix.")
        return
    
    # Check if matrices are square (required for Strassen's algorithm)
    if matrix1.shape[0] != matrix1.shape[1] or matrix2.shape[0] != matrix2.shape[1]:
        print("Note: Strassen's algorithm works best with square matrices. Using standard multiplication.")
        print("Multiplying matrices...")
        result = np.dot(matrix1, matrix2)
    else:
        print(f"Multiplying {matrix1.shape[0]}x{matrix1.shape[1]} matrices using Strassen's algorithm...")
        result = strassen_multiply(matrix1, matrix2)
    
    # Calculate sum of all entries
    total_sum = np.sum(result)
    
    print(f"\nResult:")
    print(f"Sum of all entries in result matrix: {total_sum}")

if __name__ == "__main__":
    main()
