from tkinter import *
from geometry.map import World

def createIntersection(event, line_distance):
        #x, y = determineCoords(event, line_distance)
        #print(x, y)
        itemID = world.canvas.find_closest(world.canvas.canvasx(event.x), world.canvas.canvasy(event.y))
        world.canvas.itemconfig(itemID, fill = "#808080")
   
def createGrid(world, line_distance):
    for y in range(0, canvas_height, line_distance):
        for x in range(0, canvas_width, line_distance):
            world.canvas.create_rectangle(x, y, x + line_distance, y + line_distance, fill = "bisque", outline = "#FFFFFF")
        

def createRoad(event, line_distance):
    print(event.x, event.y)
    x, y = determineCoords(event, line_distance)
    #print(x, y)
    tmpGrid = gridMatrix[x][y]
    canvas.create_rectangle(tmpGrid.x0, tmpGrid.y0, firstSelectedCross.x1, firstSelectedCross.y1, fill = "#808080")

'''
def checkCoords(event):
    print(event.x, event.y)
'''
root = Tk()
#menu = Menu(root)
#root.config(menu = menu)
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

screen = Frame(root)
world = World(screen)
#world.canvas.bind("<Button-1>", checkCoords)
world.canvas.bind("<Double-Button-1>", lambda event, line_distance = distance: createIntersection(event, line_distance))
#world.canvas.bind("<B1-Motion>", lambda event, line_distance = distance: createRoad(event, line_distance))
world.pack(fill = "both", expand = True)
#canvas.bind("<ButtonRelease>",lambda event, line_distance = distance: createRoad(event, line_distance))
#crossBtn = Button(toolbar, text = "add", command = lambda: createIntersection(canvas))
#crossBtn.pack(side = LEFT, padx = 2, pady = 2)
#toolbar.pack(side = TOP, fill = X)

#canvas.pack()
createGrid(world, distance)
screen.pack(side = BOTTOM, fill = X)









root.mainloop()