import random
import json
from model.car import Car
from model.road import Road
from model.intersection import Intersection
from geometry.rect import Rect

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

        self.carsNumber = 1


    def refreshCar(self, car):
        if len(self.cars) < self.carsNumber:
            self.addRandomCar()
        if len(self.cars) > self.carsNumber:
            self.removeRandomCar()
    
    def addRandomCar(self):
         road = random.choice(self.roads.values())
         





