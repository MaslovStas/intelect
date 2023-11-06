class Point:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

d = {}
p1 = Point(1, 2, 3)
p2 = Point(1, 2, 3)
print(p1 < p2)