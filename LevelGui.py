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
    def __init__(self, name, rect, draggable, grab=True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.name = name
        self.image.fill((255, 0, 0))
        self.Xpos = rect.x
        self.Ypos = rect.y
        self.draggable = draggable

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
       plane.XPos = coordinates[0]
       plane.YPos = coordinates[1]

class Toolbar(planes.Plane):
    def __init__(self, name, rect, transition_conditions, controls, draggable = False, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.name = name
        self.Xpos = rect.x
        self.YPos = rect.y
        self.image.fill((0,0,255))

        self.visible = True

        self.transitions = transition_conditions
        self.controls = controls

    def dropped_upon(self, plane, coordinates):
        print (plane.rect.centerx, plane.rect.centery)
        planes.Plane.dropped_upon(self, plane, (plane.rect.centerx, plane.rect.centery))

    # def set_visible(self, v):
    #     self.visible = v

    # def get_visible(self):
    #     return self.visible

class FSM_Zone(planes.Plane):
    def __init__(self, name, rect, transitions, states, draggable = False, grab = True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.name = name
        self.Xpos = rect.x
        self.YPos = rect.y
        self.image.fill((255,0,0))

        self.transitions = transitions
        self.states = states

    def dropped_upon(self, plane, coordinates):
        print (plane.rect.centerx, plane.rect.centery)
        planes.Plane.dropped_upon(self, plane, (plane.rect.centerx, plane.rect.centery))


class SwitchButton(Button):
    def __init__(self, label, rect, callback, model):
        Button.__init__(self, label, rect, callback, model)
        self.model = model
        self.image.fill((0,255,0))
    def clicked(self, button_name):
        print "CLICKED!"
        toolbar = self.model.toolbars[0]

        for c in self.model.control_enables:
            c.draggable = not c.draggable
            print c.draggable
        for t in self.model.transitions:
            t.draggable = not t.draggable
            print t.draggable
        for t in self.model.transition_conditions:
            t.draggable = not t.draggable
            print t.draggable
       

class Drop_Display(planes.Display):
	def dropped_upon(self, plane, coordinates):
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

        counterx = 0
        countery = 1

        space = 20
        side = 100

        for i in range(len(transition_conditions)):
            t = transition_conditions[i]
            
            counterx = int(i/2)
            countery = not countery

            rectx = rect.x+ (counterx+1)*space + counterx * side
            if countery == 0:
                recty = rect.y+20
            if countery == 1:
                recty = rect.y + 2*space + side

            self.transition_conditions.append(Drag(t, pygame.Rect(rectx, recty, side,side), draggable = True, grab = True))


        for i in range(len(controls)):
            t = transition_conditions[i]
            
            counterx = int(i/2)
            countery = not countery

            rectx = rect.x+ (counterx+1)*space + counterx * side
            if countery == 0:
                recty = rect.y+20
            if countery == 1:
                recty = rect.y + 2*space + side

            self.transition_conditions.append(Drag(t, pygame.Rect(rectx, recty, side,side), draggable = True, grab = True))

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

    def make_Button(self, label, rect):
        self.buttons.append(SwitchButton("Button", rect, SwitchButton.clicked, self))

class View():
    def __init__(self, model, screen): #View contains model and screen
        self.model = model
        self.screen = screen

    # def continuous_update(self, screen):

    #     for t in self.model.toolbars:
    #         if t.visible == True:
    #             this_tool = t
    #             screen.sub(t)
    #             for c in self.model.control_enables:
    #                 screen.sub(c)
    #             for e in self.model.transition_conditions:
    #                 screen.sub(e)
    #                 print ("Made a transition")
    #             print ("Made a toolbar!")
    #         else:
    #             for c in self.model.control_enables:
    #                 c.destroy()
    #             for e in self.model.transition_conditions:
    #                 e.destroy()
    #             print "No toolbar!"

        
    def update(self, screen):

        for b in self.model.buttons:
            screen.sub(b)
            print b.rect
            print("Made a button!")

        for droppy in self.model.states:
            this_droppy = droppy
            screen.sub(this_droppy)
            print ("Made a drop zone!")


        # for t in self.model.toolbars:
        #     if t.visible == True:
        #         this_tool = t
        #         screen.sub(t)
        #         for c in self.model.control_enables:
        #             screen.sub(c)
        #         for e in self.model.transition_conditions:
        #             screen.sub(e)
        #             print ("Made a transition")
        #         print ("Made a toolbar!")
        #     else:
        #         print "No toolbar!"

        for t in self.model.toolbars:
            screen.sub(t)
            print ("Made a toolbar!")
        

        for t in self.model.transition_conditions:
            this_cond = t
            screen.sub(this_cond)
            print ("Made a transition condition!")

        for t in self.model.transitions:
            this_trans = t
            screen.sub(this_trans)
            print ("Made a transition!")

        

        
              
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
    model.make_Toolbar("tool1", rect, ["trans1", "trans2", "trans3", "trans4"], [])
    
    model.make_Button("button", pygame.Rect(600,0,100,100))   
    
    
    #Just to test if materials work
    # for i in range(0,4):    
    #     model.make_control_enables("mat"+`i`, pygame.Rect(200, i*75, 50, 50))    

    view.update(screen)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
			raise SystemExit

        screen.process(events)
        #view.update(screen)
        screen.render()
        pygame.display.flip()
        time.sleep(0.001)