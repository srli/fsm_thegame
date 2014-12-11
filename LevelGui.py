#!/usr/bin/python3

"""Square clicking using planes

   Copyright 2010 Florian Berger <fberger@florian-berger.de>

   Based on a pure PyGame implementation
"""

import pygame, time
import planes


class Drag(planes.Plane):
    def __init__(self, name, rect, draggable = True, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.name = name
        self.image.fill((255, 0, 0))
        self.Xpos = rect.x
        self.Ypos = rect.y

    def clicked(self, button_name):
        self.image.fill((255,0,0))

class DropZone(planes.Plane):
    def __init__(self, name, rect, draggable = False, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        
        self.name = name
        #print ("made drop Zone with x position", self.Xpos)

        self.Xpos = rect.x
        self.Ypos = rect.y
        
        self.image.fill((0,0,255))
    
    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self, plane, coordinates)
       plane.moving = False



class DropDisplay(planes.Display):
	def dropped_upon(self, plane, coordinates):
         if isinstance(plane, Drag):
#             print plane.Xpos
             planes.Display.dropped_upon(self, plane, (plane.rect.centerx, plane.rect.centery))

class Model():
    def __init__(self):
        self.drag = []
        self.dropZones = []

    def makeDrag(self, name, rect):
        self.drag.append(Drag(name, rect, draggable = True, grab = True))
    
    def makeDropZone(self, name,rect):
        drop = DropZone(name, rect, draggable = False, grab = True)
        self.dropZones.append(drop)
   
class View():
    def __init__(self, model, screen): #View contains model and screen
        self.model = model
        self.screen = screen
        
    def update(self, screen):        
        for droppy in self.model.dropZones:
            this_droppy = droppy
            screen.sub(this_droppy)
            print ("Made a drop zone!")
              
        for draggy in self.model.drag:
            this_draggy = draggy
            screen.sub(this_draggy)                       
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
    model.makeDropZone("drop1", pygame.Rect(0, 0, 100, 100))
    model.makeDropZone("drop2", pygame.Rect(700,400, 100,100))    
    
    #Just to test if materials work
    for i in range(0,4):    
        model.makeDrag("mat"+`i`, pygame.Rect(200, i*75, 50, 50))    

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