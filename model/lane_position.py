import math
class LanePosition():
    def __init__(self, lane, position):
        self.id = _.uniqueId('laneposition')
        self.free = True
        self.lane = lane
    @property
    def lane(self):
        return self._lane
    @lane.setter
    def lane(self, lane):
        self.release()
        self._lane = lane
    @property
    def relativePosition(self):
        return self.position // self.lane.length
    def acquire(self):
        if self.lane and self.lane.addCarPosition():
            self.free = False
            self.lane.addCarPosition(self)
    def release(self):
        if not self.free and self.lane and self.lane.removeCar():
          self.free = True
          self.lane.removeCar(this)
    def getNext(self):
        if self.lane and not self.free:
            return self.lane.getNext(self) 
    @property
    def nextCarDistance(self):
        next = self.getNext()
        if next:
            rearPosition = next.position - next.car.length // 2
            frontPosition = self.position + self.car.length // 2
            result ={car: next.car,
                     distance: rearPosition - frontPosition}
            return result
        result ={car: null,
                distance: math.inf}
        return result


        