import random

class MapPartitioner:
    def __init__(self, x, y, z, num_elevators):
        self.x = x
        self.y = y
        self.z = z
        self.num_elevators = num_elevators
        self.partitioned_map = [[[1 for _ in range(x)] for _ in range(y)] for _ in range(z)] # how to call -> partitioned_map[z][x][y]
        self.sector_size = 3
        self.coordinates_center = []

    def recal_sector(self, start_x, start_y):
        center_x = start_x + self.sector_size // 2
        center_y = start_y + self.sector_size // 2
        if center_x < self.x and center_y < self.y:
            self.coordinates_center.append((center_x, center_y))

    def generate_obstacles(self, num_obstacles):
        obstacles = [1, 2, 3]  # number of blocks for each obstacle
        for k in range(0, self.z):
            for _ in range(num_obstacles):
                x = random.randint(0, self.x - 1)
                y = random.randint(0, self.y - 1)
                obstacle = random.choice(obstacles)
                orientation = random.randint(0, 1)
                if orientation == 0:
                    for i in range(obstacle):
                        if y + i < self.y and self.partitioned_map[0][x][y + i] != -1:
                            self.partitioned_map[k][x][y + i] = 0
                else:
                    for i in range(obstacle):
                        if x + i < self.x and self.partitioned_map[0][x + i][y] != -1:
                            self.partitioned_map[k][x + i][y] = 0

    def partition_map(self):
        for i in range(0, self.x, self.sector_size):
            for j in range(0, self.y, self.sector_size):
                self.recal_sector(i, j)

        num_elevators_placed = 0
        while num_elevators_placed < self.num_elevators and self.coordinates_center:
            i = random.randint(0, len(self.coordinates_center) - 1)
            x, y = self.coordinates_center[i]
            for j in range(0,self.z):
                self.partitioned_map[j][x][y] = -1
            num_elevators_placed += 1
            self.coordinates_center.pop(i)
    
    def add_picking_station(self):
        # picking station is in the form of a 4X1 rectangle at the middle 
        for j in range(self.x//2 - 2, self.x//2 + 2):
            self.partitioned_map[0][j][0] = 5
            self.partitioned_map[0][j][1] = 1
            self.partitioned_map[0][j][2] = 1

    def print_map(self):
        for z_slice in self.partitioned_map:
            for row in z_slice:
                print(row)
            print()

    def write_map_to_file(self, filename):
        with open(filename, 'w') as file:
            file.truncate(0)  # Erase previous contents
            for z_slice in self.partitioned_map:
                for row in z_slice:
                    file.write(' '.join(map(str, row)) + '\n')
                file.write('\n')

    @staticmethod
    def read_map_from_file(filename):
        partitioned_map = []
        z_slice = []
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():  # Non-empty line
                    row = list(map(int, line.split()))
                    z_slice.append(row)
                else:  # Empty line indicates a new z slice
                    partitioned_map.append(z_slice)
                    z_slice = []
            if z_slice:  # Add the last z slice if it exists
                partitioned_map.append(z_slice)
        return partitioned_map
    
    @staticmethod
    def PathWriter(map_data, filename):
        with open(filename, 'w') as file:
            file.truncate(0)
            for z_slice in map_data:
                for row in z_slice:
                    file.write(' '.join(map(str, row)) + '\n')
                file.write('\n')



def get_map_from_file(filename):
    print("Reading map from file")
    partitioned_map = MapPartitioner.read_map_from_file(filename)
    for z_slice in partitioned_map:
        for row in z_slice:
            print(row)
        print()
    # Now you can use partitioned_map for further processing

def get_map(x, y,z, num_elevators, num_obstacles, filename):
    partitioner = MapPartitioner(x, y, z, num_elevators)
    partitioner.partition_map()
    partitioner.generate_obstacles(num_obstacles)
    partitioner.add_picking_station()
    partitioner.print_map()
    partitioner.write_map_to_file(filename)



if __name__ == "__main__":
    get_map(100, 100, 5, 12, 1000, "../map.txt")
    #get_map_from_file("map.txt")
