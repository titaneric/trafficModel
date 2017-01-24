from control_signal import ControlSignals
import sys
sys.path.append("../geometry")
from rect import Rect
import copy
class Intersection():
    def __init__(self, rect):
        self.id = _.uniqueId('intersection')
        self.roads = []
        self.inRoads = []
        self.controlSignals = ControlSignals()
    def copy(self):
        return copy.deepcopy(self)
    def update(self):
        for road in self.roads:road.update() 
        for road in self.inRoads:road.update() 

        
