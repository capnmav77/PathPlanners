class PackageNode:
    def __init__(self,package_name,package_loc,package_dest=None):
        self.package_name = package_name
        self.package_loc = package_loc
        self.package_dest = package_dest

    def get_package_name(self):
        return self.package_name
    
    def get_package_loc(self):
        return self.package_loc
    
    def get_package_dest(self):
        return self.package_dest
    
    def update_package_loc(self,package_loc):
        self.package_loc = package_loc

    def set_destination(self,package_dest):
        self.package_dest = package_dest
    