from Agent_State import AgentNode
from PackageScheduling import PacMan
from PathPlanningLibrary import A_Star
from MapGenerator import MapGen_prototype
from Central_Coordinator import Collision_Manager


class CentralCoordinator:
    def __init__(self, partitioned_map):
        self.agents = []
        self.PacMan = PacMan.PacMan()
        self.agent_Packages_map = {}
        self.Partitioned_map = partitioned_map#MapGen_prototype.MapPartitioner.read_map_from_file("../map.txt")
        self.A_star_algo = A_Star.A_Star(partitioned_map=self.Partitioned_map,diagonal_traversal=False)
        self.collision_Manager = Collision_Manager.Collision_Manager()
        
    #agent management functions
    def add_agent(self,agent_id,current_coordinates):
        agent = AgentNode.Agent(agent_id,current_coordinates)
        self.agents.append(agent)
        return agent
    

    def remove_agent(self,agent): 
        if self.agents.count(agent) == 1:
            self.agents.remove(agent)
            del agent
        else:
            print("Agent does not exist.")


    def get_agent(self,agent_id):
        for agent in self.agents:
            if agent.get_agent_id() == agent_id:
                return agent
        
        return None
    

    #package management functions
    def create_package(self,package_name,package_loc,package_dest=None):
        return self.PacMan.make_new_package(package_name,package_loc,package_dest)
    

    def remove_package(self,package):
        self.PacMan.remove_Package(package)


    def assign_package(self,package_name,agent_id,destination_coordinates):
        agent = self.get_agent(agent_id)
        if agent.get_state() == "transit":
            print("Agent is already carrying a package.")
            return False
        package = self.PacMan.get_Package(package_name)
        if agent != None and package != None:
            agent.set_destination(package.get_package_loc())
            package.set_destination(destination_coordinates)
            self.agent_Packages_map[agent] = package
            print(f"Package {package.get_package_name()} assigned to agent {agent.get_agent_id()}.")
            return True
        else:
            print("Agent or Package does not exist.here's the list of agents and packages:")
            for agent in self.agents:
                print("Agent :" + agent.get_agent_id()) 
            for package in self.PacMan.Packages:
                print("Package:" + package.get_package_name())
            return False


    def pick_package(self,agent_id):
        agent = self.get_agent(agent_id)
        if agent in self.agent_Packages_map:
            agent_loc = agent.get_current_coordinates()
            package_loc = agent.get_destination_coordinates()
            path = self.A_star_algo.find_path(agent_loc[0],agent_loc[1],agent_loc[2],package_loc[0],package_loc[1],package_loc[2])   

            if(path == None):
                print("Error - 02 : failed to get source to destination , try a different map")
                return None
            
            #path = path[1:]
            agent.update_new_path(path) 
            self.update_map(path)


            while(agent.get_current_coordinates() != package_loc):
                if(self.collision_Manager.detect_collision(agent, self.agents)):
                    agent.wait()
                    #implement the deadlock avoidance function here
                else:
                    agent.move()

                    coords = agent.get_current_coordinates()

                    print(f"Agent {agent.get_agent_id()} at {coords}")

                    if(self.Partitioned_map[coords[2]][coords[0]][coords[1]] != 5 and self.Partitioned_map[coords[2]][coords[0]][coords[1]] != -1):
                        self.Partitioned_map[coords[2]][coords[0]][coords[1]]  -= 2

                    MapGen_prototype.MapPartitioner.PathWriter(self.Partitioned_map,"map.txt")

                    scan = input("Press any key to continue")



            print("agent has reached the package ")
            agent.set_destination(self.agent_Packages_map[agent].get_package_dest())
            return True
            
        else:
            print("Agent is not assigned any package.")
            return False
        
    
    def deliver_package(self,agent_id):
        agent = self.get_agent(agent_id)
        if agent in self.agent_Packages_map:
            agent_loc = agent.get_current_coordinates()
            package_loc = agent.get_destination_coordinates()
            path = self.A_star_algo.find_path(agent_loc[0],agent_loc[1],agent_loc[2],package_loc[0],package_loc[1],package_loc[2])   

            if(path == None):
                print("Error - 02 : failed to get source to destination , try a different map")
                return None
            
            #path = path[1:]
            agent.update_new_path(path) 
            self.update_map(path)


            while(agent.get_current_coordinates() != package_loc):
                if(self.collision_Manager.detect_collision(agent, self.agents)):
                    agent.wait()
                    #implement the deadlock avoidance function here
                else:
                    agent.move()

                    coords = agent.get_current_coordinates()

                    print(f"Agent {agent.get_agent_id()} at {coords}")

                    if(self.Partitioned_map[coords[2]][coords[0]][coords[1]] != 5 and self.Partitioned_map[coords[2]][coords[0]][coords[1]] != -1):
                        self.Partitioned_map[coords[2]][coords[0]][coords[1]]  -= 2

                    MapGen_prototype.MapPartitioner.PathWriter(self.Partitioned_map,"map.txt")
                    scan = input("Press any key to continue")

            print("agent has delivered the package ")
            self.agent_Packages_map[agent].set_destination(None)
            self.agent_Packages_map[agent].update_package_loc(agent.get_current_coordinates())
            self.agent_Packages_map.pop(agent)
            return True
            
        else:
            print("Agent is not assigned any package.")
            return False

    #scheduling functions
    def package_scheduler(self, package_name, package_loc = None, package_dest = None):
        if package_dest == None:
            print("Destination not provided.")
            return False
        
        # sourcing the package
        if package_loc == None:
            package = self.PacMan.get_Package(package_name)
            if package == None:
                print("Package does not exist.")
                return False
        else:
            print("making new package")
            package = self.PacMan.make_new_package(package_name,package_loc)

        # assigning the package
        if package.get_package_dest() != None:
            print("Package already has a destination.")
            return False
        
        selected_agent = None
        min_distance = float("inf")
        for agent in self.agents:
            if agent.get_state() == "idle":
                package_location = package.get_package_loc()
                agent_location = agent.get_current_coordinates()
                distance_ = (package_location[0] - agent_location[0]) + (package_location[1] - agent_location[1]) + 2*(package_location[2] - agent_location[2])
                if distance_ < min_distance:
                    min_distance = distance_
                    selected_agent = agent

        if selected_agent == None:
            print("No idle agent available.")
            return False
        
        self.assign_package(package_name,selected_agent.get_agent_id(),package_dest)
        if self.pick_package(selected_agent.get_agent_id()) :
            print(f"Package picked up by agent: {selected_agent.get_agent_id()}.")
            if self.deliver_package(selected_agent.get_agent_id()):
                print(f"Package has been delivered {selected_agent.get_agent_id()}.")
        
                return True
        
        return False
    
    #map functions
    def update_map(self,path):
        for coordinates in path:
            print(f"Updating coordinates: {coordinates}")
            if self.Partitioned_map[coordinates[2]][coordinates[0]][coordinates[1]] == -1 or self.Partitioned_map[coordinates[2]][coordinates[0]][coordinates[1]] == 5:
                continue
            else:
                self.Partitioned_map[coordinates[2]][coordinates[0]][coordinates[1]] += 2
        print("Map updated.")
        MapGen_prototype.MapPartitioner.PathWriter(self.Partitioned_map,"map.txt")




        
    
