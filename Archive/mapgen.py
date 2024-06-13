class Mapgen:
    def Generate_map(self, x, y, z, num_elevators, elevator_placement_middle):
        map = [[[0 for k in range(z)] for j in range(x)] for i in range(y)]

        # Elevator placement middle
        if elevator_placement_middle:
            num_elevators_placed = 0
            if(num_elevators % 2 == 0):
                for i in range(y):
                    map[i][x//2][z//2] = -1
                    num_elevators_placed += 1
                    if num_elevators_placed == num_elevators:
                        break
                    map[i][x//2][z//2 - 1] = -1
                    num_elevators_placed += 1
                    if num_elevators_placed == num_elevators:
                        break
                    map[i][x//2 - 1][z//2] = -1
                    num_elevators_placed += 1
                    if num_elevators_placed == num_elevators:
                        break
                    map[i][x//2 - 1][z//2 - 1] = -1
                    num_elevators_placed += 1
                    if num_elevators_placed == num_elevators:
                        break

        else:
            # Elevator placement corner
            elevators_placed = 0
            x_gap = x
            z_gap = z
            top = True

            while elevators_placed < num_elevators:
                # First, place the elevators in the 4 corners
                if elevators_placed < 4:
                    for i in range(2):
                        for j in range(2):
                            for k in range(y):
                                map[k][i * (x - 1)][j * (z - 1)] = -1
                            elevators_placed += 1
                            if elevators_placed == num_elevators:
                                break
                        if elevators_placed == num_elevators:
                            break
                else:
                    if top:
                        if elevators_placed == num_elevators:
                            break
                        x_gap = x_gap // 2
                        for i in range(y):
                            map[i][x_gap][0] = -1
                        elevators_placed += 1
                        if elevators_placed == num_elevators:
                            break
                        for i in range(y):
                            map[i][x - x_gap - 1][z - 1] = -1
                        elevators_placed += 1
                        top = False
                    else:
                        if elevators_placed == num_elevators:
                            break
                        z_gap = z_gap // 2
                        for i in range(y):
                            map[i][0][z_gap] = -1
                        elevators_placed += 1
                        if elevators_placed == num_elevators:
                            break
                        for i in range(y):
                            map[i][x - 1][z - z_gap - 1] = -1
                        elevators_placed += 1
                        top = True

        return map

    def print_map(self, map):
        for i in range(len(map)):
            for j in range(len(map[0])):
                for k in range(len(map[0][0])):
                    print(map[i][j][k], end=" ")
                print()
            print()
            print("-----------------")

if __name__ == "__main__":
    gen = Mapgen()
    map = gen.Generate_map(10,1, 10, 8, False)
    gen.print_map(map)