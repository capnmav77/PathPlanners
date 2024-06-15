class Node:
    def __init__(self, x, y, z, parent=None, cost=0):
        self.x = x
        self.y = y
        self.z = z
        self.parent = parent
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost