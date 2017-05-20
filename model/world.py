import random
import json
import settings
from model.car import Car
from model.road import Road
from model.intersection import Intersection
from geometry.rect import Rect
from geometry.curve import Curve


class World():
    def __init__(self, exp=None):
        self.set()
        self.exp = None
        if exp is not None:
            self.exp = True

    def set(self):
        self.intersections = {}
        self.roads = {}
        self.cars = {}
        self.carsNumber = 0
        self.time = 0
        self.trafficFlow = 0
        self.graphList = {}

    def load(self):
        with open('data/map2.json') as data_file:
            map = json.load(data_file)
        self.carsNumber = map["carsNumber"]
        for info in map["intersections"].values():
            rect = Rect(info["position"]["x"], info["position"]["y"], info["position"]["width"], info["position"]["height"])
            intersection = Intersection(rect)
            intersection.id = info['id']
            self.addIntersection(intersection)

        for info in map["roads"].values():
            road = Road(self.intersections[info["source"]], self.intersections[info["target"]])
            road.id = info['id']
            self.addRoad(road)

    def systemInfo(self, scale=1):
        totalVelocity = 0.0
        # carsNumber = 0
        roadArea = 0.0
        carsArea = 0.0
        for road in self.roads.values():
            roadArea += road.length * settings.setDict["grid_size"] / 2 * scale
            for lane in road.lanes:
                # carsNumber += len(lane.carsPositions)
                for carsPosition in lane.carsPositions.values():
                    totalVelocity += carsPosition.car.speed
                    carsArea += carsPosition.car.length * scale * carsPosition.car.width
        avgDensity = carsArea / roadArea
        avgSpeed = totalVelocity / len(self.cars)
        return avgSpeed, avgDensity, self.trafficFlow

    def roadInfo(self, road, scale):
        carsNumber = 0
        totalVelocity = 0.0
        carsArea = 0.0
        for lane in road.lanes:
            carsNumber += len(lane.carsPositions)
            for carsPosition in lane.carsPositions.values():
                totalVelocity += carsPosition.car.speed
                carsArea += carsPosition.car.length * scale * carsPosition.car.width

        density = carsArea / (road.length * settings.setDict["grid_size"] / 2 * scale)
        avgSpeed = totalVelocity / carsNumber if carsNumber != 0 else 0.0
        return avgSpeed, density

    def refreshCar(self):
        if len(self.cars) < self.carsNumber:
            self.addRandomCar()
        if len(self.cars) > self.carsNumber:
            self.removeRandomCar()

    def addRandomCar(self):
        road = random.choice(list(self.roads.values()))
        if road is not None:
            lane = random.choice(road.lanes)
            if lane is not None:
                # self.addCar(Car(lane=lane, position=0))
                self.addCar(Car(graphList=self.graphList))

    def addCar(self, car):
        self.cars[car.id] = car

    def removeRandomCar(self):
        car = random.choice(list(self.cars.values()))
        if car is not None:
            car.alive = False
            self.trafficFlow -= 1

    def removeCar(self, car):
        self.cars.pop(car.id)
        self.trafficFlow += 1
        self.addRandomCar()

    def getIntersection(self, ID):
        return self.intersections[ID]

    def addIntersection(self, intersection):
        self.intersections[intersection.id] = intersection
        self.graphList[intersection.id] = dict()

    def addRoad(self, road):
        self.roads[road.id] = road
        self.graphList[road.source.id][road.target.id] = road
        road.source.roads.append(road)
        road.target.inRoads.append(road)
        road.update()

    def getRoad(self, ID):
        return self.roads[ID]

    def syncLane(self):
        for car in self.cars.values():
            for road in self.roads.values():
                for lane in road.lanes:
                    if car.trajectory.current.lane.id == lane.id:
                        relativePos = car.trajectory.current.relativePosition
                        car.trajectory.current.lane.sourceSegment = lane.sourceSegment
                        car.trajectory.current.lane.targetSegment = lane.targetSegment
                        car.trajectory.current.lane.update()
                        car.trajectory.current.position = car.trajectory.current.lane.length * relativePos

                    if car.trajectory.isChangingLanes and car.trajectory.next.lane is not None and car.trajectory.next.lane.id == lane.id:
                        car.trajectory.next.lane.sourceSegment = lane.sourceSegment
                        car.trajectory.next.lane.targetSegment = lane.targetSegment
                        car.trajectory.next.lane.update()

    def syncCurve(self):
        for car in self.cars.values():
            if car.trajectory.timeToMakeTurn() and car.trajectory.canEnterIntersection() \
                    and car.trajectory.isValidTurn() and car.trajectory.temp.lane is not None:
                relativePos = car.trajectory.temp.relativePosition
                previousA = car.trajectory.temp.lane.A
                previousB = car.trajectory.temp.lane.B
                relativeA = car.trajectory.current.lane.getRelativePosition(previousA)
                relativeB = car.trajectory.next.lane.getRelativePosition(previousB)
                car.trajectory.current.position = relativeA * car.trajectory.current.lane.length
                car.trajectory.next.position = relativeB * car.trajectory.next.lane.length
                car.trajectory.temp.lane = car.trajectory.getCurve()
                car.trajectory.temp.position = car.trajectory.temp.lane.length * relativePos

    def generateMap(self, maxX=10, maxY=10, minX=0, minY=0):
        self.set()
        intersectionNumber = 20
        myMap = dict()
        self.carsNumber = 30
        gridSize = settings.setDict["grid_size"]
        step = 5 * gridSize
        while intersectionNumber > 0:
            x = random.randint(minX, maxX)
            y = random.randint(minY, maxY)
            if not myMap.get((x, y)):
                rect = Rect(step * x, step * y, gridSize, gridSize)
                intersection = Intersection(rect)
                self.addIntersection(intersection)
                myMap[(x, y)] = intersection
                intersectionNumber -= 1

        for x in range(minX, maxX + 1, 1):
            previous = None
            for y in range(minY, maxY + 1, 1):
                intersection = myMap.get((x, y))
                if intersection:
                    if random.random() < 0.9 and previous:
                        self.addRoad(Road(intersection, previous))
                        self.addRoad(Road(previous, intersection))
                    previous = intersection

        for y in range(minY, maxY + 1, 1):
            previous = None
            for x in range(minX, maxX + 1, 1):
                intersection = myMap.get((x, y))
                if intersection:
                    if random.random() < 0.9 and previous:
                        self.addRoad(Road(intersection, previous))
                        self.addRoad(Road(previous, intersection))
                    previous = intersection

    def onTick(self, delta):
        self.time += delta
        self.trafficFlow = 0

        self.refreshCar()

        if self.exp is None:
            self.syncLane()
            self.syncCurve()
        for car in list(self.cars.values()):
            car.move(delta)
            if self.exp is not None and not car.alive:
                self.removeCar(car)








