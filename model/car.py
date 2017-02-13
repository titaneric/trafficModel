from model.trajectory import Trajectory
import random
import itertools
import matplotlib.colors as colors


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
        self.maxSpeed = 10
        self.maxAcceleration = 5
        self.maxDeceleration = 3
        self.slowProb = 0.3
        self.trajectory = Trajectory(self, lane, position)
        self.alive = True
        self.preferedLane = None
        self.nextLane = None
        self.prePosition = None

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
        distanceToNextCar = max(nextCarDistance["distance"], 0)
        distanceToStopLine = self.trajectory.distanceToStopLine
        if distanceToStopLine < 30:
            return -1
        if random.random() < self.slowProb:
            return -1
        if self.speed + 1 <= self.maxSpeed and distanceToNextCar > (self.speed + 1):
            return 1
        elif distanceToNextCar <= self.speed:
            return self.speed - distanceToNextCar - 1
        else:
            return 0

    '''
    def getDecelaration(self):
        nextCarDistance = self.trajectory.nextCarDistance
        distanceToNextCar = max(nextCarDistance["distance"], 0)
        distanceToStopLine = self.trajectory.distanceToStopLine
        if distanceToStopLine < 30:
            return -1
        if random.random() < self.slowProb:
            return -1
        elif distanceToNextCar <= self.speed:
            return self.speed - (distanceToNextCar - 1)
        else:
            return 0
    '''

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
        '''
        self.prePosition = self.coords

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



