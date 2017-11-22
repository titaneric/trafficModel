import copy

from geometry.point import Point
from geometry.segment import Segment


class Rect():
    def __init__(self, x: Point, y: Point, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

    def left(self, left=None) -> Point:
        if left is not None:
            self.x = left
        return self.x

    def right(self, right=None) -> Point:
        if right is not None:
            self.x = right - self.width
        return self.x + self.width

    def top(self, top=None) -> Point:
        if top is not None:
            self.y = top
        return self.y

    def bottom(self, bottom=None) -> Point:
        if bottom is not None:
            self.y = bottom - self.height
        return self.y + self.height

    def center(self, center=None) -> Point:
        if center is not None:
            self.x = center.x - self.width / 2
            self.y = center.y - self.height / 2
        return Point(self.x + self.width / 2, self.y + self.height / 2)

    def containsPoint(self, point: Point) -> bool:
        return self.left() <= point.x <= self.right() \
            and self.top() <= point.y <= self.bottom()

    def containsRect(self, rect: "Rect") -> bool:
        return self.left() <= rect.left() and rect.right() <= self.right() \
            and self.top() <= rect.top() and rect.bottom() <= self.bottom()

    def getVertices(self) -> list:
        return [Point(self.left(), self.top()), Point(self.right(), self.top()),
                Point(self.right(), self.bottom()), Point(self.left(), self.bottom())]

    def getSide(self, i) -> Segment:
        vertices = self.getVertices()
        return Segment(vertices[i], vertices[(i + 1) % 4])

    def getSector(self, point: Point) -> Segment:
        return self.getSide(self.getSectorId(point))

    def getSectorId(self, point: Point) -> int:
        offset = point - self.center()
        if offset.y <= 0 and abs(offset.x) <= abs(offset.y):
            return 0
        if offset.x >= 0 and abs(offset.x) >= abs(offset.y):
            return 1
        if offset.y >= 0 and abs(offset.x) <= abs(offset.y):
            return 2
        if offset.x <= 0 and abs(offset.x) >= abs(offset.y):
            return 3
