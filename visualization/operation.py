import tkinter as tk
import pandas as pd
from model.world import World
from model.intersection import Intersection
from model.road import Road
from model.car import Car
from geometry.rect import Rect
from geometry.point import Point
from visualization.visualizer import Visualizer
import settings
import csv


class Operation(tk.Frame):
    def __init__(self, root, toolDict, world):
        tk.Frame.__init__(self, root)
        self.root = root
        self.canvas = tk.Canvas(self, width=settings.setDict["canvas_width"], height=settings.setDict["canvas_height"], background="bisque")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0, 0, 3000, 3000))

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
        self.world = world
        self.playBtn = toolDict['playBtn']
        self.playPNG = toolDict['playPNG']
        self.pausePNG = toolDict['pausePNG']
        self.carText = toolDict['carText']
        self.roadText = toolDict['roadText']
        self.systemText = toolDict['systemText']
        self.debugBtn = toolDict['debugBtn']
        self.selectedRoad = None
        self.slider = toolDict['slider']
        self.slider.set(self.world.carsNumber)
        self.debug = False
        self.collect = False
        self.animationID = None
        self.distance = settings.setDict["grid_size"]
        self.canvas_height = settings.setDict["canvas_height"]
        self.canvas_width = settings.setDict["canvas_width"]
        self.visualizer = Visualizer(self.world, self.canvas, self.carText)

    def scroll_start(self, event):
        coords = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        itemID = self.canvas.find_closest(*coords)
        tag = self.canvas.gettags(itemID)
        # the empty grid
        if self.canvas.itemcget(itemID, "fill") == settings.setDict["color"]["background"]:
            self.canvas.scan_mark(event.x, event.y)
            self.canvas.focus_set()
        # existed intersection
        elif len(tag) > 0 and tag[0] in self.world.intersections.keys():
            self.buildable = True
        elif len(tag) > 0 and tag[0] in self.world.roads.keys():
            self.selectedRoad = self.world.roads[tag[0]]

        if self.running is True:
            searchRange = 10
            searchRange *= self.scale
            rectCoords = (self.canvas.canvasx(event.x) - searchRange, self.canvas.canvasy(event.y) - searchRange, 
            self.canvas.canvasx(event.x) + searchRange, self.canvas.canvasy(event.y) + searchRange)
            itemList = list(self.canvas.find_enclosed(*rectCoords))
            carID_list = [self.canvas.gettags(item)[0] for item in itemList
            if self.canvas.gettags(item) and self.canvas.gettags(item)[0] in self.world.cars.keys()]
            if carID_list:
                self.buildable = False
                self.showCarInfo(carID_list, Point(coords[0], coords[1]))

    def scroll_move(self, event):
        if self.buildable is False:
            self.canvas.scan_dragto(event.x, event.y, gain=1)
            self.update_member()
        else:
            self.movePath.append((self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)))

    def ready2CreateRoad(self, event):
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
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.update_member()

    #linux zoom
    def zoomerP(self, event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scale *= 1.1
        self.visualizer.scale = self.scale
        self.update_member()

    def zoomerM(self, event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scale *= 0.9
        self.visualizer.scale = self.scale
        self.update_member()

    def update_member(self):
        for intersection in self.world.intersections.values():
            ID = self.canvas.find_withtag(intersection.id)
            coords = self.canvas.coords(ID)
            intersection.rect.x = coords[0]
            intersection.rect.y = coords[1]
            intersection.rect.width = coords[2] - coords[0]
            intersection.rect.height = coords[3] - coords[1]

        for road in self.world.roads.values():
            road.update()


    def buildIntersection(self, event):
        itemID = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        if self.canvas.itemcget(itemID, "fill") == settings.setDict["color"]["background"]:
            coords = self.canvas.coords(itemID)
            rect = Rect(coords[0], coords[1], self.distance * self.scale, self.distance * self.scale)
            intersection = Intersection(rect)
            self.visualizer.drawIntersection(intersection)
            self.world.addIntersection(intersection)
        else:
            return

    def buildRoad(self, event):
        if len(self.movePath) > 1:
            itemID = self.canvas.find_closest(self.movePath[0][0], self.movePath[0][1])
            sourceID = self.canvas.gettags(itemID)[0]
            assert sourceID in self.world.intersections.keys(), "SourceID Error where ID is {sourceID}".format(**locals())
            itemID = self.canvas.find_closest(self.movePath[-1][0], self.movePath[-1][1])
            targetID = self.canvas.gettags(itemID)[0]
            assert targetID in self.world.intersections.keys(), "TargetID Error where ID is {sourceID}".format(**locals())
            road = Road(self.world.intersections[sourceID], self.world.intersections[targetID])
            self.world.addRoad(road)
            self.visualizer.drawRoad(road)
            road = Road(self.world.intersections[targetID], self.world.intersections[sourceID])
            self.world.addRoad(road)
            self.visualizer.drawRoad(road)
            self.buildable = False
            self.movePath.clear()

    def showCarInfo(self, tag_list, coords):
        distance = float("inf")
        for carID in tag_list:
            car = self.world.cars[carID]
            if (car.coords - coords).length < distance:
                distance = (car.coords - coords).length
                self.visualizer.selectedCar = car

    def showRoadInfo(self):
        if self.selectedRoad is not None:
            self.roadText.delete('1.0', tk.END)
            carsNumber = 0
            totalVelocity = 0.0
            carsArea = 0.0
            for lane in self.selectedRoad.lanes:
                carsNumber += len(lane.carsPositions)
                for carsPosition in lane.carsPositions.values():
                    totalVelocity += carsPosition.car.speed
                    carsArea += carsPosition.car.length * self.scale 

            density = carsArea / self.selectedRoad.length
            self.roadText.insert(tk.INSERT, ' Road ID: {0}, Avg Speed: {1:.2}\n Density: {2:.3} car length/meter'.format(self.selectedRoad.id
            , totalVelocity / carsNumber if carsNumber != 0 else 0.0, density))


    def showSystemInfo(self):
        self.systemText.delete('1.0', tk.END)
        totalVelocity = 0.0
        carsNumber = 0
        for road in self.world.roads.values():
            for lane in road.lanes:
                carsNumber += len(lane.carsPositions)
                for carsPosition in lane.carsPositions.values():
                    totalVelocity += carsPosition.car.speed

        if self.collect is True and self.world.time < 60:
            with open('data/data.csv', 'a', encoding='utf8') as f:
                fwriter = csv.writer(f, delimiter=',')
                fwriter.writerow([self.world.time, totalVelocity / carsNumber])
            f.close()
        elif self.collect is True and self.world.time > 60:
            print('Finish collecting')
            self.collect = False

        self.systemText.insert(tk.INSERT, '    System\nAvg Speed: {0:.2}'.format(totalVelocity / carsNumber if carsNumber != 0 else 0.0))

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, running):
        self._running = running

    def runModel(self):
        self.running = True
        self.playBtn.config(image=self.pausePNG, text = "Pause", command=lambda : self.stop())
        self.display()

    def display(self):
        for car in list(self.world.cars.values()):
            self.visualizer.drawCar(car)
        self.world.carsNumber = self.slider.get()
        self.showRoadInfo()
        self.showSystemInfo()
        self.world.onTick(0.001)
        if self.running is True:
            self.animationID = self.root.after(1, self.display)

    def stop(self):
        self.running = False
        self.playBtn.config(image=self.playPNG, text = "Action", command=lambda : self.runModel())

    def debugSwitch(self):
        if self.running is True and self.debug is False:
            self.debug = True
            self.visualizer.debug = True
            self.debugBtn.configure(bg=settings.setDict['color']['debugBtn_on'])
        elif self.running is True and self.debug is True:
            self.debug = False
            self.visualizer.debug = False
            self.debugBtn.configure(bg=settings.setDict['color']['debugBtn_off'])


    def refresh(self):
        if self.animationID is not None:
            self.carText.delete('1.0', tk.END)
            self.roadText.delete('1.0', tk.END)
            self.visualizer.clearPath()
            self.root.after_cancel(self.animationID)
            self.animationID = None
            for car in list(self.world.cars.values()):
                self.world.removeCar(car)
                ID = self.canvas.find_withtag(car.id)
                self.canvas.delete(ID)
            self.runModel()
        else:
            self.runModel()

    def collectData(self):
        self.collect = True



