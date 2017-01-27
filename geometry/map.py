import tkinter as tk
class  World(tk.Frame):
    def __init__(self, root, canvas_height, canvas_width, distance):
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
        self.canvas.bind("<Double-Button-1>", self.createIntersection)#lambda event, line_distance = distance: self.createIntersection(event, line_distance))
        self.buildable = False
        self.movePath = []
        self.scale = 1
        self.distance = distance
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.createGrid()
    
    def scroll_start(self, event):
        itemID  = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        #the empty grid
        if self.canvas.itemcget(itemID, "fill") == "bisque": 
            self.canvas.scan_mark(event.x, event.y)
        #existed intersection
        elif self.canvas.itemcget(itemID, "fill") == "#808080":
            self.srcX = self.canvas.canvasx(event.x)
            self.srcY = self.canvas.canvasy(event.y)
            self.buildable = True

    def scroll_move(self, event):
        if self.buildable is False:  
            self.canvas.scan_dragto(event.x, event.y, gain=1)
        else:
            self.movePath.append((self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)))
            return
    
    def ready2CreateRoad(self, event):
        itemID  = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        if self.buildable is False:
            return
        else:
            self.createIntersection(event)
            self.createRoad(event)

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

    def createIntersection(self, event):
        itemID = self.canvas.find_closest(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.itemconfig(itemID, fill = "#808080")
   
    def createGrid(self):
        for y in range(0, self.canvas_height, self.distance):
            for x in range(0, self.canvas_width, self.distance):
                self.canvas.create_rectangle(x, y, x + self.distance, y + self.distance, fill = "bisque", outline = "#FFFFFF")
            
    def createRoad(self, event):
        distX = self.canvas.canvasx(event.x)
        distY = self.canvas.canvasy(event.y)
        roadCoords = []
        for move_x, move_y in self.movePath:
            itemID = self.canvas.find_closest(move_x, move_y)
            if self.canvas.itemcget(itemID, "fill") == "bisque":
                self.canvas.itemconfig(itemID, fill = "#808080")
                roadCoords.append(self.canvas.coords(itemID))
        
        if len(roadCoords) >= 2:
            #the horizontal road
            if roadCoords[0][1] == roadCoords[-1][1]:
                mid = (roadCoords[0][1] + roadCoords[-1][3]) // 2
                self.canvas.create_line(roadCoords[0][0], mid, roadCoords[-1][2], mid, fill = "yellow", dash = (10, 10), width = 3)
            #the vertical road
            if roadCoords[0][0] == roadCoords[-1][0]:
                mid = (roadCoords[0][0] + roadCoords[-1][2]) // 2
                self.canvas.create_line(mid, roadCoords[0][1], mid, roadCoords[-1][3], fill = "yellow", dash = (10, 10), width = 3)                
        '''
        for x0, y0, x1, y1 in roadCoords:
            self.canvas.create_line(x0, y0, x1, y1, fill = "yellow", dash = (10, 10), width = 3)
        '''
        self.buildable = False
        self.movePath.clear()
        roadCoords.clear()

    

    

