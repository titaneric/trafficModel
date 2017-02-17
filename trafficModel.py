from tkinter import *
from geometry.operation import Operation
from model.world import World


root = Tk()

#menu = Menu(root)
#root.config(menu = menu)
toolbar = Frame(root)
world = World()
world.load()
screen = Frame(root)
op = Operation(screen, world)
op.pack(fill = "both", expand = True)

play = Button(toolbar, text = "Action")
playPNG = PhotoImage(file = "png/play-button.png")
play.config(compound = LEFT, image=playPNG, width="50", height="24", bg = "#FFFFFF", command = lambda : op.runModel())
play.pack(side = LEFT, padx = 2, pady = 2)

pause = Button(toolbar, text = "Pause")
pausePNG = PhotoImage(file = "png/pause.png")
pause.config(compound = LEFT, image=pausePNG, width="50", height="24", bg = "#FFFFFF", command = lambda : op.stop())
pause.pack(side = LEFT, padx = 2, pady = 2)

refresh = Button(toolbar, text = "Reload")
refreshPNG = PhotoImage(file = "png/refresh-button.png")
refresh.config(compound = LEFT, image=refreshPNG, width="50", height="24", bg = "#FFFFFF", command = lambda : op.refresh())
refresh.pack(side = LEFT, padx = 2, pady = 2)

toolbar.config(bg = "#FFFFFF")
toolbar.pack(side = TOP, fill = X)

#canvas.pack()

screen.pack(side = BOTTOM, fill = X)








root.mainloop()
