from tkinter import *
from geometry.map import World



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
world = World(screen, canvas_height, canvas_width, distance)

world.pack(fill = "both", expand = True)

#crossBtn = Button(toolbar, text = "add", command = lambda: createIntersection(canvas))
#crossBtn.pack(side = LEFT, padx = 2, pady = 2)
#toolbar.pack(side = TOP, fill = X)

#canvas.pack()

screen.pack(side = BOTTOM, fill = X)









root.mainloop()