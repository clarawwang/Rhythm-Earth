#makes winning screen

import pyaudio
from pygame.locals import *
import pygame
import numpy as np
from highScoreTry import *

#class base structure from
#https://stackoverflow.com/questions/19936347/pygame-window-and-sprite-class-python

class WinScreen(object):
    #make win screen class
    def __init__(self, score, menuOpt, perR, perC, perT):
        self.score = score
        self.width = 800
        self.height = 500
        self.gameRunning = True
        self.running = False
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.margin = 125
        self.menuOpt = menuOpt
        self.perR = perR
        self.perC = perC
        self.perT = perT
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
        self.screen.blit(text0, (self.width//2 - w//2, 
        self.height//2 - h//2))
        return (x,y,w,h)
    
    def makeStats(self, bgColor, lineColor):
        #write player stats on screen
        color = (168, 255, 255)
        font = pygame.font.SysFont("ammericantypewriterttc", 25)
        (a, b) = self.perR
        (c,d) = self.perC
        (e,f) = self.perT 
        text0 = font.render(f"Recycling: {a}/{b}", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width//2 - w//2, 
        self.height//2 - h//2 - 60))
        text1 = font.render(f"Composting: {c}/{d}", True, color)
        (x1, y1, w1, h1) = text1.get_rect()
        self.screen.blit(text1, (self.width//2 - w1//2 , 
        self.height//2 - h1//2- 45))
        text2 = font.render(f"Trash: {e}/{f}", True, color)
        (x2, y2, w2, h2) = text2.get_rect()
        self.screen.blit(text2, (self.width//2 - w2//2 , 
        self.height//2 - h2//2- 30))
        

    def createTitle(self):
        #write score
        color = (168, 255, 255)
        font2 = pygame.font.SysFont("ammericantypewriterttc", 60)
        text1 = font2.render(f"Score :", True, color)
        (a, b, w1, h1) = text1.get_rect()
        self.screen.blit(text1, (self.width//2 - w1 - 10, self.height//4))
        text2 = font2.render(f"{self.score}", True, color)
        self.screen.blit(text2, (self.width//2 + 10, self.height//4))

    def createScreen(self):
        #general function
        bgColor = (103, 125, 60)
        
        lineColor = (0,125,144)
        (x,y,w,h) = self.makeGameMode(bgColor, lineColor)
        

        (x0, y0, x1, y1) = (self.width//2 - w//2, 
        self.height//2 - h//2 - 10,
        self.width//2 + w//2 + 10, self.height//2 + h//2 + 10)
        self.createTitle()
        if self.menuOpt == 1:
            addHighScore(self.score)
            self.makeStats(bgColor, lineColor)
        pygame.display.update()
        result = self.waitForKeyPress((x0, y0, x1, y1))
        return result
    
    def waitForKeyPress(self, startCoordinates):
        #see if user wants to play again
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
        #check intersect point and object
        (a0, b0, a1, b1) = bound1
        (x0, y0) = position
        if ((a0<x0) and (a1 > x0) and (b0 < y0) and (b1 > y0)):
            return True
        return False