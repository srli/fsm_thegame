#!/usr/bin/python3

"""Square clicking using planes

   Copyright 2010 Florian Berger <fberger@florian-berger.de>

   Based on a pure PyGame implementation
"""

import pygame
import planes
import pdb
import time
import math
from collections import deque
from screen import Screen
from screen import Button
from screen import ScreenText


class Drag(planes.Plane):
    def __init__(self, name, rect, draggable=True, grab=True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.name = name
        self.image.fill((255, 0, 0))
        self.Xpos = rect.x
        self.Ypos = rect.y

    def clicked(self, button_name):
        self.image.fill((255,0,0))

class Drop(planes.Plane):
    def __init__(self, name, rect, draggable=False, grab=True, control_enbales=[], next_state=0):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        
        self.name = name
        self.Xpos = rect.x
        self.Ypos = rect.y
        
        self.image.fill((0,0,255))
    
    def dropped_upon(self, plane, coordinates):
       planes.Plane.dropped_upon(self, plane, coordinates)
       plane.moving = False

class Toolbar(planes.Plane):
    def __init__(self, name, rect, transitions, controls, draggable = False, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.name = name
        self.Xpos = rect.x
        self.YPos = rect.y
        self.image.fill((0,0,255))

        self.visible = True

        self.transitions = transitions
        self.controls = controls

    def dropped_upon(self, plane, coordinates):
        print (plane.rect.centerx, plane.rect.centery)
        planes.Plane.dropped_upon(self, plane, (plane.rect.centerx, plane.rect.centery))

class Button(Button):
    def __init__(self, label, rect, model):
        Button.__init__(self, label, rect, model)
        self.image.fill((0,0,255))
    def clicked(self, button_name):
        toolbar = self.model.toolbars[0]
        if toolbar.visible == True:
            toolbar.visible = False
        else:
            toolbar.visible = True  
       

class Drop_Display(planes.Display):
	def dropped_upon(self, plane, coordinates):
         if isinstance(plane, Drop):
             planes.Display.dropped_upon(self, plane, coordinates)

class Model():
    def __init__(self):

        self.control_enables = []
        self.states = []
        self.transition_conditions = []
        self.transitions = []
        self.toolbars = []
        self.buttons = []

    def make_Toolbar(self, name, rect, transition_conditions, controls):
        self.toolbars.append(Toolbar(name, rect, transition_conditions, controls))

        for i in range(len(transition_conditions)):
            t = transition_conditions[i]
            rectx = rect.x+20*(i+1)+50*i
            recty = rect.y+20*(i+1)+50*i
            self.transition_conditions.append(Drag(t, pygame.Rect(rectx, recty, 50,50), draggable = True, grab = True))

    # def make_control_enables(self, name, rect):
    #     self.control_enables.append(Drag(name, rect, draggable = True, grab = True))

    # def make_transition_conditions(self, name, rect):
    #     self.transition_conditions.append(Drag(name, rect, draggable = True, grab = True))
    
    def make_states(self, name,rect):
        drop = Drop(name, rect, draggable = False, grab = True)
        self.states.append(drop)


    def update_states(self):
        """
            updates states to have correct control signals
        """
        for state in self.states:
            pass

class View():
    def __init__(self, model, screen): #View contains model and screen
        self.model = model
        self.screen = screen
        
    def update(self, screen):

        for t in self.model.toolbars:
            if t.visible == True:
                this_tool = t
                screen.sub(t)
                for c in self.model.control_enables:
                    screen.sub(c)
                for e in self.model.transition_conditions:
                    print type(e)
                    screen.sub(e)
                    print ("Made a transition")
                print ("Made a toolbar!")



        # for t in self.model.transition_conditions:
        #     this_cond = t
        #     screen.sub(this_cond)
        #     print ("Made a transition condition!")

        for t in self.model.transitions:
            this_trans = t
            screen.sub(this_trans)
            print ("Made a transition!")

        for droppy in self.model.states:
            this_droppy = droppy
            screen.sub(this_droppy)
            print ("Made a drop zone!")
              
        # for draggy in self.model.control_enables:
        #     this_draggy = draggy
        #     screen.sub(this_draggy)                       
        #     print("Made a draggable")
            
            
if __name__ == "__main__":
    running = True    
    pygame.init()
    screen = Drop_Display((800, 800))    
    model = Model()
    view = View(model, screen)
    clock = pygame.time.Clock()
    
    screen.grab = True
    screen.image.fill((0, 128, 0))
    
    #Make some zones
    model.make_states("drop1", pygame.Rect(0, 0, 100, 100))
    #model.make_states("drop2", pygame.Rect(700,400, 100,100)) 

    rect = pygame.Rect(0, 500, 800, 300)
    print type(rect)
    model.make_Toolbar("tool1", rect, ["trans1", "trans2"], [])   
    
    
    #Just to test if materials work
    # for i in range(0,4):    
    #     model.make_control_enables("mat"+`i`, pygame.Rect(200, i*75, 50, 50))    

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