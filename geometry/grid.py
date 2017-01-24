class Grid:
    def __init__(self, x0 = 0, y0 = 0, line_distance = 30):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x0 + line_distance
        self.y1 = y0 + line_distance
        self.crossStatus = False
        #self.coords = (x % line_distance, y % line_distance)


