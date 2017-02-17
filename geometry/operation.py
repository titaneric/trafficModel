import tkinter as tk
import numpy as np
from model.world import World
from model.intersection import Intersection
from model.road import Road
from model.car import Car
from geometry.rect import Rect
from geometry.point import Point


class Operation(tk.Frame):
    def __init__(self, root, canvas_height, canvas_width, distance, world):
        tk.Frame.__init__(self, root)
        self.root = root
        self.canvas = tk.Canvas(self, width=300, height=300, background="bisque")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0, 0, 1000, 1000))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # This is what enables using the mouse to drag:

        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.canvas.bind("<ButtonRelease>", self.ready2CreateRoad)
        # linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        # windows scroll
        self.canvas.bind("<MouseWheel>", self.zoomer)
        self.canvas.bind("<Double-Button-1>", self.buildIntersection)
        self.buildable = False
        self.movePath = []
        self._running = False
        self.scale = 1
        self.debug = False
        self.world = world
        self.distance = distance
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.drawGrid()
        self.drawWorld()

    def scroll_start(self, event):
        itemID = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        # the empty grid
        if self.canvas.itemcget(itemID, "fill") == "bisque":
            self.canvas.scan_mark(event.x, event.y)
            self.canvas.focus_set()
        # existed intersection
        elif self.canvas.itemcget(itemID, "fill") == "#808080":
            self.buildable = True

    def scroll_move(self, event):
        if self.buildable is False:
            self.canvas.scan_dragto(event.x, event.y, gain=1)
            self.update_member()
        else:
            self.movePath.append((self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)))

    def ready2CreateRoad(self, event):
        #itemID  = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        if self.buildable is False:
            return
        else:
            self.buildIntersection(event)
            self.buildRoad(event)

    #windows zoom
    def zoomer(self, event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self.update_member()

    #linux zoom
    def zoomerP(self, event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self.scale *= 1.1
        self.update_member()

    def zoomerM(self, event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self.scale *= 0.9
        self.update_member()

    def drawPolyLine(self, pointList: list):
        convertList = [(point.x, point.y) for point in pointList]
        self.canvas.create_polygon(convertList, fill="#808080", outline="#FFFFFF")

    def rotate(self, angle, coords, center):
        for point in coords:
            point.x -= center.x
            point.y -= center.y
            R = np.matrix([[np.cos(-angle), -np.sin(-angle)], [np.sin(-angle), np.cos(-angle)]])
            P = np.matrix([point.x, point.y])
            transform = np.dot(P, R)
            point.x = transform[0, 0] + center.x
            point.y = transform[0, 1] + center.y

        newCoords = [point for point in coords]
        return newCoords

    def update_member(self):
        for intersection in self.world.intersections.values():
            copyIntersection = intersection
            ID = self.canvas.find_withtag(copyIntersection.id)
            coords = self.canvas.coords(ID)
            copyIntersection.rect.x = coords[0]
            copyIntersection.rect.y = coords[1]
            copyIntersection.rect.width = coords[2] - coords[0]
            copyIntersection.rect.height = coords[3] - coords[1]
            del(self.world.intersections[copyIntersection.id])
            self.world.intersections[copyIntersection.id] = copyIntersection

        for road in self.world.roads.values():
            road.update()

    def buildIntersection(self, event):
        itemID = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        if self.canvas.itemcget(itemID, "fill") == "bisque":
            coords = self.canvas.coords(itemID)
            rect = Rect(coords[0], coords[1], self.distance * self.scale, self.distance * self.scale)
            intersection = Intersection(rect)
            self.drawIntersection(intersection)
            self.world.addIntersection(intersection)
        else:
            return

    def drawIntersection(self, intersection):
        self.canvas.create_rectangle(intersection.rect.x, intersection.rect.y, intersection.rect.x + intersection.rect.width, 
            intersection.rect.y + intersection.rect.height, fill = "#808080", outline = "#FFFFFF", tag = intersection.id)

    def drawGrid(self):
        for y in range(0, self.canvas_height, self.distance):
            for x in range(0, self.canvas_width, self.distance):
                self.canvas.create_rectangle(x, y, x + self.distance, y + self.distance, fill = "bisque", outline = "#FFFFFF")

    def buildRoad(self, event):
        itemID = self.canvas.find_closest(self.movePath[0][0], self.movePath[0][1])
        sourceID = self.canvas.gettags(itemID)[0]
        assert sourceID in self.world.intersections.keys(), "SourceID Error where ID is {sourceID}".format(**locals())
        itemID = self.canvas.find_closest(self.movePath[-1][0], self.movePath[-1][1])
        targetID = self.canvas.gettags(itemID)[0]
        assert targetID in self.world.intersections.keys(), "TargetID Error where ID is {sourceID}".format(**locals())
        road = Road(self.world.intersections[sourceID], self.world.intersections[targetID])
        self.world.addRoad(road)
        self.drawRoad(road)
        road = Road(self.world.intersections[targetID], self.world.intersections[sourceID])
        self.world.addRoad(road)
        self.drawRoad(road)
        self.buildable = False
        self.movePath.clear()

    def drawRoad(self, road):
        sourceSide = road.sourceSide
        targetSide = road.targetSide
        leftLine = road.leftmostLane.leftBorder
        self.canvas.create_line(leftLine.source.x, leftLine.source.y, leftLine.target.x, leftLine.target.y, fill = "yellow", dash = (10, 10), width = 3)
        rightLine = road.rightmostLane.rightBorder
        self.canvas.create_line(rightLine.source.x, rightLine.source.y, rightLine.target.x, rightLine.target.y, fill = "#FFFFFF")
        self.drawPolyLine([sourceSide.source, sourceSide.target, targetSide.source, targetSide.target])

    def drawWorld(self):
        for intersection in self.world.intersections.values():
            self.drawIntersection(intersection)

        for road in self.world.roads.values():
            self.drawRoad(road)

    def drawCar(self, car):
        angle = car.direction
        center = car.coords
        # prePosition = car.prePosition
        # print("{0}: ({1}, {2}), {3}".format(car.id, center.x, center.y, car.speed * 3.6 * 3))
        rect = Rect(0, 0, car.length * self.scale, car.width * self.scale)
        rect.center(Point(0, 0))
        coords = [Point(center.x + rect.left(), center.y + rect.top()),
            Point(center.x + rect.left(), center.y + rect.bottom()),
            Point(center.x + rect.right(), center.y + rect.bottom()),
            Point(center.x + rect.right(), center.y + rect.top())]
        newCoords = self.rotate(angle, coords, center)
        splitCoords = [(point.x, point.y) for point in newCoords]
        otherCoords = []
        for point in newCoords:
            otherCoords.append(point.x)
            otherCoords.append(point.y)
        # self.canvas.create_line(prePosition.x, prePosition.y, center.x, center.y, fill="red")
        if not self.canvas.find_withtag(car.id):
            self.canvas.create_polygon(splitCoords, fill=car.color, tag=car.id)
        else:
            ID = self.canvas.find_withtag(car.id)
            if car.alive:
                self.canvas.coords(ID, *otherCoords)
            else:
                print("delete")
                self.world.removeCar(car)
                self.canvas.delete(ID)

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, running):
        self._running = running

    def runModel(self):
        self.running = True
        self.display()

    def display(self):
        # self.update_member()
        for car in list(self.world.cars.values()):
            self.drawCar(car)
        self.world.onTick(0.001)

        if self.running is True:
            self.animationID = self.root.after(1, self.display)

    def stop(self):
        self.running = False

    def refresh(self):
        if self.animationID is not None:
            self.root.after_cancel(self.animationID)
            self.animationID = None
            for car in list(self.world.cars.values()):
                self.world.removeCar(car)
                ID = self.canvas.find_withtag(car.id)
                self.canvas.delete(ID)
            self.runModel()



