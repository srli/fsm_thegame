# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 20:51:39 2014

@author: sophie
"""

import pygame, time
from world import *
import planes

class Drag(planes.Plane):
    def __init__(self, name, rect, draggable=True, grab=True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        self.name = name
        self.image.fill((255, 0, 0))
        self.Xpos = rect.x
        self.Ypos = rect.y
        self.height = rect.height
        self.width = rect.width

    def clicked(self, button_name):
        self.image.fill((255,0,0))

class Drop(planes.Plane):
    def __init__(self, name, rect, draggable=False, grab=True):
        planes.Plane.__init__(self, name, rect, draggable, grab)
        
        self.name = name
        #print ("made drop Zone with x position", self.Xpos)

        self.Xpos = rect.x
        self.Ypos = rect.y
        self.height = rect.height
        self.width = rect.width
        
        self.image.fill((0,0,255))
    
    def dropped_upon(self, plane, coordinates):
        planes.Plane.dropped_upon(self, plane, coordinates)
        plane.moving = False
        self.update_drag(plane, coordinates)

    def update_drag(self,plane, coordinates):
        """ 
        updates the model position for a drag object or drag object child whenever it's dropped on a drop object or drop object child
        """
        plane.Xpos = coordinates[0]
        plane.Ypos = coordinates[1]
        print(plane.name, plane.Xpos, plane.Ypos)

 
class Transition(Drag):
    """
    Transition, a subclass of Drag, which has an attribute of transition conditions
    """
    def __init__(self, name, rect, transition_conditions=[]):
        Drag.__init__(self, name, rect, draggable=True, grab=True)
        self.transition_conditions = transition_conditions

    def is_transitioned(self):
        """
            Evaluates transition condition and returns a boolean
        """
        pass


class Drop_Display(planes.Display):
    def dropped_upon(self, plane, coordinates):
        if isinstance(plane, Drop):
            planes.Display.dropped_upon(self, plane, (plane.rect.centerx, plane.rect.centery))
        print(coordinates)


class State(Drop):
    """
    State, a subclass of Drop_zone which has control enables and one or more transition objects
    """
    def __init__(self, name, rect, transitions=None, control_signals=[], next_state=None):
        Drop.__init__(self, name, rect, draggable=False, grab=True)
        self.transitions = transitions
        self.state_control_signals = control_signals

class State:
    def __init__ (self, name, current_index, transition_check, transition_conditions, next_states, enables):
        self.name = name
        self.current_index = current_index
        self.transition_check = transition_check
        self.transition_conditions = transition_conditions
        self.next_states = next_states
        self.enables = enables
        
    def check_transition(self, transition):
        i = 0
        while i < len(self.transition_conditions):
            if self.transition_check == ">":
                if transition > self.transition_conditions[i]:
                     return self.next_states[i]
                else:
                    return self.current_index
            elif self.transition_check == "<":
                if transition < self.transition_conditions[i]:
                     return self.next_states[i]
                else:
                    return self.current_index
            elif self.transition_check == "range":
                if transition > self.transition_conditions[i] and transition < self.transition_conditions[i+1]:
                    return self.next_states[i]
                else:
                    return self.current_index
            else:
                return self.current_index
                print "Check transition condition of state", self.name
            i += 1
            
class Model:      #game encoded in model, view, controller format
    def __init__(self):
        self.level = 0
        self.state_pointer = 0
        self.states = []
        self.current_state = self.states(self.state_pointer)
        self.temperature = 70
        self.build_world(self.level)
    
    def build_world(self, level_num):
        i = 0
        for level in world.world[level_num]:
            states_in_level = level.states
            while i < len(states_in_level):
                state = states_in_level[i]
                self.states.append(State(state.name, 0, [0],[0],[0]))
    
    def update(self, transition = 0):
        heater = self.current_state.enables[0]
        if heater:
            self.temperature += 3
        elif heater == 0:
            self.temperature -= 3
        self.state_pointer = self.current_state.check_transition(self.temperature)
        print "temperature is ", self.temperature
        print self.current_state.name
        time.sleep(1)


if __name__ == "__main__":   
    pygame.init()   #initializes our game
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    model = Model()
    view = PyGameWindowView(model,screen)    
    
    running = True

    while running:
        model.update()
        view.draw()
        time.sleep(0.001)
    
    main()
    
    
    
    