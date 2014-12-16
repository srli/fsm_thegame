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
        
        #self.backgrounds = [] #FILL THIS IN LATER
        #self.current_state = states[state_pointer]
        #self.current_background = backgrounds[background_pointer]
        
        self.build_world(0) #builds first screen immediately
        
    def build_world(self, level_num):
        """Looks at the objects imported from the world python script and builds
        """
        current_level = all_levels[level_num]
        self.states_names = current_level.states
        print self.states_names
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
                if col == "S":  #if the level has a W encoded, build a wall there
                    print "is in S"
                    if i < len(self.states_names):
                        self.states.append(State(self.states_names[i], i, pygame.Rect(x,y,90,70)))
                        print "appended state"
                        i += 1
                elif col == "T":
                    if j < len(self.transitions_names):
                        self.transitions.append(Transition(self.transitions_names[j][0], 
                                                           self.transitions_names[j][1],self.transitions_names[j][2], pygame.Rect(x,y,90,70)))
                        j += 1
                elif col == "E":
                    if k < len(self.enables_names):
                        self.enables.append(Enable(self.enables_names[k], pygame.Rect(x,y,90,70)))
                        k += 1
                x += 100 #Traverses each column in the world file
            y += 75 #Goes to the next row
            x = 0 #Restarts at the first column
   
    def update(self, transition = 0):
        """updates based on inputs from the controller"""
        self.state_pointer = self.current_state.check_transition(self.transition)
        
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
        for state in self.model.states: #Draws each wall block
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), state.rect)
        for transition in self.model.transitions: #Draws each wall block
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), transition.rect)
        for enable in self.model.enables: #Draws each wall block
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), enable.rect)
            
        pygame.display.update() #Pygame call to update full display


class Controller:
    """ Manipulate game state based on keyboard input, the controller part of our model, view, controller"""
    def __init__(self, model):
        """ Initializes controller to deal with keyboard input """
        self.model = model
        self.mouse_held = False
        self.is_dragging = False
        self.mouseX = 0
        self.mouseY = 0
            
    def handle_pygame_mouse(self, event):
        """Takes position of mouse click and passes coordinates through interactibility check and applies
        proper reactions"""
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN: #when key is pressed we look at position and respond
            self.mouse_held = True
        if event.type == MOUSEBUTTONUP: #when key is pressed we look at position and respond
             self.mouse_held = False
             self.is_dragging = False
        self.update(event)
    
    def update(self, model):
        all_rects = self.model.states + self.model.transitions + self.model.enables
        for element in all_rects:
            if element.rect.collidepoint((self.mouseX, self.mouseY)) and self.mouse_held:
                element.is_dragging = True
            if element.is_dragging:
                element.rect.y = self.mouseY - element.rect.size[1] // 2
                element.rect.x = self.mouseX - element.rect.size[0] // 2

      
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

        #model.update()
        view.draw()
        clock.tick(60)