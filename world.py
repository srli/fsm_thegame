# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 15:53:58 2014

@author: sophie
"""

"""
background image
states
    -control signals
    -transitions
"""

#inits (name, current_index, transition_check, transition_conditions, next_states, enables)
    
class Level:
    def __init__ (self, background, states, enables, transitions):
        self.background = background
        self.states = states
        self.enables = enables 
        self.transitions = transitions      

intro = Level(["hallo", "deathofworld.jpg", "help"], [], [], [])
act1 = Level(["day", "night"], ["hot", "cold"], ["heater on", "heater off"], [1,2,3])
act2 = Level(["day", "night"], ["hot", "cold"], ["heater on", "heater off"], [1,2,3])

world = [intro, act1, act2]