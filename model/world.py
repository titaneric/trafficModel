import random
from car import Car
from intersection import Intersection
import sys
sys.path.append("../geometry")
from rect import Rect
class World():
    def __init__(self):
        self.set()
    def set(self, obj):
        self.intersections = obj.intersections
        self.roads = obj.roads
        self.cars = obj.cars
        self.carsNumber = 0
        self.time = 0
    @property 
    def instantSpeed(self):
        speeds = {key: v.speed() for key, v in self.cars.items()}
        if len(speeds) == 0:
            return 0 
        return (sum(speeds.values())) // len(speeds)
    



