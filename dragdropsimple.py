#!/usr/bin/python3

"""Square clicking using planes

   Copyright 2010 Florian Berger <fberger@florian-berger.de>

   Based on a pure PyGame implementation
"""

import pygame, time
import planes


class Drag():
    def __init__(self, name, xpos, ypos):
        self.name = name
        self.Xpos = xpos
        self.Ypos = ypos

    def clicked(self, button_name):
        self.image.fill((255,0,0))

class DragView(planes.Plane):
    def __init__(self, name, rect, draggable = True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.image.fill((255, 0, 0))
        self.Xpos = rect.x
        self.Ypos = rect.y

class DropZone():
    def __init__(self, name, x, y, length, width):
        self.name = name
        self.Xpos = x
        self.Ypos = y
        self.length = length
        self.width = width
        print ("made drop Zone with x position", self.Xpos)



class DropDisplay(planes.Display):
	def dropped_upon(self, plane, coordinates):
         if isinstance(plane, MaterialView):
#             print plane.Xpos
             planes.Display.dropped_upon(self, plane, (plane.Xpos, plane.Ypos))

class DropZoneView(planes.Plane):
    def __init__(self, name, rect, draggable = False, grab = True):
        self.name = name
        self.Xpos = rect.x
        self.Ypos = rect.y
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.image.fill((0,0,255))
    
    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self, plane, coordinates)
       plane.moving = False

            
class Model():
    def __init__(self):
        self.drag = []
        self.dropZones = []

    def makeDrag(self, name, xpos, ypos):
        self.drag.append(Drag(name, xpos, ypos))
    
    def makeDropZone(self, name, x, y, length, width):
        self.dropZones.append(DropZone(name, x, y, length, width))

    

class View():
    def __init__(self, model, screen): #View contains model and screen
        self.model = model
        self.screen = screen
        
    def update(self, screen):        
        for droppy in self.model.dropZones:
            this_droppy = droppy
            screen.sub(DropZoneView(this_droppy.name, pygame.Rect((this_droppy.Xpos, this_droppy.Ypos, this_droppy.length, this_droppy.width), draggable=True, grab=True)))
            print ("Made a drop zone!")
              
        for draggy in self.model.drag:
            this_draggy = draggy
            screen.sub(DragView(this_draggy.name, pygame.Rect((this_draggy.Xpos, this_draggy.Ypos, 20, 20), draggable=True, grab=True)))                       
            print("Made a draggable")
            
            
if __name__ == "__main__":
    running = True    
    pygame.init()
    screen = DropDisplay((800, 800))    
    model = Model()
    view = View(model, screen)
    clock = pygame.time.Clock()
    
    screen.grab = True
    screen.image.fill((0, 128, 0))
    
    #Make some zones
    model.makeDropZone("drop1", 0, 0, 100, 100)
    model.makeDropZone("drop2", 700,400, 100,100)    
    
    #Just to test if materials work
    for i in range(0,4):    
        model.makeDrag("mat"+`i`, 500, i*50)    

    view.update(screen)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
				running = False

        screen.process(events)
        screen.render()
        pygame.display.flip()
        time.sleep(0.001)