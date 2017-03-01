import math
import itertools
from model.lane import Lane
class LanePosition():
    id_generator = itertools.count(1)
    def __init__(self, car, lane = None, position = None):
        self.car = car
        self.id = "laneposition_" + str(next(self.id_generator))
        self.free = True
        self.position = position
        self._lane = lane

    @property
    def lane(self):
        return self._lane

    @lane.setter
    def lane(self, lane):
        self.release()
        self._lane = lane

    @property
    def relativePosition(self):
        return self.position / self.lane.length

    def acquire(self):
        if type(self.lane) is Lane:
            self.free = False
            self.lane.addCarPosition(self)

    def release(self):
        if not self.free and type(self.lane) is Lane:
            self.free = True
            self.lane.removeCar(self)

    def getNext(self):
        if type(self.lane) is Lane and not self.free:
            return self.lane.getNext(self)

    @property
    def nextCarDistance(self):
        next = self.getNext()
        if next is not None:
            rearPosition = next.position - next.car.length / 2
            frontPosition = self.position + self.car.length / 2
            result = {"car": next.car,
                      "distance": rearPosition - frontPosition if rearPosition > frontPosition else next.position - self.position}
            return result
        result = {"car": None,
                  "distance": float("inf")}
        return result
