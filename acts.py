# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 15:40:14 2014

@author: sophie
"""

import pygame, random, math, time
from pygame.locals import *
from world import *
from menu_test import *
         
class State:
    def __init__ (self, name, transition_conditions, next_states, enables):
        self.name = name
        self.transition = False
        self.transition_conditions = transition_conditions
        self.next_states = next_states
        self.enables = enables
        
    def check_transition(self, transition):
         for i in transition_conditions:
             if transition > transition_conditions[i]:
                 return next_states[i]
                 
         
class Model:      #game encoded in model, view, controller format
    def __init__(self):
        self.level = 0
        self.state_pointer = 0
        self.build_world(0) #builds first screen immediately
        self.state_names = []
        self.states = []
        self.transition_conditions = []
        self.backgrounds = []
        self.current_state = states[state_pointer]
        
    def build_world(self, level_num):
        """Looks at the objects imported from the world python script and builds
        """
        current_level = world.world[level_num]
        self.state_names = current_level.states
        self.backgrounds = current_level.backgrounds
    
    def build_transitions(self):
        pass
    
    
    def build_states(self):
        for i in self.state_names:
            temp_state = State(self.state_names[i], self.transition_conditions[i])
            states.append(temp_state)
    
    def update(self, transition = 0):
        """updates based on inputs from the controller"""
        self.state_pointer = self.current_state.check_transition(self.transition)
        
class PyGameWindowView:
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
        pygame.display.update() #Pygame call to update full display


class PyGameKeyboardController:
    """ Manipulate game state based on keyboard input, the controller part of our model, view, controller"""
    def __init__(self, model):
        """ Initializes controller to deal with keyboard input """
        self.model = model
            
    def handle_pygame_mouse(self, event):
        """Takes position of mouse click and passes coordinates through interactibility check and applies
        proper reactions"""
        x, y = event.pos #Sets click position
        
        
        
if __name__ == '__main__':
    pygame.init()   #initializes our game
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    model = Model()
    view = PyGameWindowView(model,screen)
    controller = PyGameKeyboardController(model)
    
#    music = pygame.mixer.music.load("StillAlive.mp3")   #loads our background music and plays it 
#    pygame.mixer.music.play()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN: #when key is pressed we look at position and respond
                controller.handle_pygame_mouse(event)
        model.update()
        view.draw()
        time.sleep(0.001)