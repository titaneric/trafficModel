import sys
import math
sys.path.append("../geometry")
from segment import Segment
class Lane():
    def __init__(self, sourceSegment, targetSegment, road):
        self.sourceSegment = sourceSegment
        self.targetSegment = targetSegment
        self.road = road
        self.leftAdjacent = None
        self.rightAdjacent = None
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
    def getTurnDirection(selfother):
        return self.road.getTurnDirection(other.road)

    def getDirection(self):
        return self.direction

    def getPoint(self, a):
        return self.middleLine.getPoint(a)

    def addCarPosition(self, carPosition):
        assert carPosition.id not in self.carsPositions.keys()
        self.carsPositions[carPosition.id] = carPosition

    def removeCar(self, carPosition):
        assert carPosition.id not in self.carsPositions.keys()
        del self.carsPositions[carPosition.id]

    def getNext(self, carPosition):
        next = None
        bestDistance = math.inf
        for id, other in self.carsPositions.items():
            distance = other.position - carPosition.position
            if not other.free and 0 < distance < bestDistance:
                bestDistance = distance
                next = o
        
        