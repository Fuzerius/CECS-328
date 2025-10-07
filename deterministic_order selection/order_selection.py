import os
import re
import glob

def parse_file_content(file_path):
    """Parse k and list from file with format: {k, {list of numbers}}"""
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
        
        # Remove outer braces and split by the first comma to separate k and list
        content = content.strip('{}')
        
        # Find the first comma that separates k from the list
        first_comma = content.find(',')
        if first_comma == -1:
            raise ValueError("Invalid format: no comma found")
        
        # Extract k
        k_str = content[:first_comma].strip()
        k = int(k_str)
        
        # Extract the list part
        list_part = content[first_comma + 1:].strip()
        
        # Remove braces from list and parse numbers
        list_part = list_part.strip('{}')
        
        # Split by comma and convert to integers
        numbers = []
        for num_str in list_part.split(','):
            num_str = num_str.strip()
            if num_str:  # Skip empty strings
                numbers.append(int(num_str))
        
        return k, numbers
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None, None
    except Exception as e:
        print(f"Error parsing file '{file_path}': {e}")
        return None, None

def insertion_sort(arr):
    """Simple insertion sort for small arrays"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def median_of_medians(arr, k):
    """
    Deterministic Order Selection Algorithm (Median of Medians)
    Finds the kth smallest element in O(n) worst-case time
    
    Args:
        arr: List of numbers
        k: Position (1-indexed) of element to find in sorted order
    
    Returns:
        The kth smallest element
    """
    if len(arr) == 1:
        return arr[0]
    
    # Base case: use insertion sort for small arrays
    if len(arr) <= 5:
        sorted_arr = insertion_sort(arr[:])
        return sorted_arr[k - 1]
    
    # Step 1: Divide array into groups of 5
    groups = []
    for i in range(0, len(arr), 5):
        group = arr[i:i + 5]
        groups.append(group)
    
    # Step 2: Find median of each group
    medians = []
    for group in groups:
        sorted_group = insertion_sort(group[:])
        median_idx = len(sorted_group) // 2
        medians.append(sorted_group[median_idx])
    
    # Step 3: Find median of medians recursively
    if len(medians) == 1:
        pivot = medians[0]
    else:
        median_pos = (len(medians) + 1) // 2
        pivot = median_of_medians(medians, median_pos)
    
    # Step 4: Partition array around pivot
    less = []
    equal = []
    greater = []
    
    for num in arr:
        if num < pivot:
            less.append(num)
        elif num == pivot:
            equal.append(num)
        else:
            greater.append(num)
    
    # Step 5: Recursively search in appropriate partition
    if k <= len(less):
        return median_of_medians(less, k)
    elif k <= len(less) + len(equal):
        return pivot
    else:
        return median_of_medians(greater, k - len(less) - len(equal))

def find_kth_element(numbers, k):
    """Find kth smallest element using Deterministic Order Selection"""
    if k < 1 or k > len(numbers):
        return None
    
    return median_of_medians(numbers[:], k)  # Pass a copy to avoid modifying original

def process_file(file_path):
    """Process a single file and return the kth element"""
    k, numbers = parse_file_content(file_path)
    
    if k is None or numbers is None:
        return None
    
    if k < 1 or k > len(numbers):
        print(f"Warning: k={k} is out of range for list of size {len(numbers)}")
        return None
    
    result = find_kth_element(numbers, k)
    return result

def main():
    """Process all files in data3 folder"""
    data3_folder = "data"
    
    if not os.path.exists(data3_folder):
        print("Error: 'data' folder not found.")
        return
    
    # Get all txt files in data3 folder
    txt_files = glob.glob(os.path.join(data3_folder, "*.txt"))
    
    if not txt_files:
        print("Error: No txt files found in data folder.")
        return
    
    # Sort files numerically
    txt_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    
    print("=== Deterministic Order Selection Results ===")
    print("Processing files using Median of Medians algorithm (O(n) time complexity)")
    print()
    
    # Process each file
    for file_path in txt_files:
        filename = os.path.basename(file_path)
        result = process_file(file_path)
        
        if result is not None:
            print(f"{filename}: {result}")
        else:
            print(f"{filename}: Error processing file")

if __name__ == "__main__":
    main()
