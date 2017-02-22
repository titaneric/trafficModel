class Segment():
    def __init__(self, source, target):
        self.source = source
        self.target = target

    @property
    def vector(self):
        return self.target - self.source

    @property
    def length(self):
        return self.vector.length

    @property
    def direction(self):
        return self.vector.direction

    @property
    def center(self):
        return self.getPoint(0.5)

    def getPoint(self, scale):
        return self.source + (self.vector * scale)

    def subsegment(self, a, b):
        offset = self.vector
        start = self.source + (offset * a)
        end = self.source + (offset * b)
        return Segment(start, end)

    def split(self, n, reverse):
        order = reversed(list(range(n))) if reverse else list(range(n))
        splitResult = [self.subsegment(k / n, (k + 1) / n) for k in order]
        return splitResult
