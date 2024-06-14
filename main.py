from MapGenerator.MapGen_prototype import MapPartitioner
from PathPlanningLibrary.Dijkistra import *

# Example usage
source_x, source_y, source_z = 0, 0, 0
dest_x, dest_y, dest_z = 9, 9, 4

partitioned_map = MapPartitioner.read_map_from_file("map.txt")
if(partitioned_map == None):
    print("Error reading map from file")
    exit()
path = dijkstra(partitioned_map, source_x, source_y, source_z, dest_x, dest_y, dest_z)
if path:
    print("Shortest path:")
    for x, y, z in path:
        print(f"({x}, {y}, {z})", end=" -> ")
else:
    print("No path found.")