# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 22:18:51 2014

@author: sophie
"""
import pygame, time
from world import *

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
    
    
    
    