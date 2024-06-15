from MapGenerator.MapGen_prototype import MapPartitioner
from PathPlanningLibrary.Dijkistra import *
from PathPlanningLibrary.Node import Node
from PathPlanningLibrary.A_Star import *  

# Example usage
source_x, source_y, source_z = 0, 0, 0
dest_x, dest_y, dest_z = 2, 1, 4

partitioned_map = MapPartitioner.read_map_from_file("map.txt")

#path = dijkstra(partitioned_map, source_x, source_y, source_z, dest_x, dest_y, dest_z)

#path = A_star(partitioned_map, source_x, source_y, source_z, dest_x, dest_y, dest_z)
A_star_algo = Dijkstra(partitioned_map , source_x , source_y , source_z , dest_x, dest_y, dest_z)
path = A_star_algo.find_path()

if path:
    print("Shortest path:")
    for x, y, z in path:
        print(f"({x}, {y}, {z})", end=" -> ")
        #modify the partitioned map to show the path by updating the coordinates of the path to 3
        partitioned_map[z][x][y] = 3
        #write the updated partitioned map to solved map.txt
    MapPartitioner.PathWriter(partitioned_map, "solved_map.txt")

else:
    print("No path found.")