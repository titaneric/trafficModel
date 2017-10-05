from geometry.segment import Segment


class Curve():
    def __init__(self, A, B, O, Q):
        self.A = A
        self.B = B
        self.O = O
        self.Q = Q
        self.AB = Segment(self.A, self.B)
        self.AO = Segment(self.A, self.O)
        self.OQ = Segment(self.O, self.Q)
        self.QB = Segment(self.Q, self.B)
        self._length = None

    @property
    def length(self):
        if self._length is None:
            pointsNumber = 10
            prevoiusPoint = None
            self._length = 0
            for i in range(pointsNumber):
                point = self.getPoint(i / pointsNumber)
                if prevoiusPoint is not None:
                    self._length += (point - prevoiusPoint).length

                prevoiusPoint = point
        return self._length

    def getPoint(self, a):
        p0 = self.AO.getPoint(a)
        p1 = self.OQ.getPoint(a)
        p2 = self.QB.getPoint(a)
        r0 = (Segment(p0, p1)).getPoint(a)
        r1 = (Segment(p1, p2)).getPoint(a)
        return (Segment(r0, r1)).getPoint(a)

    def getDirection(self, a):
        p0 = self.AO.getPoint(a)
        p1 = self.OQ.getPoint(a)
        p2 = self.QB.getPoint(a)
        r0 = (Segment(p0, p1)).getPoint(a)
        r1 = (Segment(p1, p2)).getPoint(a)
        return (Segment(r0, r1)).direction
