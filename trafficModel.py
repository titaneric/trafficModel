from tkinter import *
from geometry.operation import Operation
from model.world import World
import settings


root = Tk()
#menu = Menu(root)
#root.config(menu = menu)
toolbar = Frame(root)
function = Frame(toolbar)
info = Frame(toolbar)
world = World()
world.load()

text = Text(info, height = 3)
text.pack()

screen = Frame(root)
op = Operation(screen, text, world)
op.pack(fill = "both", expand = True)

play = Button(function, text = "Action")
playPNG = PhotoImage(file = "png/play-button.png")
play.config(compound = LEFT, image=playPNG, width="55", height="24", bg = "#FFFFFF", command = lambda : op.runModel())
play.pack(side = LEFT, padx = 2, pady = 2)

pause = Button(function, text = "Pause")
pausePNG = PhotoImage(file = "png/pause.png")
pause.config(compound = LEFT, image=pausePNG, width="55", height="24", bg = "#FFFFFF", command = lambda : op.stop())
pause.pack(side = LEFT, padx = 2, pady = 2)

refresh = Button(function, text = "Reload")
refreshPNG = PhotoImage(file = "png/refresh-button.png")
refresh.config(compound = LEFT, image=refreshPNG, width="55", height="24", bg = "#FFFFFF", command = lambda : op.refresh())
refresh.pack(side = LEFT, padx = 2, pady = 2)

function.config(bg = "#90C3D4")
function.pack(side=LEFT)

info.config(bg="#FFFFFF")
info.pack(side=RIGHT, padx=10, pady=10)

toolbar.config(bg = "#90C3D4")
toolbar.pack(side = TOP, fill = X)

screen.pack(side = BOTTOM, fill = X)

root.mainloop()
