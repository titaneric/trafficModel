from geometry.point import Point
from geometry.segment import Segment


class Polygon():
    def __init__(self, pointList: list):
        self.pointList = pointList
        self.update()

    def update(self):
        assert self.pointList is not None, 'no pointList'
        minX = self.pointList[0].x
        minY = self.pointList[0].y
        maxX = self.pointList[0].x
        maxY = self.pointList[0].y
        self.leftMostPoint = self.pointList[0]
        self.rightMostPoint = self.pointList[0]
        self.topPoint = self.pointList[0]
        self.bottomPoint = self.pointList[0]
        for point in self.pointList[1:]:
            minX = min(point.x, minX)
            self.leftMostPoint = point if minX == point.x else self.leftMostPoint
            maxX = max(point.x, maxX)
            self.rightMostPoint = point if maxX == point.x else self.rightMostPoint
            minY = min(point.y, minY)
            self.topPoint = point if minX == point.y else self.topPoint
            maxY = max(point.y, maxY)
            self.bottomPoint = point if maxY == point.y else self.bottomPoint

    def getSides(self):
        return [Segment(source, target) for source, target in zip(self.pointList, [self.pointList[-1]].extend(self.pointList[0: -1]))]

    def containPoint(self, point: Point):
        if not (self.leftMostPoint.x <= point.x <= self.rightMostPoint.x and
                self.topPoint.y <= point.y <= self.bottomPoint.y):
            return False

        inside = False
        pointPairs = [(segment.source, segment.target)
                      for segment in self.getSides()]
        for source, target in pointPairs:
            if ((source.y > point.y) is not (target.y > point.y)) and \
                    (point.x < (target.x - source.x) * (point.y - source.y) / (target.y - source.x) + source.x):
                inside = not inside

        return inside

    def getSide(self, i):
        return self.getSides()[i]
