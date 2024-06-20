from Agent_State import AgentNode
from PackageScheduling import PacMan
from PathPlanningLibrary import A_Star
from MapGenerator import MapGen_prototype


class CentralCoordinator:
    def __init__(self):
        self.agents = []
        self.PacMan = PacMan.PacMan()
        self.agent_Packages_map = {}
        self.Partitioned_map = MapGen_prototype.MapPartitioner.read_map_from_file("../map.txt")
        self.A_star_algo = A_Star.A_Star(partitioned_map=self.Partitioned_map,diagonal_traversal=False)
        

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
            agent.set_destination(self, package.get_package_loc())
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
            path = self.A_star_algo.find_path(self,agent_loc[0],agent_loc[1],agent_loc[2],package_loc[0],package_loc[1],package_loc[2])   
            agent.update_new_path(path) 
            while(agent.move() != package_loc):
                #implement the deadlock avoidance function here
                pass
            print("agent has reached the package ")
            agent.set_destination(self.agent_Packages_map[agent].get_package_dest())
            
        else:
            print("Agent is not assigned any package.")
        
    
    def deliver_package(self,agent_id):
        agent = self.get_agent(agent_id)
        if agent in self.agent_Packages_map:
            agent_loc = agent.get_current_coordinates()
            package_loc = agent.get_destination_coordinates()
            path = self.A_star_algo.find_path(self,agent_loc[0],agent_loc[1],agent_loc[2],package_loc[0],package_loc[1],package_loc[2])   
            agent.update_new_path(path) 
            while(agent.move() != package_loc):
                #implement the deadlock avoidance function here
                pass
            print("agent has delivered the package ")
            self.agent_Packages_map[agent].set_destination(None)
            self.agent_Packages_map[agent].update_package_loc(agent.get_current_coordinates())
            self.agent_Packages_map.pop(agent)
            
        else:
            print("Agent is not assigned any package.")

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
            package = self.PacMan.make_new_package(package_name,package_loc)

        # assigning the package
        if package.get_package_dest() != None:
            print("Package already has a destination.")
            return False
        
        selected_agent = None
        min_distance = float("inf")
        for agent in self.agents:
            if agent.get_state() == "idle":
                distance_coords = package.get_package_loc() - agent.get_current_coordinates()
                distance_ = abs(distance_coords[0]) + abs(distance_coords[1]) + 3*abs(distance_coords[2])
                if distance_ < min_distance:
                    min_distance = distance_
                    selected_agent = agent

        if selected_agent == None:
            print("No idle agent available.")
            return False
        
        self.assign_package(package_name,selected_agent.get_agent_id(),package_dest)
        print(f"Package assigned to agent: {selected_agent.get_agent_id()}.")
        return True

        
    