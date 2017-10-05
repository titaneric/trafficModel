import math


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    @property
    def direction(self):
        return math.atan2(self.y, self.x)

    @property
    def normalized(self):
        return Point(self.x / self.length, self.y / self.length)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        return Point(self.x * other, self.y * other)

    def __div__(self, other: float):
        return Point(self.x / other, self.y / other)

