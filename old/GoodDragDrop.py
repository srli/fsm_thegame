#!/usr/bin/python3

"""Square clicking using planes

   Copyright 2010 Florian Berger <fberger@florian-berger.de>

   Based on a pure PyGame implementation
"""

import sys

sys.path.append("../")
sys.path.append("./")

import pygame
import planes
from collections import deque

class Material():

    def __init__(self, name):
        self.name = name
        self.strength = 0
        self.meltingPoint = 0
        self.Xpos = 0
        self.Ypos = 0

    def clicked(self, button_name):
        self.image.fill((255,0,0))

class MaterialView(planes.Plane):
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

class DropDisplay(planes.Display):
	def dropped_upon(self, plane, coordinates):
         if isinstance(plane, MaterialView):
#             print plane.Xpos
             planes.Display.dropped_upon(self, plane, (plane.Xpos, plane.Ypos))

class Model():
    def __init__(self):
        self.materials = []
        self.dropZones = []

    def makeMaterials(self, name):
        self.materials.append(Material(name))
    
    def makeDropZone(self, name, x, y, length, width):
        self.dropZones.append(DropZone(name, x, y, length, width))

    

class View():
    def __init__(self, model, screen): #View contains model and screen
        self.model = model
        self.screen = screen
        
    def updateMats(self, screen):        
        for material in range (len(self.model.materials)):
            thisMaterial = self.model.materials[material]
            thisMaterial.Xpos = 750
            thisMaterial.Ypos = 800/len(self.model.materials) * material
            screen.sub(MaterialView(thisMaterial.name, pygame.Rect((thisMaterial.Xpos, thisMaterial.Ypos, 20, 20), draggable=True, grab=True)))                       
            print("Made a plane")
        
        for zone in range(len(self.model.dropZones)):
            thisZone = self.model.dropZones[zone]
            screen.sub(DropZoneView(thisZone.name, pygame.Rect((thisZone.Xpos, thisZone.Ypos, thisZone.length, thisZone.width), draggable=True, grab=True)))
            print ("Made a drop zone!")
            
            
if __name__ == "__main__":
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
    
    print ("made some zones")    
    
    #Just to test if materials work
    for i in range(0,4):    
        model.makeMaterials("mat"+`i`)    

    print("made some materials")
    
    view.updateMats(screen)
    print("Updated the materials view")

    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
				print("got pygame.QUIT, terminating")
				raise SystemExit

        screen.process(events)
        screen.render()
        pygame.display.flip()