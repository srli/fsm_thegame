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

grid = [["SSSXEEXX",
        "SSSXEEXX",
        "TTTXXXXX",
        "TTTXXXXX"]] #each block has width 100px, height 75


class Level:
    def __init__ (self, states, transitions, enables):
       # self.background = background
        self.states = states
        self.enables = enables 
        self.transitions = transitions 

 #name, transition_check_type, value, rect)

#intro = Level(["hallo", "deathofworld.jpg", "help"], [], [], [])
#act1 = Level(["day", "night"], ["hot", "cold"], ["heater on", "heater off"], [1,2,3])
#act2 = Level(["day", "night"], ["hot", "cold"], ["heater on", "heater off"], [1,2,3])


test = Level(["too hot", "too cold"], [("on to off",">",70), ("off to on", "<", 40)], ["heater on", "heater off"])

all_levels = [test]
print all_levels[0].states