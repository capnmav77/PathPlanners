
class Agent():
    def __init__(self , current_coordinates):
        self.state = "idle"
        self.current_coordinates = current_coordinates
        self.path = []
        self.path_index = 0
        self.destination_coordinates = None

    def set_destination(self , destination_coordinates):
        self.destination_coordinates = destination_coordinates
        self.state = "moving"

    def move(self):
        if self.state == "moving":
            if self.path_index < len(self.path):
                self.current_coordinates = self.path[self.path_index]
                self.path_index += 1
            else:
                self.state = "idle"
                self.path = []
                self.path_index = 0
                self.destination_coordinates = None
                print("Destination reached.")
        else:
            print("Agent is idle.")

    
    def update_path(self , path):
        self.path = path
        self.path_index = 0

    def get_current_coordinates(self):
        return self.current_coordinates
    
    def get_destination_coordinates(self):
        return self.destination_coordinates
    
    def get_state(self):
        return self.state
    
    def get_path(self):
        return self.path
    
    # wip
    
    # def get_nearby_obstacles(self,map):
    #     density_map =  [[0 for i in range(0,3)] for j in range(0,3)]
    #     for i in range(-1,2):
    #         for j in range(-1,2):
    #             if map[self.current_coordinates[2]][self.current_coordinates[0] + i][self.current_coordinates[1] + j] == 0 or  map[self.current_coordinates[2]][self.current_coordinates[0] + i][self.current_coordinates[1] + j] == 2:
                    