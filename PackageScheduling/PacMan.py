from PackageScheduling import packageNode
from Agent_State import AgentNode


class PacMan : 
    def __init__(self):
        # a list to keep track of all the packages in the environment
        self.stationary_Packages = []
        self.Agents = []

        # a map to keep track of which agent is carrying which package
        self.agent_Packages_map = {} # key: agent, value: package
        
    def add_package(self,package):
        if self.stationary_Packages.count(package) == 0:
            self.stationary_Packages.append(package)
        else:
            print("Package already exists.")
    
    def add_agent(self,agent):
        if self.Agents.count(agent) == 0:
            self.Agents.append(agent)
        else:
            print("Agent already exists.")
    
    def create_new_agent(self,agent_id,agent_loc):
        for agent in self.Agents:
            if agent.get_agent_id() == agent_id:
                print("Agent already exists.")
                return
        agent = AgentNode.Agent(agent_id,agent_loc)
        self.add_agent(agent)

    def remove_package(self,package):
        if self.stationary_Packages.count(package) == 1:
            self.stationary_Packages.remove(package)
        else:
            print("Package does not exist.")

    def get_stationary_packages(self , package_name):
        for package in self.stationary_Packages:
            if package.get_package_name() == package_name:
                return package
        return None
    
    def make_new_package(self,package_name,package_loc,package_dest=None):
        package = packageNode.PackageNode(package_name,package_loc,package_dest)
        self.add_package(package)
    
    
    def assign_package(self,package_name,agent,destination_coordinates):

        package = self.get_stationary_packages(package_name)

        if package != None:
            self.stationary_Packages.remove(package)
            package.set_destination(destination_coordinates)
            agent.set_destination(package.get_package_loc())
            self.agent_Packages_map[agent] = package
            self.logging(f"Package {package.get_package_name()} assigned to agent {agent.get_agent_id()}.")

        else:
            print("Package does not exist.")

    def pick_Package(self,agent):
        if agent in self.agent_Packages_map:
            package = self.agent_Packages_map[agent]
            agent.set_destination(package.get_package_dest())
            self.logging(f"Agent {agent.get_agent_id()} is picking up package {package.get_package_name()} at {package.get_package_loc()}.")
        else:
            print("Agent is not carrying any package.")

    def unassign_package(self, agent):
        if agent not in self.agent_Packages_map:
            print("Agent is not carrying any package.")
            return
        
        package = self.agent_Packages_map[agent]
        package.update_package_loc(agent.get_current_coordinates())
        package.set_destination(None)

        self.agent_Packages_map.pop(agent)
        self.stationary_Packages.append(package)

        self.logging(f"Package {package.get_package_name()} unassigned from agent {agent.get_agent_id()}.")
        
    def get_nearest_agent(self,package_loc):
        min_distance = float("inf")
        nearest_agent = None
        for agent in self.Agents:
            distance = abs(agent.get_current_coordinates()[0] - package_loc[0]) + abs(agent.get_current_coordinates()[1] - package_loc[1]) + 10*abs(agent.get_current_coordinates()[2] - package_loc[2])
            if distance < min_distance:
                if agent in self.agent_Packages_map:
                    continue
                min_distance = distance
                nearest_agent = agent
        if nearest_agent == None:
            print("No agent available.")
        else: 
            self.logging(f"Nearest agent to package at {package_loc} is {nearest_agent.get_agent_id()}.")
        return nearest_agent

    def logging(self,message):
        with open ("log.txt", "a") as file: 
            file.write(message + "\n")
            
