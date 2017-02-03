import copy
from geometry.point import Point
from geometry.segment import Segment


class Rect():
    def __init__(self, x, y, width = 0, height = 0):
        self.x = x
        self.y = y
        self._width = width
        self._height = height

    @property
    def area(self):
        return self.width * self.height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    def left(self, left = None):
        if left is not None:
            self.x = left
        return self.x

    def right(self, right = None):
        if right is not None:
            self.x = right - self.width
        return self.x + self.width

    def top(self, top = None):
        if top is not None:
            self.y = top
        return self.y

    def bottom(self, bottom = None):
        if bottom is not None:
            self.y = bottom - self.height
        return self.y + self.height

    def center(self, center = None):
        if center is not None:
            self.x = center.x - self.width / 2
            self.y = center.y - self.height / 2
        return Point(self.x + self.width / 2, self.y + self.height / 2)

    def containsPoint(self, point):
        return self.left() <= point.x <= self.right() \
            and self.top() <= point.y <= self.bottom()

    def containsRect(self, rect):
        return self.left() <= rect.left() and rect.right() <= self.right() \
            and self.top() <= rect.top() and rect.bottom() <= self.bottom()

    def getVertices(self):
        return [Point(self.left(), self.top()), Point(self.right(), self.top()), \
            Point(self.right(), self.bottom()), Point(self.left(), self.bottom())]

    def getSide(self, i):
        vertices = self.getVertices()
        return Segment(vertices[i], vertices[(i + 1) % 4])

    def getSector(self, point):
        return self.getSide(self.getSectorId(point))

    def getSectorId(self, point):
        offset = point - self.center()
        if offset.y <= 0 and abs(offset.x) <= abs(offset.y):
            return 0
        if offset.x >= 0 and abs(offset.x) >= abs(offset.y):
            return 1
        if offset.y >= 0 and abs(offset.x) <= abs(offset.y):
            return 2
        if offset.x <= 0 and abs(offset.x) >= abs(offset.y):
            return 3
