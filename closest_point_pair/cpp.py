import math
import sys
import os
import time
import glob

def get_distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def find_closest_pair_brute_force(points):
    """Brute force approach for small sets of points"""
    if len(points) < 2:
        return None, None, float('inf')
    
    min_distance = float('inf')
    closest_pair = (None, None)
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = get_distance(points[i], points[j])
            # Skip overlapping points (distance = 0)
            if distance > 0 and distance < min_distance:
                min_distance = distance
                closest_pair = (points[i], points[j])
    
    return closest_pair[0], closest_pair[1], min_distance

def find_closest_in_strip(strip, d):
    """Find the closest pair in the strip around the dividing line"""
    min_dist = d
    closest_pair = (None, None)
    
    # Sort points in strip by y-coordinate
    strip.sort(key=lambda point: point[1])
    
    # Check each point with at most 7 following points
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j][1] - strip[i][1]) < min_dist:
            dist = get_distance(strip[i], strip[j])
            # Skip overlapping points (distance = 0)
            if dist > 0 and dist < min_dist:
                min_dist = dist
                closest_pair = (strip[i], strip[j])
            j += 1
    
    return closest_pair[0], closest_pair[1], min_dist

def find_closest_pair_rec(px, py):
    """Recursive divide-and-conquer closest pair algorithm"""
    n = len(px)
    
    # Base case: use brute force for small arrays
    if n <= 3:
        return find_closest_pair_brute_force(px)
    
    # Find the middle point
    mid = n // 2
    midpoint = px[mid]
    
    # Divide points in y sorted array around the vertical line
    pyl = [point for point in py if point[0] <= midpoint[0]]
    pyr = [point for point in py if point[0] > midpoint[0]]
    
    # Calculate the smallest distance on left and right recursively
    dl_point1, dl_point2, dl = find_closest_pair_rec(px[:mid], pyl)
    dr_point1, dr_point2, dr = find_closest_pair_rec(px[mid:], pyr)
    
    # Find the smaller of the two halves
    if dl <= dr:
        d = dl
        min_pair = (dl_point1, dl_point2)
    else:
        d = dr
        min_pair = (dr_point1, dr_point2)
    
    # Create an array of points close to the line dividing the left and right halves
    strip = []
    for point in py:
        if abs(point[0] - midpoint[0]) < d:
            strip.append(point)
    
    # Find the closest points in strip
    strip_point1, strip_point2, strip_dist = find_closest_in_strip(strip, d)
    
    # Return the minimum of distance from strip and d
    if strip_dist < d:
        return strip_point1, strip_point2, strip_dist
    else:
        return min_pair[0], min_pair[1], d

def find_closest_pair(points):
    """Find the pair of points with minimum distance using divide-and-conquer algorithm"""
    if len(points) < 2:
        return None, None, float('inf')
    
    # Create sorted copies of points
    px = sorted(points, key=lambda point: point[0])  # Sort by x-coordinate
    py = sorted(points, key=lambda point: point[1])  # Sort by y-coordinate
    
    return find_closest_pair_rec(px, py)

def remove_duplicate_points(points):
    """Remove duplicate/overlapping points from the list"""
    seen = set()
    unique_points = []
    duplicates_removed = 0
    
    for point in points:
        # Round to avoid floating point precision issues
        rounded_point = (round(point[0], 10), round(point[1], 10))
        if rounded_point not in seen:
            seen.add(rounded_point)
            unique_points.append(point)
        else:
            duplicates_removed += 1
    
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate/overlapping points")
    
    return unique_points

def parse_points_from_file(file_path):
    """Parse points from a text file containing points in format: {x1, y1}, {x2, y2}, ..."""
    import re
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Find all coordinate pairs in curly braces (handles both { } and {{ }} formats)
        pattern = r'\{+([^}]+)\}+'
        matches = re.findall(pattern, content)
        
        points = []
        for match in matches:
            try:
                # Split by comma and convert to float
                coords = [float(x.strip()) for x in match.split(',')]
                if len(coords) == 2:
                    points.append((coords[0], coords[1]))
                else:
                    print(f"Warning: Skipping invalid coordinate pair: {{{match}}}")
            except ValueError:
                print(f"Warning: Skipping invalid coordinate pair: {{{match}}}")
        
        return points
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def process_single_file(file_path):
    """Process a single file and return the minimum distance"""
    points = parse_points_from_file(file_path)
    
    if len(points) == 0:
        return None
    
    # Remove duplicate/overlapping points (silently)
    seen = set()
    unique_points = []
    for point in points:
        rounded_point = (round(point[0], 10), round(point[1], 10))
        if rounded_point not in seen:
            seen.add(rounded_point)
            unique_points.append(point)
    
    if len(unique_points) < 2:
        return None
    
    point1, point2, distance = find_closest_pair(unique_points)
    
    if point1 is not None and point2 is not None:
        return distance
    else:
        return None

def main():
    """Main function to process all txt files in data folder"""
    data_folder = "data"
    
    if not os.path.exists(data_folder):
        print("Error: 'data' folder not found.")
        return
    
    # Get all txt files in data folder
    txt_files = glob.glob(os.path.join(data_folder, "*.txt"))
    
    if not txt_files:
        print("Error: No txt files found in data folder.")
        return
    
    # Sort files numerically
    txt_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    
    # Process each file and print only the distance
    for file_path in txt_files:
        filename = os.path.basename(file_path)
        distance = process_single_file(file_path)
        
        if distance is not None:
            print(f"{filename}: {distance:.3f}")
        else:
            print(f"{filename}: No valid result")

if __name__ == "__main__":
    main()
