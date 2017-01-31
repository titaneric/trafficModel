import random
import json
#from car import Car
#from intersection import Intersection
from model.road import Road
from model.intersection import Intersection
from geometry.rect import Rect
#import sys
#sys.path.append("../geometry")
#from rect import Rect
class World():
    def __init__(self):
        self.set()
    def set(self):
        self.intersections = {}
        self.roads = {}
        self.cars = {}
        self.carsNumber = 0
        self.time = 0

    def load(self):
        with open('map.json') as data_file:    
            map = json.load(data_file)
        
        self.carsNumber = map["carsNumber"]
        for info in map["intersections"].values():
            rect = Rect(info["position"]["x"], info["position"]["y"], info["position"]["width"], info["position"]["height"])
            intersection = Intersection(rect)
            self.intersections[intersection.id] = intersection

        for info in map["roads"].values():
            road = Road(self.intersections[info["source"]], self.intersections[info["target"]])
            self.roads[road.id] = road


            


    '''
    @property 
    def instantSpeed(self):
        speeds = {key: v.speed() for key, v in self.cars.items()}
        if len(speeds) == 0:
            return 0 
        return (sum(speeds.values())) // len(speeds)
    '''



