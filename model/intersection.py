#from control_signal import ControlSignals
import copy
import itertools
from geometry.rect import Rect

class Intersection():
    id_generator = itertools.count(1)
    def __init__(self, rect):
        self.id = "intersection_" + str(next(self.id_generator))
        self.roads = []
        self.inRoads = []
        self.rect = rect
        #self.controlSignals = ControlSignals(self)

    def copy(self):
        return copy.deepcopy(self)

    def update(self):
        for road in self.roads:
            road.update()
        for road in self.inRoads:
            road.update()
