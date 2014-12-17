# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 15:40:14 2014

@author: sophie
"""

import pygame, random, math, time
from pygame.locals import *
from world import *
import time
         
class State:
    def __init__ (self,  name, rect): #, transition_check, transition_conditions, next_states, enables):
        self.name = name
        self.current_index = 0
        self.rect = rect
        self.glow = False
        self.is_dragging = False
        self.transition_check = []
        self.transition_conditions = []
        self.next_states = []
        self.enables = []
        
    def check_transition(self, transition):
        i = 0
        while i < len(self.transition_conditions):
            print "transistions of", self.name, " are ", self.transition_check[i]
            print "next states are", self.next_states[i]
            if self.transition_check[i] == "x":
                return self.current_index
            elif self.transition_check[i] == ">":
                if transition > self.transition_conditions[i]:
                    return self.next_states[i]
                else:
                    return self.current_index
            elif self.transition_check[i] == "<":
                if transition < self.transition_conditions[i]:
                    return self.next_states[i]
                else:
                    return self.current_index
            elif self.transition_check[i] == "range":
                if transition > self.transition_conditions[i] and transition < self.transition_conditions[i+1]:
                    return self.next_states[i]
                else:
                    return self.current_index
            else:
                print "Check transition condition of state", self.name
                return self.current_index
            i += 1
        return self.current_index
            
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
    def __init__(self, name, rect, next_state):
        self.name = name
        self.rect = rect
        self.next_state = next_state
        
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
        
        self.start_button = pygame.Rect((550, 475), (50,30))
        self.end_button = pygame.Rect((700, 475), (50,30))
        
        self.begin_linking = False
        self.begin_simulation = False
        
        self.condition_name = "none"
        self.init_conditions = []
        self.condition = 0        

        self.build_drag_objects(self.level) #builds first screen immediately
        self.build_drop_zones(self.level)
        
        self.current_state = None
        #self.current_state = self.states[self.state_pointer]

        self.win_condition = False
        self.start = 0

    
    def reset(self):
        """ resets lists for the next level"""
        self.states_names = []
        self.states = []
        self.transitions_names = []
        self.transitions = []
        self.enables_names = []
        self.enables = []
        
        self.states_drop_zones = []
        self.transitions_drop_zones = []
        self.enables_drop_zones = []
        self.win_condition = False
        self.start = 0


    def build_drag_objects(self, level_num):
        """Looks at the objects imported from the world python script and builds
        """
        current_level = all_levels[level_num][0]
        self.states_names = current_level.states
        self.condition_name = all_levels[level_num][1].name
        self.init_conditions = all_levels[level_num][1].initial_values
        #print self.states_names
        #self.backgrounds = current_level.backgrounds
        self.transitions_names = current_level.transitions
        self.enables_names = current_level.enables
        
        layout = ["SSSXEEXX",
                  "SSSXEEXX",
                  "TTTXEEXX",
                  "TTTXXXXX"] #each block has width 100px, height 75                
        x = 50
        y = 500
        i = j = k = 0
        for row in layout:
            for col in row:
                if col == "S":
                    if i < len(self.states_names):
                        self.states.append(State(self.states_names[i],pygame.Rect(x,y, 60,60)))
                        i += 1
                elif col == "T":
                    if j < len(self.transitions_names):             
                        self.transitions.append(Transition(self.transitions_names[j][0], 
                                                           self.transitions_names[j][1],self.transitions_names[j][2], pygame.Rect(x,y, 60,60)))
                        j += 1
                elif col == "E":
                    if k < len(self.enables_names):
                        self.enables.append(Enable(self.enables_names[k], pygame.Rect(x,y, 60,60)))
                        k += 1
                x += 70 #Traverses each column in the world file
            y += 70 #Goes to the next row
            x = 50 #Restarts at the first column
    
    
    def build_drop_zones(self,level_num):
        toggle = False
        next_state_number = 1
              
        current_level = all_levels[level_num][0]
        self.states_names = current_level.states
        self.transitions_names = current_level.transitions
        self.enables_names = current_level.enables        
         
        layout = ["XSEX",
                  "XXXX",
                  "TTXX",
                  "XXXX",
                  "XSEX",
                  "XXXX",
                  "TTXT",
                  "XXXX",
                  "XSEX",
                  "XXXX",
                  "TTXX",
                  "XXXX",
                  "XSEX"]

               
        x_width = 700/(3*len(self.states_names))
        x = 50
        y = 50
        i = j = k = 0
        for col in layout:
            for row in col:
                if row == "S":
                    if i < len(self.states_names):
                        self.states_drop_zones.append(State_drop("state"+str(i), pygame.Rect(x,y,100,100)))
                        i += 1
                elif row == "T":
                    if j < len(self.transitions_names):
                        if (j == len(self.transitions_names) - 1):
                            print "transition ", str(j), "is 0"
                            next_state_number = 0
                        self.transitions_drop_zones.append(Transition_drop("transition"+str(j), pygame.Rect(x,y,130,70), next_state_number))
                        if not toggle:
                            next_state_number -= 1
                            print "transition ", str(j), "is ", next_state_number
                            toggle = not toggle
                        elif toggle:
                            next_state_number += 2
                            print "transition ", str(j), "is ", next_state_number                            
                            toggle = not toggle
                        j += 1
                
                elif row == "E":
                    if k < len(self.enables_names):
                        self.enables_drop_zones.append(Enable_drop("enable"+str(k), pygame.Rect(x+10,y+10,80,80)))
                        k += 1
                y += 100#Traverses each column in the world file
            y = 50 #Goes to the next row
            x += x_width #Restarts at the first column

#    def init_predef(self, level):
#        """
#        takes in a list of objects that need to move and where they should be placed and moves them there 
#        """
#        from_list = all_levels[level][0].from_list
#        to_list = all_levels[level][0].to_list
#
#        for state in self.states:
#            if state.name in from_list:
#                index = from_list.index(state.name)
#                for state_drop in self.states_drop_zones:
#                    if state_drop.name == to_list[index]:
#                        state.rect.x = state_drop.rect.x + 10
#                        state.rect.y = state_drop.rect.y + 10
#
#        for enable in self.enables:
#            if enable.name in from_list:
#                index = from_list.index(enable.name)
#                for enable_drop in self.enables_drop_zones:
#                    if enable_drop.name == to_list[index]:
#                        enable.rect.x = enable_drop.rect.x + 10
#                        enable.rect.y = enable_drop.rect.y + 10
#
#        for trans in self.transitions:
#            if trans.name in from_list:
#                index = from_list.index(trans.name)
#                for trans_drop in self.transitions_drop_zones:
#                    if trans_drop.name == to_list[index]:
#                        trans.rect.x = trans_drop.rect.x + 10
#                        trans.rect.y = trans_drop.rect.y + 10
    

    def link_states(self):
        print "linking states"
        index = 0
        for state_drop in self.states_drop_zones: #indexes all the states properly
            for state_drag in self.states:
                if state_drop.rect.contains(state_drag.rect):
                    state_drag.current_index = index
                    index += 1 
           
        t_first = self.transitions_drop_zones[0]
        self.transitions_drop_zones.remove(self.transitions_drop_zones[0])

        t_last = self.transitions_drop_zones[-1]
        self.transitions_drop_zones.remove(self.transitions_drop_zones[-1])

        for transition_drag in self.transitions:
            if t_first.rect.contains(transition_drag.rect):
                self.states[0].transition_check.append(transition_drag.transition_check_type)
                self.states[0].transition_conditions.append(transition_drag.value)
                self.states[0].next_states.append(t_first.next_state)
            if t_last.rect.contains(transition_drag.rect):
                self.states[-1].transition_check.append(transition_drag.transition_check_type)
                self.states[-1].transition_conditions.append(transition_drag.value)
                self.states[-1].next_states.append(t_last.next_state)
            
        i = 0
        while i < len(self.transitions_drop_zones): #name, transition check, transition conditions
            transition_drop1 = self.transitions_drop_zones[i]
            for transition_drag in self.transitions:
                if transition_drop1.rect.contains(transition_drag.rect):
                    self.states[i].transition_check.append(transition_drag.transition_check_type)
                    self.states[i].transition_conditions.append(transition_drag.value)
                    self.states[i].next_states.append(transition_drop1.next_state)
            i += 1
        
        j = 0
        while j < len(self.enables_drop_zones):
            enable_drop = self.enables_drop_zones[j]
            for enable_drag in self.enables:
                if enable_drop.rect.contains(enable_drag.rect):
                    self.states[j].enables.append(enable_drag.name)
            j += 1 
        print self.states[0].name, self.states[0].enables, self.states[0].transition_check, self.states[0].transition_conditions   
        self.condition = self.init_conditions[self.states[0].current_index]
   
    def simulation(self):
        print self.state_pointer
        self.current_state = self.states[self.state_pointer]
        for state in self.states:        
            if self.current_state.name == state.name:            
                state.glow = True
            else:
                state.glow = False
        enable = self.current_state.enables[0]
        if "yes" in enable:
            self.condition += 0.1
        elif "no" in enable:
            self.condition -= 0.5
        else:
            self.condition += 0.2
        self.state_pointer = self.current_state.check_transition(self.condition)
        print self.condition_name, " is ", self.condition
        print self.current_state.name

    def update(self):
        """updates based on inputs from the controller"""
        if self.begin_linking:
            self.link_states()
            self.begin_linking = False
            self.begin_simulation = True
            self.start = time.time()
        if self.begin_simulation:
            self.simulation()
            self.check_win_conditions(time.time()-self.start)


    def check_win_conditions(self, time):
        if time > 10:
            if self.level == 1 and 40 <= self.condition <= 70:
                self.win_condition = True
                self.begin_simulation = False
            elif self.level == 2 and self.condition >= 60:
                self.win_condition = True
                self.begin_simulation = False


        
class View:
    """ Draws our game in a Pygame window, the view part of our model, view, controller"""
    def __init__(self,model,screen):
        """ Initializes view when the game starts """
        self.model = model
        self.screen = screen
    
    def create_font(self, rect):
        """
        Changes the font size based on the size of the box we are adding the label to

        """

        if rect == None:
            size = 27

        else:
            size = rect.width/4 -2
        
        return pygame.font.SysFont('Arial', size)


    def draw(self):
        """Draws updated view every 0.001 seconds, or as defined by sleep at end of main loop
        Does not do any updating on its own, takes model objects and displays        
        """
        self.screen.fill(pygame.Color(0,0,0)) #Background
        #self.screen.blit(pygame.image.load("FallT.png"), [0,0])
        pygame.draw.line(self.screen, (255,255,255), (0,450), (800,450))
        pygame.draw.line(self.screen, (255,255,255), (50,0), (50,800))
        pygame.draw.line(self.screen, (255,255,255), (750,0), (750,800))

        pygame.draw.rect(screen, pygame.Color(50,50,50), pygame.Rect((0, 450), (800, 450)))
        pygame.draw.rect(screen, pygame.Color(120,120,120), pygame.Rect((500, 450), (300, 450)))

        for s in range(len(self.model.states_drop_zones)-1):
            now = self.model.states_drop_zones[s]
            next = self.model.states_drop_zones[s+1]

            origin = now.rect.topright
            endx = (now.rect.x + next.rect.x)/2 
            endy = now.rect.y-100

            self.draw_arrow(origin, (endx, endy+40), "end", "up", "right")
            self.draw_arrow((endx+130, endy+40), next.rect.topleft, "end", "down", "right")

            #pygame.draw.line(self.screen, (255, 255, 255), (endx+130, endy+40), next.rect.topleft)
            self.draw_arrow(next.rect.midleft, now.rect.midright, "end", "straight" , "right")
            #pygame.draw.line(self.screen, (255, 255, 255), next.rect.midleft, now.rect.midright)

            if s == 1:
                first = self.model.states_drop_zones[0]
                self.draw_arrow(next.rect.bottomleft, ((next.rect.x + 0.25*(now.rect.x - next.rect.x)), next.rect.y+200), "end", "down", "left")
                #pygame.draw.line(self.screen, (255, 255, 255), next.rect.bottomleft, ((next.rect.x + 0.25*(now.rect.x - next.rect.x)), next.rect.y+200))
                #pygame.draw.line(self.screen, (255, 255, 255), (endx+127, endy), nex
                self.draw_arrow(first.rect.bottomright, ((next.rect.x + 0.25*(first.rect.x - next.rect.x)), next.rect.y+200), "start", "up", "right")
                #pygame.draw.line(self.screen, (255, 255, 255), first.rect.bottomright, ((next.rect.x + 0.25*(first.rect.x - next.rect.x)), next.rect.y+200))


        alldroppys = self.model.states_drop_zones + self.model.enables_drop_zones
        
        for droppy in alldroppys:
            pygame.draw.rect(screen, pygame.Color(120, 120, 120), droppy.rect)
            self.screen.blit(self.create_font(droppy.rect).render(droppy.name, True, (255,255,255)), (droppy.rect.x + 2, droppy.rect.y+0.25*droppy.rect.height))
        
        for droppy in self.model.transitions_drop_zones:
            pygame.draw.rect(screen, pygame.Color(120, 120, 120), droppy.rect)
            self.screen.blit(self.create_font(None).render(droppy.name, True, (255,255,255)), (droppy.rect.x + 2, droppy.rect.y+0.25*droppy.rect.height))
        

        for state in self.model.states: #Draws each wall block
            if state.glow:
                color = pygame.Color(255,0,0)
            else:
                color = pygame.Color(45,131,238)
            pygame.draw.rect(screen, color, state.rect)
            self.screen.blit(self.create_font(state.rect).render(state.name, True, (255,255,255)), (state.rect.x + 2, state.rect.y+0.25*state.rect.height))
        for transition in self.model.transitions: #Draws each wall block
            pygame.draw.rect(screen, pygame.Color(109, 190, 69), transition.rect)
            self.screen.blit(self.create_font(transition.rect).render(transition.name, True, (255,255,255)), (transition.rect.x + 2, transition.rect.y+0.25*transition.rect.height))
        for enable in self.model.enables: #Draws each wall block
            pygame.draw.rect(screen, pygame.Color(238, 45, 45), enable.rect)
            self.screen.blit(self.create_font(enable.rect).render(enable.name, True, (255,255,255)), (enable.rect.x + 2, enable.rect.y+0.25*enable.rect.height))
        # for state in self.model.states:
        #     origin = state.rect.center


        pygame.draw.rect(screen, pygame.Color(120,120,120), pygame.Rect((500, 450), (300, 450)))
        pygame.draw.rect(screen, pygame.Color(120,244,120), self.model.start_button)
        pygame.draw.rect(screen, pygame.Color(244,120,120), self.model.end_button)
        self.draw_console()        
        pygame.display.update() #Pygame call to update full display


    def draw_arrow(self, start, end, begin, facing, dir):
        width = 3
        pygame.draw.line(self.screen, (109, 190, 69), start, end, width)
        if begin == "end":
            if facing == "up":
                pygame.draw.line(self.screen, (109, 190, 69), end, (end[0]-25, end[1]+0), width)
                pygame.draw.line(self.screen, (109, 190, 69), end, (end[0]-5, end[1]+20), width)
            elif facing == "down":
                if dir == "right":
                    pygame.draw.line(self.screen, (109, 190, 69), end, (end[0]-25, end[1]-5), width)
                    pygame.draw.line(self.screen, (109, 190, 69), end, (end[0]+5, end[1]-20), width)
                else:
                    pygame.draw.line(self.screen, (109, 190, 69), end, (end[0]+20, end[1]-15), width)
                    pygame.draw.line(self.screen, (109, 190, 69), end, (end[0]-5, end[1]-25), width)

            else:
                pygame.draw.line(self.screen, (109, 190, 69), end, (end[0]+25, end[1]+13), width)
                pygame.draw.line(self.screen, (109, 190, 69), end, (end[0]+25, end[1]-13), width)

        if begin == "start":
            if facing == "up":
                if dir == "right":
                    pygame.draw.line(self.screen, (109, 190, 69), start, (start[0]+25, start[1]-10), width)
                    pygame.draw.line(self.screen, (109, 190, 69), start, (start[0]+5, start[1]+25), width)
                else:
                    pygame.draw.line(self.screen, (109, 190, 69), start, (start[0]+25, start[1]+5), width)
                    pygame.draw.line(self.screen, (109, 190, 69), start, (start[0]-2, start[1]+20), width)

            elif facing == "down":
                if dir == right:
                    pygame.draw.line(self.screen, (109, 190, 69), start, (start[0]-25, start[1]-5), width)
                    pygame.draw.line(self.screen, (109, 190, 69), start, (start[0]+3, start[1]-20), width)
                else:
                    pygame.draw.line(self.screen, (109, 190, 69), start, (start[0]-25, start[1]-5), width)
                    pygame.draw.line(self.screen, (109, 190, 69), start, (start[0]+3, start[1]-20), width)

            else:
                pygame.draw.line(self.screen, (109, 190, 69), start, (start[0]+25, start[1]+13), width)
                pygame.draw.line(self.screen, (109, 190, 69), start, (start[0]+25, start[1]-13), width)
    

    def draw_introl(self, image):
        """
        creates the screen as an image for the tutorial
        """
        self.screen.blit(pygame.image.load(image), [0,0])
        pygame.display.update()

    def draw_console(self):
        fontt = pygame.font.SysFont('Arial', 20)
        self.screen.blit(fontt.render("Drag elements to their correct spaces", True, (255,255,255)), (50,460))
        #self.screen.blit(fontt.render("Current state is "+str(self.model.current_state.name), True, (255,0,0)), (525,525))        
        self.screen.blit(fontt.render("Current "+str(self.model.condition_name) + " is "+str(self.model.condition), True, (255,255,255)), (525,575))
        
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
            self.model.begin_linking = True            
            print "starting!"
        elif self.model.end_button.collidepoint((mouseX, mouseY)):
            self.model.begin_simulation = False            
            print "ending!"
    
    def un_drag(self):        
        element = self.all_rects[self.drag_index]
        element.is_dragging = False
  
    def update(self):
        for element in self.all_rects:
            if element.rect.collidepoint((mouseX, mouseY)) and self.mouse_held:
                element.is_dragging = True
                #print "dragging", element.name
                self.drag_index = self.all_rects.index(element)
                #print self.drag_index
            if element.is_dragging:
                #print "is dragging", element.name
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
        if model.level == 0:
            backgrounds = ["FallT.png","hope.png", "SM.png", "ACT1_title.png", "Act1_intro_text.png", "StateIntro.png", "ControlIntro.png", "TransitionsIntro.png", "Level1Exp.png", "Level1Exp2.png", "Level1Exp3.png", "Level1Exp4.png"]
            #for b in range(len(backgrounds)):
            b = 0
            while b < len(backgrounds):
                view.draw_introl(backgrounds[b])
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        print "CLICK!"
                        b = b+1
            model.level += 1
        elif model.win_condition:
            model.level += 1
            if model.level == 2:
                backgrounds = ["Level2Trans.png", "Level2Exp.png"]
            b = 0
            while b < len(backgrounds):
                view.draw_introl(backgrounds[b])
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        print "CLICK!"
                        b = b+1
            model.reset()
            model.build_drag_objects(model.level) #builds first screen immediately
            model.build_drop_zones(model.level)
            view = View(model,screen)
            controller = Controller(model)
        
        
        else:
            view.draw()        
        clock.tick(60)
