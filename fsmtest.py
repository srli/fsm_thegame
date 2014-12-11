# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 22:18:51 2014

@author: sophie
"""
import time

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
            i += 1
                 
#inits (name, current_index, transition_check, transition_conditions, next_states, enables)
TOO_HOT = State("TOO_HOT", 0, "<", [50], [1], [0])
TOO_COLD = State("TOO_COLD", 1, ">", [50], [0], [1])
#JUST_RIGHT = State("JUST_RIGHT", 2, "range", [60, 40],[0],[0])

states = [TOO_HOT, TOO_COLD]
state_pointer = 0
current_state = states[state_pointer]

i = 0
heater = 0
temperature = 78

while i < 50:
    current_state = states[state_pointer]
    heater = current_state.enables[0]
    print heater
    if heater:
        temperature += 3
    elif heater == 0:
        temperature -= 3
    state_pointer = current_state.check_transition(temperature)
    print "temperature is ", temperature
    print current_state.name
    i += 1
    time.sleep(1)