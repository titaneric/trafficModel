import random
from trajectory import Trajectory
import itertools
class Car():
    id_generator = itertools.count(1)
    def __init__(self):
        self.id = "car_" + str(next(self.id_generator))
        self.start = 0
        self.end = 0 
        self.path = []
        #Inter = IntersectionTuple()
        #Inter = 0, 0
        #self.currentRoad = Inter
        #self.nextRoad = self.pickNextRoad()
        self.color = (300 + 240 * random.random()) % 360
        self._speed = 0
        self.width = 1.7
        self.length = 3 + 2 * random.random()
        self.maxSpeed = 30
        self.maxAcceleration = 1
        self.slowProb  = 0.3
        self.trajectory = Trajectory(lane, position)
        self.alive = True
    @property
    def speed(self):
        return self._speed
    @speed.setter 
    def speed(self, speed):
        if speed < 0:speed = 0 
        if speed > self.maxSpeed:speed = self.maxSpeed 
        self._speed = speed
    '''
    @property
    def coords(self):
        return self.trajectory.coords
    @property
    def direction(self):
        return self.trajectory.direction

    def release(self):
        self.trajectory.release()

    def getAcceleration(self):
        nextCarDistance = self.trajectory.nextCarDistance
        distanceToNextCar = max(nextCarDistance.distance, 0)
        if self.speed + 1 <= self.maxSpeed and distanceToNextCar > (self.speed + 1):
            return 1
        else:
            return 0

    def getDecelaration(self):
        nextCarDistance = self.trajectory.nextCarDistance
        distanceToNextCar = max(nextCarDistance.distance, 0)
        if random.random() < self.slowProb:
            return -1
        if distanceToNextCar <= self.speed:
            return (self.speed - (distanceToNextCar - 1))
    def move(self, delta):
        acce = self.getAcceleration()
        dece = self.getDecelaration()
        self.speed += (acce + dece) * delta
        if not self.trajectory.isChangingLanes and self.nextLane:
            currentLane = self.trajectory.current.lane
            turnNumber = currentLane.getTurnDirection(self.nextLane)
            if turnNumber == 0:
                preferedLane = currentLane.leftmostAdjacent
            elif turnNumber == 2:
                preferedLane = currentLane.rightmostAdjacent
            else:
                preferedLane = currentLane
            
            if preferedLane is not currentLane:
                self.trajectory.changeLane(preferedLane)
        step = self.speed * delta + 0.5 * (acce + dece) * delta ** 2
        if self.trajectory.timeToMakeTurn(step):
            if not self.nextLane:
                self.alive = False
        self.trajectory.moveForward(step)

    def pickNextRoad(self):
        intersection = self.trajectory.nextIntersection
        currentLane = self.trajectory.current.lane
        #nextRoad = 
        return nextRoad
    def pickNextLane(self):
        self.nextLane = None
        nextRoad = self.pickNextRoad()
        if not nextRoad:
            return None
        turnNumber = self.trajectory.current.lane.road.getTurnDirection(nextRoad)
        if turnNumber == 0:
            laneNumber =  nextRoad.lanesNumber - 1
        elif turnNumber == 1:
            laneNumber = random.randint(0, nextRoad.lanesNumber - 1)
        elif turnNumber == 2:
            laneNumber = 0
        self.nextLane = nextRoad.lanes[laneNumber]
        assert self.nextLane > 0
        return self.nextLane

    def popNextLane(self):
        nextLane = self.nextLane
        self.nextLane = None
        self.preferedLane = None
        return nextLane
    '''







    



