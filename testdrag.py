import pygame
import os


class ImageClass:
   def __init__(self):
      self.size = (50, 250)
      self.image = pygame.Surface(self.size).convert_alpha()
      self.image.fill((255,255,0))
      #self.mask = pygame.mask.from_surface(self.image)
      self.rect = self.image.get_rect()
      
      
class Control:
   def __init__(self):
      pygame.init()
      self.screensize = (600,600)
      self.screen = pygame.display.set_mode(self.screensize)
      self.clock = pygame.time.Clock()
      self.mouseX = 0
      self.mouseY = 0
      self.keys = None
      self.mouse_keys = (0,0,0)
      self.mouse_held = False
      self.is_dragging = False
      
      self.images = ImageClass()

   def update(self):
      self.screen.fill((150,150,150))
      if self.images.rect.collidepoint((self.mouseX, self.mouseY)) and self.mouse_held:
         self.is_dragging = True
      if self.is_dragging: #keep moving box if mouse is still holding but movees too fast
         self.images.rect[1] = self.mouseY - self.images.size[1] // 2
         self.images.rect[0] = self.mouseX - self.images.size[0] // 2

      self.screen.blit(self.images.image, (self.images.rect[0],self.images.rect[1]))
      
   def main(self):
      run = True
      while run:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
               self.mouse_held = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
               self.mouse_held = False
               self.is_dragging = False

         self.keys = pygame.key.get_pressed()
         self.mouseX, self.mouseY = pygame.mouse.get_pos()
         self.mouse_keys = pygame.mouse.get_pressed()

         self.update()
         pygame.display.flip()
         self.clock.tick(60)
         

controller = Control()
controller.main()