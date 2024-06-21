
class Agent():
    def __init__(self ,agent_id , current_coordinates):
        self.agent_id = agent_id
        self.state = "idle"
        self.current_coordinates = current_coordinates
        self.destination_coordinates = None
        self.path = []
        self.path_index = 0
        

    def get_agent_id(self):
        return self.agent_id

    def get_current_coordinates(self):
        return self.current_coordinates
    
    def get_destination_coordinates(self):
        return self.destination_coordinates
    
    def get_state(self):
        return self.state

    def get_next_coordinates(self):
        if self.path_index < len(self.path):
            return self.path[self.path_index]
        else: 
            return None
    
    def wait(self):
        self.state = "idle"
    
    def set_destination(self , destination_coordinates):
        self.state = "transit"
        self.destination_coordinates = destination_coordinates
        self.path = []
        self.path_index = 0
    
    def update_new_path(self , path):
        self.path = path
        self.path_index = 0
    
    def move(self):
        if self.current_coordinates != self.destination_coordinates:
            self.current_coordinates = self.path[self.path_index]
            self.path_index += 1
            #return self.current_coordinates
        else:
            self.state = "idle"
            #return self.current_coordinates
        
    def get_path(self):
        return self.path[self.path_index:] # return the remaining path
        
    def __str__(self):
        return f"Agent {self.agent_id} at {self.current_coordinates} going to {self.destination_coordinates} with state {self.state}"
    

# how to use the above object
# agent = Agent(1, (0,0,0))
# print(agent)
# agent.set_destination((1,1,1))
# print(agent)
# agent.move()
        
    