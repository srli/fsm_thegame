#!/usr/bin/python3

"""Square clicking using planes

   Copyright 2010 Florian Berger <fberger@florian-berger.de>

   Based on a pure PyGame implementation
"""

import pygame, time
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
        plane.Xpos = coordinates[0]+self.Xpos
        plane.Ypos = coordinates[1]+self.Ypos
        # print(plane.name, plane.Xpos, plane.Ypos)


class State(Drop):
    """
    State, a subclass of Drop_zone which has control enables and one or more transition objects
    """
    def __init__(self, name, rect, transitions=None, control_signals=[], next_state=None):
        Drop.__init__(self, name, rect, draggable=False, grab=True)
        self.transitions = transitions
        self.state_control_signals = control_signals

 
class Transition(Drag):
    """
    Transition, a subclass of Drag, which has an attribute of transition conditions
    """
    def __init__(self, name, rect, transition_conditions=[]):
        Drag.__init__(self, name, rect, draggable=True, grab=True)
        self.conditions = transition_conditions

    def is_transitioned(self):
        """
            Evaluates transition condition and returns a boolean
        """
        pass


class Drop_Display(planes.Display):
    def dropped_upon(self, plane, coordinates):
        if isinstance(plane, Drop):
            planes.Display.dropped_upon(self, plane, (plane.rect.centerx, plane.rect.centery))
        # print(coordinates)

class Model():
    def __init__(self, current_state=None):
        self.all_control_signals = []
        self.states = []
        self.current_state = current_state

    def make_control_signal(self, name, rect):
        self.all_control_signals.append(Drag(name, rect))
    
    def make_state(self, name, rect):
        self.states.append(State(name, rect))

    def update_states(self):
        for s in self.states:
            # print s.name
            for signal in self.all_control_signals:
                if (s.Xpos <= signal.Xpos <= s.Xpos+s.width) or (s.Xpos <= signal.Xpos+signal.width <= s.Xpos+s.width):
                    print(signal.Xpos, signal.Ypos)
                    if (s.Ypos <= signal.Ypos <= s.Ypos+s.height) or (s.Ypos <= signal.Ypos+signal.height <= s.Ypos+height):
                        if signal.name not in s.state_control_signals:
                            s.state_control_signals.append(signal.name)
                    else:
                        if signal.name in s.control_signals:
                            s.state_control_signals.remove(signal.name)
            print(s.name, s.state_control_signals)

class View():
    def __init__(self, model, screen): #View contains model and screen
        self.model = model
        self.screen = screen
        
    def update(self, screen):        
        for state in self.model.states:
            this_droppy = state
            screen.sub(this_droppy)
            # print ("Made a drop zone!")     
        for control in self.model.all_control_signals:
            this_draggy = control
            screen.sub(this_draggy)                       
            # print("Made a draggable")
        
            
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
    model.make_state("drop1", pygame.Rect(0, 0, 100, 100))
    model.make_state("drop2", pygame.Rect(700,400, 100,100))    
    
    #Just to test if materials work
    for i in range(0,4):    
        model.make_control_signal("mat"+`i`, pygame.Rect(200, i*75, 50, 50))    

    view.update(screen)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        model.update_states()
        screen.process(events)
        screen.render()
        pygame.display.flip()
        time.sleep(0.001)