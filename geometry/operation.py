import tkinter as tk
from model.world import World
from model.intersection import Intersection
from model.road import Road
from geometry.rect import Rect
class  Operation(tk.Frame):
    def __init__(self, root, canvas_height, canvas_width, distance, world):
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(self, width=300, height=300, background="bisque")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,1000,1000))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # This is what enables using the mouse to drag:
        
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.canvas.bind("<ButtonRelease>", self.ready2CreateRoad)
        #linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        #windows scroll
        self.canvas.bind("<MouseWheel>",self.zoomer)
        self.canvas.bind("<Double-Button-1>", self.drawIntersection)#lambda event, line_distance = distance: self.createIntersection(event, line_distance))
        self.buildable = False
        self.movePath = []
        self.scale = 1
        self.world = world
        self.distance = distance
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.drawGrid()
        self.drawWorld()
    
    def scroll_start(self, event):
        itemID  = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        #the empty grid
        if self.canvas.itemcget(itemID, "fill") == "bisque": 
            self.canvas.scan_mark(event.x, event.y)
        #existed intersection
        elif self.canvas.itemcget(itemID, "fill") == "#808080":
            self.buildable = True

    def scroll_move(self, event):
        if self.buildable is False:  
            self.canvas.scan_dragto(event.x, event.y, gain=1)
        else:
            self.movePath.append((self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)))
    
    def ready2CreateRoad(self, event):
        #itemID  = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        if self.buildable is False:
            return
        else:
            self.drawIntersection(event)
            self.drawRoad(event)

    #windows zoom
    def zoomer(self,event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    #linux zoom
    def zoomerP(self,event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self.scale *= 1.1
        

    def zoomerM(self,event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self.scale *= 0.9
        
    def update_coords(self, coords):
        new_coords = [coords_i * self.scale for coords_i in coords]
        return new_coords

    def drawIntersection(self, event):
        itemID = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        if self.canvas.itemcget(itemID, "fill") == "bisque":
            coords = self.canvas.coords(itemID)
            rect = Rect(coords[0], coords[1], self.distance, self.distance)
            intersection = Intersection(rect)
            self.buildIntersection(intersection)
            self.world.intersections[intersection.id] = intersection
        else:
            return

    def buildIntersection(self, intersection):
        self.canvas.create_rectangle(intersection.rect.x, intersection.rect.y, intersection.rect.x + intersection.rect.width, intersection.rect.y + intersection.rect.height, fill = "#808080", outline = "#FFFFFF")
   
    def drawGrid(self):
        for y in range(0, self.canvas_height, self.distance):
            for x in range(0, self.canvas_width, self.distance):
                self.canvas.create_rectangle(x, y, x + self.distance, y + self.distance, fill = "bisque", outline = "#FFFFFF")
            
    def drawRoad(self, event):
        itemID = self.canvas.find_closest(self.movePath[0][0], self.movePath[0][1])
        sourceCoords = self.canvas.coords(itemID)
        sourceID = self.findIntersectionID(sourceCoords)
        itemID = self.canvas.find_closest(self.movePath[-1][0], self.movePath[-1][1])
        targetCoords = self.canvas.coords(itemID)
        targetID = self.findIntersectionID(targetCoords)
        road = Road(self.world.intersections[sourceID], self.world.intersections[targetID])
        self.world.roads[road.id] = road
        self.buildRoad(road)        
        road = Road(self.world.intersections[targetID], self.world.intersections[sourceID])
        self.world.roads[road.id] = road
        self.buildRoad(road)
        self.buildable = False
        self.movePath.clear()

    def buildRoad(self, road):#Fixed me
        source = road.source
        target = road.target
        #the vertical road
        if source.rect.x == target.rect.x:
            mid = (source.rect.x + target.rect.x + target.rect.width) // 2
            x0, y0, x1, y1 = (0, 0, 0, 0)   
            if source.rect.y < target.rect.y:
                x0 = source.rect.x
                y0 = source.rect.y + source.rect.height
                x1 = target.rect.x + target.rect.width
                y1 = target.rect.y     
                self.canvas.create_rectangle(x1, y1, mid, y0, fill = "#808080", outline = "#FFFFFF")                                                                         
            elif source.rect.y > target.rect.y:
                x0 = target.rect.x
                y0 = target.rect.y + target.rect.height
                x1 = source.rect.x + source.rect.width
                y1 = source.rect.y
                self.canvas.create_rectangle(x0, y0, mid, y1, fill = "#808080", outline = "#FFFFFF")                        
                

            self.canvas.create_line(mid, y0, mid, y1, fill = "yellow", dash = (10, 10), width = 3)
         #the horizontal road
        elif source.rect.y == target.rect.y:
            mid = (source.rect.y + target.rect.y + target.rect.height) // 2 
            x0, y0, x1, y1 = (0, 0, 0, 0)          
            if source.rect.x < target.rect.x:
                x0 = source.rect.x + source.rect.width
                y0 = source.rect.y
                x1 = target.rect.x
                y1 = target.rect.y + target.rect.height
                self.canvas.create_rectangle(x0, y0, x1, mid, fill = "#808080", outline = "#FFFFFF")                                       
            elif source.rect.x > target.rect.x:
                x0 = target.rect.x + target.rect.width
                y0 = target.rect.y
                x1 = source.rect.x
                y1 = source.rect.y + source.rect.height
                self.canvas.create_rectangle(x1, y1, x0, mid, fill = "#808080", outline = "#FFFFFF")                                       
                

            self.canvas.create_line(x0, mid, x1, mid, fill = "yellow", dash = (10, 10), width = 3)
     
    def drawWorld(self):
        for intersection in self.world.intersections.values():
            self.buildIntersection(intersection)

        for road in self.world.roads.values():
            self.buildRoad(road)

    def findIntersectionID(self, coords):
        for intersection in self.world.intersections.values():
            if coords[0] == intersection.rect.x and coords[1] == intersection.rect.y:
                return intersection.id

        

    '''
    def moveCar(self, tag):
        itemID = self.canvas.find_withtag(tag)
        beforePos = self.canvas.coords(itemID)
        afterPos = (beforePos[0] + 20, beforePos[1], beforePos[2] + 20, beforePos[3])
        self.canvas.coords(itemID, afterPos[0], afterPos[1], afterPos[2], afterPos[3])

    '''

    

