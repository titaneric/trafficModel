from tkinter import *
from geometry.grid import Grid
from geometry.map import World

def createIntersection(event, line_distance):
        x, y = determineCoords(event, line_distance)
        print(x, y)
        tmpGrid = gridMatrix[x][y]
        if tmpGrid.crossStatus is False:
            world.canvas.create_rectangle(tmpGrid.x0, tmpGrid.y0, tmpGrid.x1, tmpGrid.y1, fill = "#808080")
            gridMatrix[x][y].crossStatus = True
        
        else:
            world.canvas.create_rectangle(tmpGrid.x0, tmpGrid.y0, tmpGrid.x1, tmpGrid.y1, fill = "#808080", dash = (4, 4))
            firstSelectedCross = tmpGrid
            firstSelectedStatus = True
   

def determineCoords(event, line_distance):
    itemID = world.canvas.find_closest(event.x, event.y)
    print("ID is", itemID)
    index = itemID[0]
    #assert 0 < index <= (canvas_width // line_distance) * (canvas_height // line_distance)
    index -= 1
    #First picked intersection
    if 0 < index < (canvas_width // line_distance) * (canvas_height // line_distance):
        x, y = (index // (canvas_height // line_distance), index % (canvas_height // line_distance))
        return y, x
    #Select the intersection to be the part of road

def createGrid(world, line_distance):
    for y in range(0, canvas_height, line_distance):
        for x in range(0, canvas_width, line_distance):
            world.canvas.create_rectangle(x, y, x + line_distance, y + line_distance, fill = "bisque", outline = "#FFFFFF")
            tmpGrid = Grid(x, y, line_distance)
            gridMatrix[x // line_distance][y // line_distance] = tmpGrid

def createRoad(event, line_distance):
    print(event.x, event.y)
    x, y = determineCoords(event, line_distance)
    #print(x, y)
    tmpGrid = gridMatrix[x][y]
    canvas.create_rectangle(tmpGrid.x0, tmpGrid.y0, firstSelectedCross.x1, firstSelectedCross.y1, fill = "#808080")
'''
def pickIntersection(event, line_distance):
    #print(event.x, event.y)
    x, y = determineCoords(event, line_distance)
    #print(x, y)
    tmpGrid = gridMatrix[x][y]
    world.canvas.create_rectangle(tmpGrid.x0, tmpGrid.y0, tmpGrid.x1, tmpGrid.y1, fill = "#A69E24")
'''
'''
def checkCoords(event):
    print(event.x, event.y)
'''
root = Tk()

menu = Menu(root)
root.config(menu = menu)
'''
------------Canvas--------------
app:
    createIntersection
    createGrid
'''
#toolbar = Frame(root)
canvas_height = 300
canvas_width = 300
distance = 30
gridMatrix = [[Grid() for i in range(0, canvas_width, distance)] for j in range(0, canvas_height, distance)]
firstSelectedCross = Grid()
firstSelectedStatus = False
screen = Frame(root)
world = World(screen)
#world.canvas.bind("<Button-1>", checkCoords)
world.canvas.bind("<Double-Button-1>", lambda event, line_distance = distance: createIntersection(event, line_distance))
#world.canvas.bind("<Enter>", lambda event, line_distance = distance: pickIntersection(event, line_distance))
world.pack(fill = "both", expand = True)
#canvas.bind("<ButtonRelease>",lambda event, line_distance = distance: createRoad(event, line_distance))
#crossBtn = Button(toolbar, text = "add", command = lambda: createIntersection(canvas))
#crossBtn.pack(side = LEFT, padx = 2, pady = 2)
#toolbar.pack(side = TOP, fill = X)

#canvas.pack()
createGrid(world, distance)
screen.pack(side = BOTTOM, fill = X)









root.mainloop()