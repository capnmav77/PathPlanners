import heapq
from PathPlanningLibrary.Node import Node

class Dijkstra: 
    def __init__(self, partitioned_map,diagonal_traversal=False):
        self.partitioned_map = partitioned_map
        self.diagonal_traversal = diagonal_traversal
        
    def find_path(self, source_x , source_y, source_z, dest_x, dest_y, dest_z):
        if source_z == dest_z:
            return self.find_path_on_level(source_x,source_y,source_z , dest_x, dest_y, dest_z)
        else : 
            start_elevator = self.find_nearest_elevator(source_x,source_y,source_z)
            if start_elevator is None:
                return None
    
        source_to_elevator = self.find_path_on_level(source_x,source_y,source_z , start_elevator[0], start_elevator[1],source_z)
        elevator_to_dest = self.find_path_on_level(start_elevator[0],start_elevator[1],dest_z , dest_x, dest_y ,dest_z)

        if source_to_elevator and elevator_to_dest:
            return source_to_elevator + elevator_to_dest
        else:
            print("Error - 03 : failed to get source to destination , try a different map")
            return None

    def find_path_on_level(self, source_x, source_y, source_z, dest_x, dest_y, dest_z):
        pq = [(0, Node(source_x, source_y, source_z))]
        visited = set()
        while pq:
            cost, node = heapq.heappop(pq)
            if (node.x, node.y, node.z) == (dest_x, dest_y, dest_z):
                path = []
                while node:
                    path.append((node.x, node.y, node.z))
                    node = node.parent
                return path[::-1]

            if (node.x, node.y, node.z) in visited:
                continue

            visited.add((node.x, node.y, node.z))
            if self.diagonal_traversal==False:
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_x, new_y = node.x + dx, node.y + dy
                    if 0 <= new_x < len(self.partitioned_map[0]) and 0 <= new_y < len(self.partitioned_map[0][0]) and self.partitioned_map[source_z][new_x][new_y] != 0:
                        heapq.heappush(pq, (cost + 1, Node(new_x, new_y, source_z, node)))
            else:
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
                    new_x, new_y = node.x + dx, node.y + dy
                    if 0 <= new_x < len(self.partitioned_map[0]) and 0 <= new_y < len(self.partitioned_map[0][0]) and self.partitioned_map[source_z][new_x][new_y] != 0:
                        if dx == 0 or dy == 0:
                            heapq.heappush(pq, (cost + 1, Node(new_x, new_y, source_z, node, cost + 1)))
                        else:
                            heapq.heappush(pq, (cost + 1.4, Node(new_x, new_y, source_z, node, cost + 1.4)))

        return None
        
        
    def find_nearest_elevator(self, x, y, z):
        min_dist = float('inf')
        nearest_elevator = None
        for i in range(len(self.partitioned_map[z])): # len(partitioned_map[z]) is the number of rows
            for j in range(len(self.partitioned_map[z][0])): # len(partitioned_map[z][0]) is the number of columns
                if self.partitioned_map[z][i][j] == -1:
                    dist = abs(i - x) + abs(j - y) # Manhattan distance
                    if dist < min_dist:
                        min_dist = dist
                        nearest_elevator = (i, j)
        return nearest_elevator
