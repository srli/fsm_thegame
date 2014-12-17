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

class Condition:
    def __init__(self, name, initial_values):
        self.name = name
        self.initial_values = initial_values

class Level:
    def __init__ (self, states, transitions, enables, from_list=[], to_list=[]):
       # self.background = background
        self.states = states
        self.enables = enables 
        self.transitions = transitions 
        self.from_list = from_list
        self.to_list = to_list


 #name, transition_check_type, value, rect)

#intro = Level(["hallo", "deathofworld.jpg", "help"], [], [], [])
#act1 = Level(["day", "night"], ["hot", "cold"], ["heater on", "heater off"], [1,2,3])
#act2 = Level(["day", "night"], ["hot", "cold"], ["heater on", "heater off"], [1,2,3])

intro = [Level(["too hot", "too cold"], [("on to off",">",70), ("off to on", "<", 40)], ["heater on", "heater off"], ["too hot", "too cold", "on to off", "off to on", "heater on", "heater off"], ["state0", "state1", "transition0", "transition1", "enable0", "enable1"]),Condition("intro",[0])]
level1 = [Level(["too hot", "too cold"], [("on to off",">",70), ("off to on", "<", 40)], ["heater yes", "heater no"]), Condition("temperature",[80,20])]
level2 = [Level(["peace", "Zerstoert", "reconstruction"],[("dragons appear","<", 50), ("reconstruction begins", ">", 60), ("peace acheived!", ">", 90), ("none1", "x", 100), ("none", "x", 100)], 
                ["workers no", "workers no", "workers yes"]), Condition("HP",[101])]

# two_states = Level(["too hot", "too cold"], [("on to off",">",70), ("off to on", "<", 40)], ["heater on", "heater off"])

all_levels = [intro, level1, level2]
print all_levels[1][1].name

#two_states = [Level(["too hot", "too cold"], [("on to off",">",70), ("off to on", "<", 40)], ["heater on", "heater off"]), Condition("temperature",80)]
# two_states = Level(["too hot", "too cold"], [("on to off",">",70), ("off to on", "<", 40)], ["heater on", "heater off"])

#three_states = Level(["too bright", "just right", "too dim"], ["bright to right"])
