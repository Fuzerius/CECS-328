import os
import re

def max_crossing_sum(arr, left, mid, right):
    """
    Find the maximum sum of a subsequence that crosses the midpoint.
    """
    # Find maximum sum starting from mid and going left
    left_sum = float('-inf')
    current_sum = 0
    for i in range(mid, left - 1, -1):
        current_sum += arr[i]
        if current_sum > left_sum:
            left_sum = current_sum
    
    # Find maximum sum starting from mid+1 and going right
    right_sum = float('-inf')
    current_sum = 0
    for i in range(mid + 1, right + 1):
        current_sum += arr[i]
        if current_sum > right_sum:
            right_sum = current_sum
    
    # Return sum of elements on both sides of mid
    return left_sum + right_sum

def max_subarray_sum_recursive(arr, left, right):
    """
    Divide and conquer approach to find maximum subsequence sum.
    The maximum subsequence is either:
    1. Entirely in the left half
    2. Entirely in the right half
    3. Crosses the middle
    """
    # Base case: only one element
    if left == right:
        return arr[left]
    
    # Find middle point
    mid = (left + right) // 2
    
    # Return maximum of:
    # 1. Maximum subarray sum in left half
    # 2. Maximum subarray sum in right half
    # 3. Maximum subarray sum that crosses the midpoint
    return max(
        max_subarray_sum_recursive(arr, left, mid),
        max_subarray_sum_recursive(arr, mid + 1, right),
        max_crossing_sum(arr, left, mid, right)
    )

def max_subarray_sum(arr):
    """
    Wrapper function to find maximum subsequence sum.
    """
    if not arr:
        return 0
    return max_subarray_sum_recursive(arr, 0, len(arr) - 1)

def parse_data_file(filepath):
    """
    Parse a data file and extract the list of numbers.
    """
    with open(filepath, 'r') as f:
        content = f.read().strip()
    
    # Extract numbers from the format {n1, n2, n3, ...}
    # Remove curly braces and split by comma
    content = content.strip('{}')
    numbers = [int(x.strip()) for x in content.split(',')]
    return numbers

def main():
    data_folder = 'data'
    results = []
    
    # Process files 1.txt through 10.txt
    for i in range(1, 11):
        filename = f'{i}.txt'
        filepath = os.path.join(data_folder, filename)
        
        try:
            # Parse the data file
            numbers = parse_data_file(filepath)
            
            # Find maximum subsequence sum
            max_sum = max_subarray_sum(numbers)
            
            results.append({
                'file': filename,
                'numbers': numbers,
                'max_sum': max_sum
            })
            
            print(f"File: {filename}")
            print(f"Numbers: {numbers}")
            print(f"Maximum Subsequence Sum: {max_sum}")
            print("-" * 80)
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            print("-" * 80)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY OF RESULTS")
    print("=" * 80)
    for result in results:
        print(f"{result['file']:10s} -> Maximum Subsequence Sum: {result['max_sum']}")

if __name__ == "__main__":
    main()

