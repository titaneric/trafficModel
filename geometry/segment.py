from geometry.point import Point


class Segment():
    def __init__(self, source: Point, target: Point):
        self.source = source
        self.target = target

    @property
    def vector(self) -> Point:
        return self.target - self.source

    @property
    def length(self):
        return self.vector.length

    @property
    def direction(self):
        return self.vector.direction

    @property
    def center(self) -> Point:
        return self.getPoint(0.5)

    def getPoint(self, scale) -> Point:
        return self.source + (self.vector * scale)

    def getRelativePoint(self, point: Point):
        diff = point - self.source
        return diff.x / self.vector.x if self.vector.x != 0 else 0

    def subsegment(self, a, b):
        offset = self.vector
        start = self.source + (offset * a)
        end = self.source + (offset * b)
        return Segment(start, end)

    def split(self, n, reverse=False):
        order = reversed(list(range(n))) if reverse else list(range(n))
        splitResult = [self.subsegment(k / n, (k + 1) / n) for k in order]
        return splitResult
