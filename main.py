from MapGenerator.MapGen_prototype import MapPartitioner
from PathPlanningLibrary.Dijkistra import *
from PathPlanningLibrary.Node import Node
from PathPlanningLibrary.A_Star import *  
from Agent_State import AgentNode
from PackageScheduling import PacMan
from Central_Coordinator import CC

# # Example usage
# source_x, source_y, source_z = 0, 0, 0
# dest_x, dest_y, dest_z = 2, 1, 4



partitioned_map = MapPartitioner.read_map_from_file("map.txt")
CC = CC.CentralCoordinator(partitioned_map)
agent1 = CC.add_agent(1,(0,3,0))
package1 = CC.create_package("package-1",(5,0,0))

CC.package_scheduler(package_name="package-1",package_loc=(5,0,0),package_dest=(9,9,1)) 


# #path = dijkstra(partitioned_map, source_x, source_y, source_z, dest_x, dest_y, dest_z)

# #path = A_star(partitioned_map, source_x, source_y, source_z, dest_x, dest_y, dest_z)




# A_star_algo = Dijkstra(partitioned_map , source_x , source_y , source_z , dest_x, dest_y, dest_z)
# path = A_star_algo.find_path()

# if path:
#     print("Shortest path:")
#     for x, y, z in path:
#         print(f"({x}, {y}, {z})", end=" -> ")
#         #modify the partitioned map to show the path by updating the coordinates of the path to 3
#         partitioned_map[z][x][y] = 3
#         #write the updated partitioned map to solved map.txt
#     MapPartitioner.PathWriter(partitioned_map, "solved_map.txt")

# else:
#     print("No path found.")


# agent1 = AgentNode.Agent(1, (0,0,0))
# agent2 = AgentNode.Agent(2, (0,5,0))

# PacMan = PacMan.PacMan()
# PacMan.add_agent(agent1)
# PacMan.add_agent(agent2)
# PacMan.make_new_package("package-1",(50,0,0))
# Agent = PacMan.get_nearest_agent((50,0,0))
# PacMan.assign_package("package-1",Agent,(0,0,0))
# print(Agent)
# agent_coords = Agent.get_current_coordinates()
# print(agent_coords)
# dest_coords = Agent.get_destination_coordinates()


# A_Star_algo = A_Star(partitioned_map , agent_coords[0],agent_coords[1],agent_coords[2], dest_coords[0],dest_coords[1],dest_coords[2])
# path = A_Star_algo.find_path()
# if path:
#     print("Shortest path:")
#     for x, y, z in path:
#         print(f"({x}, {y}, {z})", end=" -> ")
#         #modify the partitioned map to show the path by updating the coordinates of the path to 3
#         partitioned_map[z][x][y] = 3
#         #write the updated partitioned map to solved map.txt
#     MapPartitioner.PathWriter(partitioned_map, "solved_map.txt")

# else:
#     print("No path found.")

# Agent.update_path(path)

# while Agent.get_state() == "transit":
#     Agent.move()
#     print(Agent)

# PacMan.pick_Package(Agent)
# print(Agent)

# agent_coords = Agent.get_current_coordinates()
# print(agent_coords)
# dest_coords = Agent.get_destination_coordinates()

# A_Star_algo = A_Star(partitioned_map , agent_coords[0],agent_coords[1],agent_coords[2], dest_coords[0],dest_coords[1],dest_coords[2])
# path = A_Star_algo.find_path()
# if path:
#     print("Shortest path:")
#     for x, y, z in path:
#         print(f"({x}, {y}, {z})", end=" -> ")
#         #modify the partitioned map to show the path by updating the coordinates of the path to 3
#         partitioned_map[z][x][y] = 3
#         #write the updated partitioned map to solved map.txt
#     MapPartitioner.PathWriter(partitioned_map, "solved_map.txt")

# else:
#     print("No path found.")

# Agent.update_path(path)

# while Agent.get_state() == "transit":
#     Agent.move()
#     print(Agent)

# PacMan.unassign_package(Agent)
# print(Agent)
