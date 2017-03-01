import math
from geometry.segment import Segment


class Lane():
    def __init__(self, sourceSegment, targetSegment, road):
        self.sourceSegment = sourceSegment
        self.targetSegment = targetSegment
        self.road = road
        self.id = road.id + '_' + 'lane'
        self.leftmostAdjacent = None
        self.rightmostAdjacent = None
        self.carsPositions = {}
        self.update()

    @property
    def sourceSideId(self):
        return self.road.sourceSideId

    @property
    def targetSideId(self):
        return self.road.targetSideId

    @property
    def isRightmost(self):
        return self is self.rightmostAdjacent

    @property
    def isLeftmost(self):
        return self is self.leftmostAdjacent

    @property
    def leftBorder(self):
        return Segment(self.sourceSegment.source, self.targetSegment.target)

    @property
    def rightBorder(self):
        return Segment(self.sourceSegment.target, self.targetSegment.source)

    def update(self):
        self.middleLine = Segment(self.sourceSegment.center, self.targetSegment.center)
        self.length = self.middleLine.length
        self.direction = self.middleLine.direction

    def getTurnDirection(self, other):
        return self.road.getTurnDirection(other.road)

    def getDirection(self, pos=None):
        return self.direction

    def getPoint(self, a):
        return self.middleLine.getPoint(a)

    def addCarPosition(self, carPosition):
        assert carPosition.id not in self.carsPositions.keys()
        self.carsPositions[carPosition.id] = carPosition

    def removeCar(self, carPosition):
        assert carPosition.id in self.carsPositions.keys()
        del self.carsPositions[carPosition.id]

    def getNext(self, carPosition):
        next = None
        bestDistance = float("inf")
        for other in self.carsPositions.values():
            if other is not carPosition:
                distance = other.position - carPosition.position
                if not other.free and 0 < distance < bestDistance:
                    bestDistance = distance
                    next = other
        return next