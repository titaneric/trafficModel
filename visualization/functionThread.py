import threading
import csv
import settings
import tkinter as tk
import pickle


class SystemInfoThread(threading.Thread):

    def __init__(self, systemText, world, stateQueue):
        threading.Thread.__init__(self)
        self.world = world
        self.systemText = systemText
        self.stateQueue = stateQueue
        # self.collect = collect

    def run(self):
            while True:
                try:
                    state = self.stateQueue.get()
                    if state is False:
                        break
                    self.systemText.delete('1.0', tk.END)
                    totalVelocity = 0.0
                    carsNumber = 0
                    for road in self.world.roads.values():
                        for lane in road.lanes:
                            carsNumber += len(lane.carsPositions)
                            for carsPosition in lane.carsPositions.values():
                                totalVelocity += carsPosition.car.speed

                    self.systemText.insert(tk.INSERT, 'Avg Speed: {0:.3} km/hr'.format(totalVelocity / carsNumber * 3.6 if carsNumber != 0 else 0.0))
                finally:
                    self.stateQueue.task_done()


class RoadInfoThread(threading.Thread):

    def __init__(self, scaleMap, roadText, stateQueue):
        threading.Thread.__init__(self)
        self.scaleMap = scaleMap
        self.roadText = roadText
        self.stateQueue = stateQueue

    def run(self):
        while True:
            try:
                d = pickle.loads(self.stateQueue.get())
                state = d["state"]
                self.selectedRoad = d["selectedRoad"]
                if state is False:
                    break
                if self.selectedRoad is not None:
                    # print(self.selectedRoad.id)
                    self.roadText.delete('1.0', tk.END)
                    carsNumber = 0
                    totalVelocity = 0.0
                    carsArea = 0.0
                    for lane in self.selectedRoad.lanes:
                        carsNumber += len(lane.carsPositions)
                        for carsPosition in lane.carsPositions.values():
                            totalVelocity += carsPosition.car.speed
                            carsArea += carsPosition.car.length * self.scaleMap["scale"]

                    density = carsArea / self.selectedRoad.length
                    self.roadText.insert(tk.INSERT, ' Road ID: {0}, Avg Speed: {1:.3} km/hr\n Density: {2:.3} car length/meter'.format(self.selectedRoad.id
                    , totalVelocity / carsNumber * 3.6 if carsNumber != 0 else 0.0, density))
            finally:
                self.stateQueue.task_done()


class CollectDataThread(threading.Thread):

    def __init__(self, world, systemText):
        threading.Thread.__init__(self)
        self.world = world
        self.systemText = systemText

    def run(self):
        print("Start collecting")
        while True:
            if self.world.time < settings.setDict["collecting_time"]:
                with open('data/data.csv', 'a', encoding='utf8') as f:
                    fwriter = csv.writer(f, delimiter=',')
                    text = self.systemText.get("1.0", tk.END)
                    avgSpeed = text[len("Avg Speed: "): -len(" km/hr")].strip()
                    fwriter.writerow([self.world.time, avgSpeed])
                f.close()
            else:
                print('Finish collecting')
                break




