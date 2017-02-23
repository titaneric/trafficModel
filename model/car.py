from model.trajectory import Trajectory
import random
import itertools
import matplotlib.colors as colors
import math


class Car():
    id_generator = itertools.count(1)

    def __init__(self, lane, position):
        self.id = "car_" + str(next(self.id_generator))
        self.start = 0
        self.end = 0
        self.color = colors.rgb2hex((random.random(), random.random(), random.random()))
        self._speed = 0
        self.width = 4
        self.length = 10 + random.randint(0, 5)
        self.maxSpeed = 40
        self.maxAcceleration = 2
        self.maxDeceleration = 3
        self.slowProb = 0.3
        self.trajectory = Trajectory(self, lane, position)
        self.alive = True
        self.preferedLane = None
        self.nextLane = None

        self.timeHeadway = 1.5
        self.s0 = 2

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        if speed < 0:
            speed = 0
        if speed > self.maxSpeed:
            speed = self.maxSpeed
        self._speed = speed

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
        distanceToNextCar = max(nextCarDistance["distance"], 1)
        
        distanceToStopLine = self.trajectory.distanceToStopLine
        if distanceToStopLine < 30:
            return -1
        else:
            a = self.maxAcceleration
            b = self.maxDeceleration
            deltaSpeed = (self.speed - nextCarDistance["car"].speed) if nextCarDistance["car"] is not None else 0
            freeRoadCoeff = (self.speed / self.maxSpeed) ** 4
            distanceGap = self.s0
            timeGap = self.speed * self.timeHeadway
            breakGap = self.speed * deltaSpeed / (2 * math.sqrt(a * b))
            safeDistance = distanceGap + timeGap + breakGap
            busyRoadCoeff = (safeDistance / distanceToNextCar) ** 2
            safeIntersectionDistance = 1 + timeGap + self.speed ** 2 / (2 * b)
            intersectionCoeff = (safeIntersectionDistance / self.trajectory.distanceToStopLine) ** 2
            coeff = 1 - freeRoadCoeff - busyRoadCoeff - intersectionCoeff
            return self.maxAcceleration * coeff

    def move(self, delta):
        acce = self.getAcceleration()
        self.speed += acce * delta
        '''
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

        self.prePosition = self.coords
        '''
        step = self.speed * delta + 0.5 * acce * delta ** 2
        if self.trajectory.timeToMakeTurn(step):
            if not self.nextLane:
                self.alive = False
        self.trajectory.moveForward(step)

    def pickNextRoad(self):
        intersection = self.trajectory.nextIntersection
        currentLane = self.trajectory.current.lane
        possibleRoads = [road for road in intersection.roads if road.target is not currentLane.road.source]
        if not possibleRoads:
            return None
        nextRoad = random.choice(possibleRoads)
        return nextRoad

    def pickNextLane(self):
        self.nextLane = None
        nextRoad = self.pickNextRoad()
        if not nextRoad:
            self.nextLane = None
            return None
        turnNumber = self.trajectory.current.lane.road.getTurnDirection(nextRoad)
        if turnNumber == 0:
            laneNumber = -1
        elif turnNumber == 1:
            laneNumber = random.randint(0, nextRoad.lanesNumber - 1)
        elif turnNumber == 2:
            laneNumber = 0
        self.nextLane = nextRoad.lanes[laneNumber]
        assert self.nextLane is not None
        return self.nextLane

    def popNextLane(self):
        nextLane = self.nextLane
        self.nextLane = None
        self.preferedLane = None
        return nextLane



