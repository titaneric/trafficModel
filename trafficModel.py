import tkinter as tk
from system.operation import Operation
from model.world import World
import settings


root = tk.Tk()
img = tk.PhotoImage(file='png/sports-car.png')
root.tk.call('wm', 'iconphoto', root._w, img)
menu = tk.Menu(root)

root.config(menu=menu)
root.protocol("WM_DELETE_WINDOW", lambda: op.terminate(root))
toolbar = tk.Frame(root)
function = tk.Frame(toolbar)
info = tk.Frame(toolbar)
world = World()
world.load()

buttonGroup = tk.Frame(function)
sliderGroup = tk.Frame(function)


play = tk.Button(buttonGroup, text="Action")
playPNG = tk.PhotoImage(file="png/play-button.png")
pausePNG = tk.PhotoImage(file="png/pause.png")
play.config(compound=tk.LEFT, image=playPNG, width="70", 
            height="24", bg="#FFFFFF", command=lambda: op.runModel())
play.pack(side=tk.LEFT, padx=2, pady=2)

refresh = tk.Button(buttonGroup, text="Reload")
refreshPNG = tk.PhotoImage(file="png/refresh-button.png")
refresh.config(compound=tk.LEFT, image=refreshPNG, width="70", 
               height="24", bg="#FFFFFF", command=lambda: op.refresh())
refresh.pack(side=tk.LEFT, padx=2, pady=2)

debug = tk.Button(buttonGroup, text="Debug")
debugPNG = tk.PhotoImage(file="png/debug.png")
debug.config(compound=tk.LEFT, image=debugPNG, width="70", 
             height="24", bg="#FFFFFF", command=lambda: op.debugSwitch())
debug.pack(side=tk.LEFT, padx=2, pady=2)

gridMap = tk.Button(buttonGroup, text="New Map")
mapPNG = tk.PhotoImage(file="png/map.png")
gridMap.config(compound=tk.LEFT, image=mapPNG, width="70", 
               height="24", bg="#FFFFFF", command=lambda: op.generateMap())
gridMap.pack(side=tk.LEFT, padx=2, pady=2)

timeSliderName = tk.Entry(sliderGroup, width='10')
timeSliderName.grid(row=0, column=0)
timeSliderName.insert(0, "Time scale")

timeSlider = tk.Scale(sliderGroup, from_=settings.setDict["timeMin"], 
                      to=settings.setDict["timeMax"], orient=tk.HORIZONTAL,
                      troughcolor="#90C3D4", bg="#FFFFFF")
timeSlider.grid(row=1, column=0)

carSliderName = tk.Entry(sliderGroup, width='10')
carSliderName.grid(row=0, column=1)
carSliderName.insert(0, "Cars Number")

carSlider = tk.Scale(sliderGroup, from_=settings.setDict["carMin"], 
                     to=settings.setDict["carMax"], orient=tk.HORIZONTAL,
                     troughcolor="#90C3D4", bg="#FFFFFF")
carSlider.grid(row=1, column=1)

systemName = tk.Entry(info, width='10')
systemName.grid(row=0, column=0)
systemName.insert(0, "System")

systemText = tk.Text(info, height=2, width=40)
systemText.grid(row=1, column=0)

roadName = tk.Entry(info, width='10')
roadName.grid(row=0, column=1)
roadName.insert(0, "Road info")

roadText = tk.Text(info, height=2, width=45)
roadText.grid(row=1, column=1)

carName = tk.Entry(info, width='10')
carName.grid(row=0, column=2)
carName.insert(0, "Car info")

carText = tk.Text(info, height=2, width=40)
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

screen = tk.Frame(root)
op = Operation(screen, toolDict, world)
op.pack(fill="both", expand=True)

buttonGroup.config(bg="#90C3D4")
buttonGroup.pack(side=tk.LEFT)

sliderGroup.config(bg="#90C3D4")
sliderGroup.pack(side=tk.LEFT)

function.config(bg="#90C3D4")
function.pack(side=tk.LEFT)

info.config(bg="#90C3D4")
info.pack(side=tk.RIGHT)

toolbar.config(bg="#90C3D4")
toolbar.pack(side=tk.TOP, fill=tk.X)

screen.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
