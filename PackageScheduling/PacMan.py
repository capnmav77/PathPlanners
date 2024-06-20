from PackageScheduling import packageNode
from Agent_State import AgentNode


class PacMan : 
    def __init__(self):
        # a list to keep track of all the packages in the environment
        self.Packages = []

    def make_new_package(self,package_name,package_loc,package_dest=None):
        package = packageNode.PackageNode(package_name,package_loc,package_dest)
        self.add_package(package)
        return package

    def remove_Package(self,package):
        if self.Packages.count(package) == 1:
            self.Packages.remove(package)
            del package
        else:
            print("Package does not exist.")

    def get_Package(self , package_name):
        for package in self.Packages:
            if package.get_package_name() == package_name:
                return package
        return None

    def logging(self,message):
        with open ("log.txt", "a") as file: 
            file.write(message + "\n")
            

