from tkinter import *
from geometry.map import World



'''
def checkCoords(event):
    print(event.x, event.y)
'''
root = Tk()
menu = Menu(root)
root.config(menu = menu)
toolbar = Frame(root)
canvas_height = 300
canvas_width = 300
distance = 30

screen = Frame(root)
world = World(screen, canvas_height, canvas_width, distance)

world.pack(fill = "both", expand = True)

play = Button(toolbar, text = "Action")
playPNG = PhotoImage(file = "png/play-button.png")
play.config(compound = LEFT, image=playPNG,width="50",height="24",bg = "#FFFFFF")
play.pack(side = LEFT, padx = 2, pady = 2)

pause = Button(toolbar, text = "Pause")
pausePNG = PhotoImage(file = "png/pause.png")
pause.config(compound = LEFT, image=pausePNG,width="50",height="24",bg = "#FFFFFF")
pause.pack(side = LEFT, padx = 2, pady = 2)
toolbar.config(bg = "#FFFFFF")
toolbar.pack(side = TOP, fill = X)

#canvas.pack()

screen.pack(side = BOTTOM, fill = X)









root.mainloop()