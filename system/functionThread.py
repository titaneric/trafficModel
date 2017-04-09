import threading
import csv
import settings
import tkinter as tk
import pickle
import os
from model.car import Car


class SystemInfoThread(threading.Thread):

    def __init__(self, systemText, world, stateQueue):
        threading.Thread.__init__(self)
        self.world = world
        self.systemText = systemText
        self.stateQueue = stateQueue

    def run(self):
            while True:
                try:
                    d = pickle.loads(self.stateQueue.get())
                    state = d["state"]
                    if state is False:
                        break
                    scale = d["scale"]
                    self.systemText.delete('1.0', tk.END)
                    avgSpeed, avgDensity = self.world.systemInfo(scale)
                    self.systemText.insert(tk.INSERT, 'Avg Speed: {0:.3} km/hr'.format(avgSpeed * 3.6))
                finally:
                    self.stateQueue.task_done()


class RoadInfoThread(threading.Thread):

    def __init__(self, roadText, world, stateQueue):
        threading.Thread.__init__(self)
        self.roadText = roadText
        self.world = world
        self.stateQueue = stateQueue

    def run(self):
        while True:
            try:
                d = pickle.loads(self.stateQueue.get())
                state = d["state"]
                if state is False:
                    break
                self.selectedRoad = d["selectedRoad"]
                scale = d["scale"]
                if self.selectedRoad is not None:
                    # print(self.selectedRoad.id)
                    self.roadText.delete('1.0', tk.END)
                    avgSpeed, density = self.world.roadInfo(self.selectedRoad, scale)
                    self.roadText.insert(tk.INSERT, ' Road ID: {0}, Avg Speed: {1:.3} km/hr\n Density: {2:.3} car length/meter'.format(self.selectedRoad.id
                    , avgSpeed * 3.6, density))
            finally:
                self.stateQueue.task_done()


class CollectDataThread(threading.Thread):

    def __init__(self, world, stateQueue):
        threading.Thread.__init__(self)
        self.world = world
        self.stateQueue = stateQueue

    def run(self):
        print("Start collecting")
        dataFile = "data/data.csv"
        if os.path.isfile(dataFile):
            os.remove(dataFile)

        while True:
            try:
                d = pickle.loads(self.stateQueue.get())
                state = d["state"]
                if state is False:
                    break
                if self.world.time < settings.setDict["collecting_time"]:
                    scale = d["scale"]
                    avgSpeed, density = self.world.systemInfo(scale)
                    with open(dataFile, 'a', encoding='utf8') as f:
                        fwriter = csv.writer(f, delimiter=',')
                        fwriter.writerow([self.world.time, avgSpeed, self.world.trafficFlow / self.world.time, density])
                    f.close()
                else:
                    print('Finish collecting')
                    break
            finally:
                self.stateQueue.task_done()


class CarInfoThread(threading.Thread):

    def __init__(self, canvas, carText, stateQueue, world):
        threading.Thread.__init__(self)        
        self.canvas = canvas
        self.carText = carText
        self.world = world
        self.stateQueue = stateQueue
        self.preCar = None
        self.selectedCar = None

    def run(self):
        while True:
            d = pickle.loads(self.stateQueue.get())
            state = d["state"]
            debug = d["debug"]
            if self.selectedCar is not None:
                self.preCar = self.selectedCar 
            self.selectedCar = d["selectedCar"]
            if self.preCar is not None and self.selectedCar is not self.preCar:
                ID = self.canvas.find_withtag(self.preCar.id)
                self.canvas.itemconfig(ID, outline=self.preCar.color)

            if state is False:
                break
            if type(self.selectedCar) is Car and self.selectedCar.alive:
                ID = self.canvas.find_withtag(self.selectedCar.id)
                self.canvas.itemconfig(ID, outline=settings.setDict['color']['selected'])
                self.carText.delete('1.0', tk.END)
                info = "Car ID: {0}, Car Speed: {1:.3} km/hr\n".format(self.selectedCar.id, self.selectedCar.speed * 3.6)
                self.carText.insert(tk.INSERT, info)
                if debug is True:
                    nextCarDistance = self.selectedCar.trajectory.nextCarDistance
                    carID = nextCarDistance["car"].id if nextCarDistance["car"] is not None else None
                    if carID is not None and carID in self.world.cars.keys() and self.selectedCar.alive:
                        info = "Front carID: {0}, distance: {1}".format(carID, nextCarDistance["distance"])
                        self.carText.insert(tk.INSERT, info)

            elif type(self.selectedCar) is Car and not self.selectedCar.alive:
                self.carText.delete('1.0', tk.END)





