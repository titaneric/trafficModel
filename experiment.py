import csv
import sys

from model.world import World
from settings import setDict


START_DENSITY = 0.005
TERMINATE_DENSITY = 0.9
STEP = 0.005
ITERATION = 10
CAR_NUM = 15
START_COLLECT = 10000
checkLockTime = 10000
zero = [0 for i in range(10)]
for car in range(15, 220, 5):
    print('Car number is {}'.format(car))
    i = 0
    while i < ITERATION:
        print('exp{}'.format(i + 1))
        world = World(exp=True)
        world.load()
        world.carsNumber = car
        expList = []
        time = 0
        zeroList = []
        while time < setDict["collecting_time"] + 1:
            world.onTick(0.2)
            if len(world.cars) == 0:
                print()
                break
            avgSpeed, avgDensity, flow = world.systemInfo()
            zeroList.append(0 if avgSpeed == 0.0 else 1)
            if time > 100 and zeroList[-10:] == zero:
                print()
                break
            if time > START_COLLECT:
                expList.append({'time': time, 'avgSpeed': avgSpeed,
                                'flow': flow, 'avgDensity': avgDensity})                            
                sys.stdout.write("\r%d%%" % ((time - START_COLLECT) / 100))
                sys.stdout.flush()
            time += 1
        if  time > 20000:
            with open('exp/car_{0}_id_{1}.csv'.format(car, i), 'w') as f:
                colName = ['time', 'avgSpeed', 'flow', 'avgDensity']
                fwriter = csv.DictWriter(f, fieldnames=colName)
                fwriter.writeheader()
                fwriter.writerows(expList)
                f.close()
                i += 1
            print()
    print('--------------------------------------------')
