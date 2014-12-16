# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 15:40:14 2014

@author: sophie
"""

import pygame, random, math, time
from pygame.locals import *
from world import *
         
class State:
    def __init__ (self,  name, current_index, rect): #, transition_check, transition_conditions, next_states, enables):
        self.name = name
        self.current_index = current_index
        self.rect = rect
        self.is_dragging = False
        self.transition_check = []
        self.transition_conditions = []
        self.next_states = []
        self.enables = []
        
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
            
class Transition:
    def __init__(self, name, transition_check_type, value, rect):
        self.name = name
        self.transition_check_type = transition_check_type
        self.value = value
        self.rect = rect
        self.is_dragging = False
    
class Enable:
    def __init__(self, name, rect):
        self.name = name
        self.rect = rect
        self.is_dragging = False
 

       
class State_drop:
    def __init__(self, name, rect):
        self.name = name
        self.rect = rect
        
class Transition_drop:
    def __init__(self, name, rect):
        self.name = name
        self.rect = rect
        
class Enable_drop:
    def __init__(self, name, rect):
        self.name = name
        self.rect = rect
        
class Model:      #game encoded in model, view, controller format
    def __init__(self):
        self.level = 0
        self.state_pointer = 0
        self.background_pointer = 0       
       
        self.states_names = []
        self.states = []
        self.transitions_names = []
        self.transitions = []
        self.enables_names = []
        self.enables = []
        
        self.states_drop_zones = []
        self.transitions_drop_zones = []
        self.enables_drop_zones = []
        
        self.start_button = pygame.Rect((550, 500), (50,30))
        self.beginning_simulation = False
        #self.backgrounds = [] #FILL THIS IN LATER
        #self.current_state = states[state_pointer]
        #self.current_background = backgrounds[background_pointer]
        
        self.build_drag_objects(0) #builds first screen immediately
        self.build_drop_zones(0)
        
    def build_drag_objects(self, level_num):
        """Looks at the objects imported from the world python script and builds
        """
        current_level = all_levels[level_num]
        self.states_names = current_level.states
        #print self.states_names
        #self.backgrounds = current_level.backgrounds
        self.transitions_names = current_level.transitions
        self.enables_names = current_level.enables
        
        layout = ["SSSXEEXX",
                  "SSSXEEXX",
                  "TTTXXXXX",
                  "TTTXXXXX"] #each block has width 100px, height 75
        x = 0
        y = 500
        i = j = k = 0
        for row in layout:
            for col in row:
                if col == "S":
                    if i < len(self.states_names):
                        self.states.append(State(self.states_names[i], i, pygame.Rect(x,y,45,20)))
                        i += 1
                elif col == "T":
                    if j < len(self.transitions_names):
                        self.transitions.append(Transition(self.transitions_names[j][0], 
                                                           self.transitions_names[j][1],self.transitions_names[j][2], pygame.Rect(x,y,45,20)))
                        j += 1
                elif col == "E":
                    if k < len(self.enables_names):
                        self.enables.append(Enable(self.enables_names[k], pygame.Rect(x,y,45,20)))
                        k += 1
                x += 50 #Traverses each column in the world file
            y += 30 #Goes to the next row
            x = 0 #Restarts at the first column
    
    
    def build_drop_zones(self,level_num):
        current_level = all_levels[level_num]
        self.states_names = current_level.states
        self.transitions_names = current_level.transitions
        self.enables_names = current_level.enables        
        
        layout = ["XXTXXTXXTXXTXXTXX",
                  "XXXXXXXXXXXXXXXXX",
                  "SXTXSXTXSXTXSXTXS",
                  "EXXXEXXXEXXXEXXXE"]
                  
        x = 50
        y = 0
        i = j = k = 0
        for row in layout:
            for col in row:
                if col == "S":
                    if i < len(self.states_names):
                        self.states_drop_zones.append(State(self.states_names[i], i, pygame.Rect(x,y,45,20)))
                        i += 1
                elif col == "T":
                    if j < len(self.transitions_names):
                        self.transitions_drop_zones.append(Transition(self.transitions_names[j][0], 
                                                           self.transitions_names[j][1],self.transitions_names[j][2], pygame.Rect(x,y,45,20)))
                        j += 1
                elif col == "E":
                    if k < len(self.enables_names):
                        self.enables_drop_zones.append(Enable(self.enables_names[k], pygame.Rect(x,y,45,20)))
                        k += 1
                x += x_width #Traverses each column in the world file
            y += y_width #Goes to the next row
            x = 50 #Restarts at the first column

    def link_states(self):
        pass
   
   
   
    def update(self, transition = 0):
        """updates based on inputs from the controller"""
        if self.beginning_simulation:
            self.link_states()
        
class View:
    """ Draws our game in a Pygame window, the view part of our model, view, controller"""
    def __init__(self,model,screen):
        """ Initializes view when the game starts """
        self.model = model
        self.screen = screen
    
    def draw(self):
        """Draws updated view every 0.001 seconds, or as defined by sleep at end of main loop
        Does not do any updating on its own, takes model objects and displays        
        """
        self.screen.fill(pygame.Color(0,0,0)) #Background
        pygame.draw.line(self.screen, (255,255,255), (0,450), (800,450))
        pygame.draw.line(self.screen, (255,255,255), (50,0), (50,800))
        pygame.draw.line(self.screen, (255,255,255), (750,0), (750,800))
        
        for state in self.model.states: #Draws each wall block
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), state.rect)
        for transition in self.model.transitions: #Draws each wall block
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), transition.rect)
        for enable in self.model.enables: #Draws each wall block
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), enable.rect)
        pygame.draw.rect(screen, pygame.Color(120,120,120), pygame.Rect((500, 450), (300, 450)))
        pygame.draw.rect(screen, pygame.Color(244,244,120), self.model.start_button)
        pygame.display.update() #Pygame call to update full display


class Controller:
    """ Manipulate game state based on keyboard input, the controller part of our model, view, controller"""
    def __init__(self, model):
        """ Initializes controller to deal with keyboard input """
        self.model = model
        self.mouse_held = False
        self.drag_index = 0   
        self.all_rects = self.model.states + self.model.transitions + self.model.enables
            
    def handle_pygame_mouse(self, event):
        """Takes position of mouse click and passes coordinates through interactibility check and applies
        proper reactions"""
        if event.type == MOUSEBUTTONDOWN: #when key is pressed we look at position and respond
            self.mouse_held = True
            self.check_buttons()
        if event.type == MOUSEBUTTONUP: #when key is pressed we look at position and respond
             self.mouse_held = False
             self.un_drag()
    
    def check_buttons(self):
        if self.model.start_button.collidepoint((mouseX, mouseY)):
            print "starting!"              
    
    def un_drag(self):        
        element = self.all_rects[self.drag_index]
        element.is_dragging = False
  
    def update(self):
        for element in self.all_rects:
            if element.rect.collidepoint((mouseX, mouseY)) and self.mouse_held:
                element.is_dragging = True
                print "dragging", element.name
                self.drag_index = self.all_rects.index(element)
                print self.drag_index
            if element.is_dragging:
                print "is dragging", element.name
                element.rect.y = mouseY# - element.rect.size[1] // 2
                element.rect.x = mouseX# - element.rect.size[0] // 2

      
if __name__ == '__main__':
    pygame.init()   #initializes our game
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    model = Model()
    view = View(model,screen)
    controller = Controller(model)
    
#    music = pygame.mixer.music.load("StillAlive.mp3")   #loads our background music and plays it 
#    pygame.mixer.music.play()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP: #when key is pressed we look at position and respond
                controller.handle_pygame_mouse(event)
        mouseX, mouseY = pygame.mouse.get_pos()
        controller.update()
        model.update()
        view.draw()
        clock.tick(60)