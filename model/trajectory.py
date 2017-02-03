from model.lane_position import LanePosition
import math
from geometry.curve import Curve


class Trajectory():
    def __init__(self, car, lane, position):
        self.car = car
        assert position is not None
        self.current = LanePosition(self.car, lane, position)
        self.current.acquire()
        self.next = LanePosition(self.car)
        self.temp = LanePosition(self.car)
        self.isChangingLanes = False

    @property
    def lane(self):
        return self.temp.lane or self.current.lane

    @property
    def absolutePosition(self):
        return self.temp.position if self.temp.lane is not None \
            else self.current.position

    @property
    def relativePosition(self):
        return self.absolutePosition / self.lane.length

    @property
    def direction(self):
        return self.lane.getDirection(self.relativePosition)

    @property
    def coords(self):
        return self.lane.getPoint(self.relativePosition)

    @property
    def nextCarDistance(self):
        a = self.current.nextCarDistance
        b = self.next.nextCarDistance
        return a if a.distance < b.distance else b

    @property
    def distanceToStopLine(self):
        if not self.canEnterIntersection():
            return self.getDistanceToIntersection()
        return float("inf")

    @property
    def nextIntersection(self):
        return self.current.lane.road.target

    @property
    def previousIntersection(self):
        return self.current.lane.road.source

    def isValidTurn(self):
        # TODO right turn is only allowed from the right lane
        nextLane = self.car.nextLane
        sourceLane = self.current.lane
        if nextLane is None:
            print('no road to enter')
        turnNumber = sourceLane.getTurnDirection(nextLane)
        if turnNumber is 3:
            print('no U-turns are allowed')
        if turnNumber is 0 and not sourceLane.isLeftmost:
            print('no left turns from this lane')
        if turnNumber is 2 and not sourceLane.isRightmost:
            print('no right turns from this lane')
        return True

    def canEnterIntersection(self):
        nextLane = self.car.nextLane
        sourceLane = self.current.lane
        if not nextLane:
            return True
        '''
        intersection = self.nextIntersection
        turnNumber = sourceLane.getTurnDirection(nextLane)
        sideId = sourceLane.road.targetSideId
        intersection.controlSignals.state[sideId][turnNumber]
        '''

    def getDistanceToIntersection(self):
        distance = self.current.lane.length - \
            self.car.length / 2 - self.current.position
        return max(distance, 0) if not self.isChangingLanes else float("inf")

    def timeToMakeTurn(self, plannedStep = 0):
        return (self.getDistanceToIntersection() <= plannedStep)

    def moveForward(self, distance):
        distance = max(distance, 0)
        self.current.position += distance
        self.next.position += distance
        self.temp.position += distance
        if self.timeToMakeTurn() and self.canEnterIntersection() and self.isValidTurn():
            self._startChangingLanes(self.car.popNextLane(), 0)
        tempRelativePosition = self.temp.position / self.temp.lane.length
        gap = 2 * self.car.length
        if self.isChangingLanes and (self.temp.position > gap) and not self.current.free:
            self.current.release()
        if self.isChangingLanes and self.next.free \
            and ((self.temp.position + gap) > self.temp.lane.length):
            self.next.acquire()
        if self.isChangingLanes and (tempRelativePosition >= 1):
            self._finishChangingLanes()
        if self.current.lane and not self.isChangingLanes and not self.car.nextLane:
            self.car.pickNextLane()

    def changeLane(self, nextLane):
        if self.isChangingLanes:
            print('already changing lane')
        if not nextLane:
            print('no next lane')
        if nextLane is self.lane:
            print('next lane == current lane')
        if self.lane.road is not nextLane.road:
            print('not neighboring lanes')
        nextPosition = self.current.position + 3 * self.car.length
        if not (nextPosition < self.lane.length):
            print('too late to change lane')
        self._startChangingLanes(nextLane, nextPosition)

    def _getAdjacentLaneChangeCurve(self):
        p1 = self.current.lane.getPoint(self.current.relativePosition)
        p2 = self.next.lane.getPoint(self.next.relativePosition)
        distance = (p2 - p1).length
        direction1 = self.current.lane.middleLine.vector.normalized * (distance * 0.3)
        control1 = p1 + direction1
        direction2 = self.next.lane.middleLine.vector.normalized * (distance * 0.3)
        control2 = p2 - direction2
        curve = Curve(p1, p2, control1, control2)
        return curve

    def _getCurve(self):
        self._getAdjacentLaneChangeCurve()

    def _startChangingLanes(nextLane, nextPosition):
        assert self.isChangingLanes, 'already changing lane'
        assert not nextLane, 'no next lane'
        self.isChangingLanes = True
        self.next.lane = nextLane
        self.next.position = nextPosition
        curve = self._getCurve()
        self.temp.lane = curve
        self.temp.position = 0  # @current.lane.length - @current.position
        self.next.position -= self.temp.lane.length

    def _finishChangingLanes(self):
        assert not self.isChangingLanes, 'no lane changing is going on'
        self.isChangingLanes = False
        # TODO swap current and next
        self.current.lane = self.next.lane
        self.current.position = self.next.position or 0
        self.current.acquire()
        self.next.lane = None
        self.next.position = None
        self.temp.lane = None
        self.temp.position = None
        self.current.lane

    def release(self):
        self.current.release()
        self.next.release()
        self.temp.release()
