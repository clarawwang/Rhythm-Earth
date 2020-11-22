#make help screen!

from pygame.locals import *
import pygame
import numpy as np
import string
import os.path
from os import path

class HelpScreen(object):
    #make help screen
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gameRunning = True
        self.running = False
        self.helpList = ["help.txt", "help1.txt", "help2.txt", "help25.txt",
        "help3.txt"]
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.margin = self.width//5
        pygame.init()
        self.bgImage = pygame.image.load("backgroundImage3.png").convert_alpha()
        self.margin = self.width//5
        self.num = 0

    def makeReturn(self, color):
        #make return button
        font = pygame.font.SysFont("ammericantypewriterttc", 45)
        text0 = font.render(f"Return", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width - self.margin - w//2, 
        9*self.height//10 - h//2))
        return (x,y,w,h)

    def writeLines(self, color):
        #write lines from help files
        listScores = []
        #first line take from 
        # https://www.guru99.com/reading-and-writing-files-in-python.html
        if os.path.exists(self.helpList[self.num]):
            f = open(self.helpList[self.num], "r")
            lines = f.readlines()
            for i in range(len(lines)):
                font = pygame.font.SysFont("ammericantypewriterttc", 25)
                text0 = font.render(f"{lines[i][:-1]}", True, color)
                (x, y, w, h) = text0.get_rect()
                self.screen.blit(text0, (self.width//2 - w//2, 
                (i + 1) * (self.height-40)//(len(lines)+1) - h//2 + 40))
        else:
            font = pygame.font.SysFont("ammericantypewriterttc", 25)
            text0 = font.render(f"Try your best!", True, color)
            (x, y, w, h) = text0.get_rect()
            self.screen.blit(text0, (self.width//2 - w//2, 
            self.height//2 - h//2))

    def makeButtons(self, color, h):
        #make buttons for scrolling through pages
        pygame.draw.polygon(self.screen, color, 
        [(self.margin//3, self.height//2), 
        (2*self.margin//3, self.height//2 - h//2),
        (2*self.margin//3, self.height//2 + h//2)])
        pygame.draw.polygon(self.screen, color, 
        [(self.width - self.margin//3, self.height//2), 
        (self.width - 2*self.margin//3, self.height//2 - h//2),
        (self.width - 2*self.margin//3, self.height//2 + h//2)])

    def redraw(self):
        #main drawing fxn
        bgColor = (255, 255, 255)
        pygame.draw.rect(self.screen, bgColor,(0,0,self.width,self.height))
        bgPic = pygame.transform.scale(self.bgImage, (self.width, self.height))
        self.screen.blit(bgPic,(0, 0,self.width//2, self.height//2))


        color = (13, 47, 92)
        colorl = (23, 96, 135)
        colorb = (51, 204, 204)
        (x,y,w,h) = self.makeReturn(color)
        self.writeLines(colorl)
        
        h = 40
        self.makeButtons(colorb, h)

        pygame.display.update()
        return (x,y,w,h)
    
    def createHelpScreen(self):
        #main running fxn
        while True:
        
            (x,y,w,h) = self.redraw()

            (x0, y0, x1, y1) = (self.width - self.margin - w//2 - 10, 
            9 * self.height//10 - h//2 - 10,
            self.width - self.margin + w//2 + 10, 
            9 * self.height//10 + h//2 + 10)

            
            result = self.waitForKeyPress((x0, y0, x1, y1))
            if result == 1:
                return result
            elif result == 2:
                self.redraw()
            elif result == 0:
                return result

    
    def waitForKeyPress(self, startCoordinates):
        #check for key pressed
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN: 
                    (x,y) = pygame.mouse.get_pos()
                    if self.intersect(startCoordinates, (x,y)):
                        return 1
                    if self.hitLeft((x,y)):
                        self.num = (self.num - 1)%(len(self.helpList))
                        return 2
                    if self.hitRight((x,y)):
                        self.num = (self.num + 1)%(len(self.helpList))
                        return 2
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 0
        return 0

    def hitLeft(self, position):
        #check if hit left button
        (x,y) = position
        h= 40
        leftTriangle = (self.margin//3, self.height//2 - h//2,
        2*self.margin//3, self.height//2 + h//2)
        if self.intersect(leftTriangle, (x,y)):
            return True
        return False
    
    def hitRight(self, position):
        #check if hit right button
        h = 40
        (x,y) = position
        rightTriangle = (self.width - 2 * self.margin//3, self.height//2 - h//2,
        self.width - self.margin//3, self.height//2 + h//2)
        if self.intersect(rightTriangle, (x,y)):
            return True
        return False

    def intersect(self, bound1, position):
        #check if point and object intersect
        (a0, b0, a1, b1) = bound1
        (x0, y0) = position
        if ((a0<x0) and (a1 > x0) and (b0 < y0) and (b1 > y0)):
            return True
        return False

