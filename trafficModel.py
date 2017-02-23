from tkinter import *
from visualization.operation import Operation
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

carText = Text(info, height=2, width=15)
carText.pack(side=RIGHT)

systemText = Text(info, height=2, width=15)
systemText.pack(side=LEFT)

roadText = Text(info, height=2, width=35)
roadText.pack(side=LEFT)



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

debug = Button(function, text = "Debug")
debugPNG = PhotoImage(file = "png/debug.png")
debug.config(compound = LEFT, image=debugPNG, width="55", height="24", bg = "#FFFFFF", command = lambda : op.debugSwitch())
debug.pack(side = LEFT, padx = 2, pady = 2)

sliderName = Entry(function, width='10')
sliderName.pack(padx = 2, pady = 2)
sliderName.insert(0, "Cars Number")

slider = Scale(function, from_=0, to=30, orient=HORIZONTAL,
    troughcolor="#90C3D4", bg="#FFFFFF")
slider.pack(side = LEFT, padx = 2, pady = 2)

toolDict = dict()
toolDict['carText'] = carText
toolDict['roadText'] = roadText
toolDict['systemText'] = systemText
toolDict['slider'] = slider
toolDict['debugBtn'] = debug

screen = Frame(root)
op = Operation(screen, toolDict, world)
op.pack(fill = "both", expand = True)

function.config(bg = "#90C3D4")
function.pack(side=LEFT)

info.config(bg="#FFFFFF")
info.pack(side=RIGHT)

toolbar.config(bg = "#90C3D4")
toolbar.pack(side = TOP, fill = X)

screen.pack(side = BOTTOM, fill = X)

root.mainloop()
