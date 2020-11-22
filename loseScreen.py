#makes losing screen

import pyaudio
from pygame.locals import *
import pygame
import numpy as np

#class base structure from
#https://stackoverflow.com/questions/19936347/pygame-window-and-sprite-class-python

class LoseScreen(object):
    #make losing screen
    def __init__(self, width, height, score):
        self.score = score
        self.width = width
        self.height = height
        self.gameRunning = True
        self.running = False
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.margin = 125
        pygame.init()

    def makeGameMode(self, bgColor, lineColor):
        #make "return" button
        color = (168, 255, 255)
        pygame.draw.rect(self.screen, bgColor,(0,0,self.width,self.height))
        pygame.draw.line(self.screen, lineColor, (0,self.height - 75),
         (self.width, self.height - 75))
        font = pygame.font.SysFont("ammericantypewriterttc", 25)
        
        
        text0 = font.render(f"Return", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width//2 - w//2 - 10, 
        self.height//2 - h//2))
        return (x,y,w,h)

    def createTitle(self):
        #make "You Lost!"
        color = (168, 255, 255)
        font2 = pygame.font.SysFont("ammericantypewriterttc", 60)
        text1 = font2.render(f"You", True, color)
        (a, b, w1, h1) = text1.get_rect()
        self.screen.blit(text1, (self.width//2 - w1 - 10, self.height//4))
        text2 = font2.render(f"lost!", True, color)
        self.screen.blit(text2, (self.width//2 + 10, self.height//4))

    def createScreen(self):
        #main function
        bgColor = (103, 125, 60)
        
        lineColor = (0,125,144)
        (x,y,w,h) = self.makeGameMode(bgColor, lineColor)
        

        (x0, y0, x1, y1) = (self.width//2 - w//2, 
        self.height//2 - h//2 - 10,
        self.width//2 + w//2 + 10, self.height//2 + h//2 + 10)
        self.createTitle()
        pygame.display.update()
        result = self.waitForKeyPress((x0, y0, x1, y1))
        return result
    
    def waitForKeyPress(self, startCoordinates):
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN: 
                    (x,y) = pygame.mouse.get_pos()
                    if self.intersect(startCoordinates, (x,y)):
                        return 1
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 0
        return 0
        
    def intersect(self, bound1, position):
        #check intersection of point and object
        (a0, b0, a1, b1) = bound1
        (x0, y0) = position
        if ((a0<x0) and (a1 > x0) and (b0 < y0) and (b1 > y0)):
            return True
        return False