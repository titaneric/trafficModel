from lane import Lane
import copy
class Road():
    def __init__(self, source, target):
        self.id = uniqueId ('road')
        self.source = source
        self.target = target
        self.lanes = []
        self.lanesNumber = None
        self.update()
    def copy(self):
        return copy.deepcopy(self)
    @property
    def length(self):
        return self.targetSide.target.subtract(self.sourceSide.source).length

    @property
    def leftmostLane(self):
        return self.lanes[self.lanesNumber - 1]

    @property
    def rightmostLane(self):
        return self.lanes[0]

    def getTurnDirection(self, other):
        assert self.target is other.source
        side1 = self.targetSideId
        side2 = other.sourceSideId
        # 0 - left, 1 - forward, 2 - right
        turnNumber = (side2 - side1 - 1 + 8) % 4

    def update(self):
    #throw Error 'incomplete road' unless @source and @target
        self.sourceSideId = self.source.rect.getSectorId(self.target.rect.center())
        self.sourceSide = self.source.rect.getSide(self.sourceSideId).subsegment(0.5, 1.0)
        self.targetSideId = self.target.rect.getSectorId(self.source.rect.center())
        self.targetSide = self.target.rect.getSide(self.targetSideId).subsegment(0, 0.5)
        self.lanesNumber = min(self.sourceSide.length, self.targetSide.length) or 0
        self.lanesNumber = max(2, self.lanesNumber // settings.gridSize) or 0
        sourceSplits = self.sourceSide.split(self.lanesNumber, True)
        targetSplits = self.targetSide.split(self.lanesNumber)
        if not self.lanes or self.lanes.length < self.lanesNumber:
          self.lanes = []
          for i in range(0, self.lanesNumber - 1):
            self.lanes[i] = Lane(sourceSplits[i], targetSplits[i], self)
        for i in range(0, self.lanesNumber - 1): 
          self.lanes[i].sourceSegment = sourceSplits[i]
          self.lanes[i].targetSegment = targetSplits[i]
          self.lanes[i].leftAdjacent = self.lanes[i + 1]
          self.lanes[i].rightAdjacent = self.lanes[i - 1]
          self.lanes[i].leftmostAdjacent = self.lanes[self.lanesNumber - 1]
          self.lanes[i].rightmostAdjacent = self.lanes[0]
          self.lanes[i].update()
        