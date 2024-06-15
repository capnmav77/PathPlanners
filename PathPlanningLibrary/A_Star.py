import heapq
from MapGenerator.MapGen_prototype import MapPartitioner

class Node:
    def __init__(self, x, y, z, parent=None, cost=0):
        self.x = x
        self.y = y
        self.z = z
        self.parent = parent
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

def find_nearest_elevator(partitioned_map, x, y, z):
    min_dist = float('inf')
    nearest_elevator = None
    for i in range(len(partitioned_map[z])): # len(partitioned_map[z]) is the number of rows
        for j in range(len(partitioned_map[z][0])): # len(partitioned_map[z][0]) is the number of columns
            if partitioned_map[z][i][j] == -1:
                dist = abs(i - x) + abs(j - y) # Manhattan distance
                if dist < min_dist:
                    min_dist = dist
                    nearest_elevator = (i, j)
    return nearest_elevator

def A_star(partitioned_map, source_x, source_y, source_z, dest_x, dest_y, dest_z):
    if source_z == dest_z:
        # Source and destination are on the same level
        return find_path_on_level_heuristic(partitioned_map, source_x, source_y, source_z, dest_x, dest_y, dest_z)
    else:
        # Find the nearest elevator on the source level
        start_elevator = find_nearest_elevator(partitioned_map, source_x, source_y, source_z)
        if start_elevator is None:
            return None

        # Combine paths: source -> start_elevator, start_elevator -> end_elevator, end_elevator -> destination
        source_to_start_elevator = find_path_on_level_heuristic(partitioned_map, source_x, source_y, source_z, start_elevator[0], start_elevator[1], source_z)
        end_elevator_to_dest = find_path_on_level_heuristic(partitioned_map, start_elevator[0], start_elevator[1], dest_z, dest_x, dest_y, dest_z)

        if source_to_start_elevator and end_elevator_to_dest:
            return source_to_start_elevator + end_elevator_to_dest
        else:
            return None

def find_path_on_level_heuristic(partitioned_map, source_x, source_y, source_z, dest_x, dest_y, dest_z):
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
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
            new_x, new_y = node.x + dx, node.y + dy
            if 0 <= new_x < len(partitioned_map[0]) and 0 <= new_y < len(partitioned_map[0][0]) and partitioned_map[source_z][new_x][new_y] != 0:
                heuristic_factor = abs(new_x - dest_x) + abs(new_y - dest_y)
                if dx == 0 or dy == 0:
                    heapq.heappush(pq, (cost + 1 + heuristic_factor, Node(new_x, new_y, source_z, node, cost + 1 + heuristic_factor)))
                else:
                    heapq.heappush(pq, (cost + 1.4 + heuristic_factor, Node(new_x, new_y, source_z, node, cost + 1.4 + heuristic_factor)))

    return None