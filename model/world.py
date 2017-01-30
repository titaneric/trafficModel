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
        for ID, info in map["intersections"].items():
            rect = Rect(info["position"]["x"], info["position"]["y"], info["position"]["width"], info["position"]["height"])
            #print(info["position"]["x"], info["position"]["y"], info["position"]["width"], info["position"]["height"])
            intersection = Intersection(rect)
            self.intersections[ID] = intersection

        for ID, info in map["roads"].items():
            road = Road(self.intersections[info["source"]], self.intersections[info["target"]])
            #print(info["source"], info["target"])
            self.roads[ID] = road


            


    '''
    @property 
    def instantSpeed(self):
        speeds = {key: v.speed() for key, v in self.cars.items()}
        if len(speeds) == 0:
            return 0 
        return (sum(speeds.values())) // len(speeds)
    '''



