from tkinter import *
from geometry.grid import Grid
def createIntersection(event, line_distance):
    x, y = determineCoords(event, line_distance)
    #print(x, y)
    tmpGrid = gridMatrix[x][y]
    if tmpGrid.crossStatus is False:
        cross = canvas.create_rectangle(tmpGrid.x0, tmpGrid.y0, tmpGrid.x1, tmpGrid.y1, fill = "#808080")
        gridMatrix[x][y].crossStatus = True
        

def determineCoords(event, line_distance):
    for x in range(line_distance,canvas_width + line_distance,line_distance):
        for y in range(line_distance,canvas_height + line_distance,line_distance):
            if ((x - line_distance) < event.x < x) and ((y - line_distance) < event.y < y):
                return (x - line_distance)//line_distance, (y - line_distance)//line_distance

def createGrid(canvas, line_distance):
    # vertical lines at an interval of "line_distance" pixel
    for x in range(line_distance,canvas_width,line_distance):
        canvas.create_line(x, 0, x, canvas_height, fill="#000000")
    # horizontal lines at an interval of "line_distance" pixel
    for y in range(line_distance,canvas_height,line_distance):
        canvas.create_line(0, y, canvas_width, y, fill="#000000")
    
    for x in range(0, canvas_width, line_distance):
        for y in range(0, canvas_height, line_distance):
            tmpGrid = Grid(x, y, line_distance)
            gridMatrix[x // line_distance][y // line_distance] = tmpGrid

def createRoad():
    return

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

screen = Frame(root)
canvas = Canvas(screen, width = canvas_width, height = canvas_height)
canvas.bind("<Button-1>", lambda event, line_distance = distance: createIntersection(event, line_distance))


#crossBtn = Button(toolbar, text = "add", command = lambda: createIntersection(canvas))
#crossBtn.pack(side = LEFT, padx = 2, pady = 2)
#toolbar.pack(side = TOP, fill = X)

canvas.pack()
createGrid(canvas, distance)
screen.pack(side = BOTTOM, fill = X)









root.mainloop()