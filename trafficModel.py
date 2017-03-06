from tkinter import *
from visualization.operation import Operation
from model.world import World
import settings

root = Tk()
img = PhotoImage(file='png/sports-car.png')
root.tk.call('wm','iconphoto',root._w,img)
menu = Menu(root)



subMenu = Menu(menu)
menu.add_cascade(label='Test', menu=subMenu)
subMenu.add_command(label='Collect Data', command=lambda :op.collectData())

root.config(menu=menu)
toolbar = Frame(root)
function = Frame(toolbar)
info = Frame(toolbar)
world = World()
world.load()

buttonGroup = Frame(function)
sliderGroup = Frame(function)


play = Button(buttonGroup, text = "Action")
playPNG = PhotoImage(file = "png/play-button.png")
pausePNG = PhotoImage(file = "png/pause.png")
play.config(compound = LEFT, image=playPNG, width="55", height="24", bg = "#FFFFFF", command = lambda : op.runModel())
play.pack(side = LEFT, padx = 2, pady = 2)

refresh = Button(buttonGroup, text = "Reload")
refreshPNG = PhotoImage(file = "png/refresh-button.png")
refresh.config(compound = LEFT, image=refreshPNG, width="55", height="24", bg = "#FFFFFF", command = lambda : op.refresh())
refresh.pack(side = LEFT, padx = 2, pady = 2)

debug = Button(buttonGroup, text = "Debug")
debugPNG = PhotoImage(file = "png/debug.png")
debug.config(compound = LEFT, image=debugPNG, width="55", height="24", bg = "#FFFFFF", command = lambda : op.debugSwitch())
debug.pack(side = LEFT, padx = 2, pady = 2)

timeSliderName = Entry(sliderGroup, width='10')
timeSliderName.grid(row=0, column=0)
timeSliderName.insert(0, "Time scale")

timeSlider = Scale(sliderGroup, from_=settings.setDict["timeMin"], to=settings.setDict["timeMax"], orient=HORIZONTAL,
    troughcolor="#90C3D4", bg="#FFFFFF")
timeSlider.grid(row=1, column=0)

carSliderName = Entry(sliderGroup, width='10')
carSliderName.grid(row=0, column=1)
carSliderName.insert(0, "Cars Number")

carSlider = Scale(sliderGroup, from_=settings.setDict["carMin"], to=settings.setDict["carMax"], orient=HORIZONTAL,
    troughcolor="#90C3D4", bg="#FFFFFF")
carSlider.grid(row=1, column=1)

systemName = Entry(info, width='10')
systemName.grid(row=0, column=0)
systemName.insert(0, "System")

systemText = Text(info, height=2, width=40)
systemText.grid(row=1, column=0)

roadName = Entry(info, width='10')
roadName.grid(row=0, column=1)
roadName.insert(0, "Road info")

roadText = Text(info, height=2, width=45)
roadText.grid(row=1, column=1)

carName = Entry(info, width='10')
carName.grid(row=0, column=2)
carName.insert(0, "Car info")

carText = Text(info, height=2, width=40)
carText.grid(row=1, column=2)

toolDict = dict()
toolDict['playBtn'] = play
toolDict['playPNG'] = playPNG
toolDict['pausePNG'] = pausePNG
toolDict['carText'] = carText
toolDict['roadText'] = roadText
toolDict['systemText'] = systemText
toolDict['carSlider'] = carSlider
toolDict['timeSlider'] = timeSlider
toolDict['debugBtn'] = debug

screen = Frame(root)
op = Operation(screen, toolDict, world)
op.pack(fill = "both", expand = True)

buttonGroup.config(bg = "#90C3D4")
buttonGroup.pack(side=LEFT)

sliderGroup.config(bg = "#90C3D4")
sliderGroup.pack(side=LEFT)

function.config(bg = "#90C3D4")
function.pack(side=LEFT)

info.config(bg="#90C3D4")
info.pack(side=RIGHT)

toolbar.config(bg = "#90C3D4")
toolbar.pack(side = TOP, fill = X)

screen.pack(side = BOTTOM, fill = X)

root.mainloop()
