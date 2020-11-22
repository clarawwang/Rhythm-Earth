#makes high score page by reading from high score file

from pygame.locals import *
import pygame
import numpy as np
import string
import os.path
from os import path

class HighScorePage(object):
    #make high score page
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gameRunning = True
        self.running = False
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.margin = 125
        pygame.init()
        self.bgImage = pygame.image.load("backgroundPic.png").convert_alpha()
        self.margin = self.width//5

    def makeReturn(self, color):
        #make "return button"
        font = pygame.font.SysFont("ammericantypewriterttc", 45)
        text0 = font.render(f"Return", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width - self.margin - w//2, 
        9*self.height//10 - h//2))
        return (x,y,w,h)
    
    def createTitle(self, color):
        font = pygame.font.SysFont("ammericantypewriterttc", 45)
        text0 = font.render(f"High Scores List", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width//2 - w//2, 
        self.height//10 - h//2))
        return (x,y,w,h)

    def writeScores(self, color):
        #write scores into a file and read out
        listScores = []
        #first line take from 
        # https://www.guru99.com/reading-and-writing-files-in-python.html
        if os.path.exists("hiscore.txt"):
            f = open("hiscore.txt", "r")
            lines = f.readlines()
            for i in range(0, min(8, len(lines))):
                var = lines[i]
                score1 = " "
                for char in var:
                    if not char.isspace():
                        if score1 == " ":
                            score1 = str(char)
                        else:
                            score1 += str(char)
                listScores.append(int(score1))
            f.close()
            for i in range(len(listScores)):
                font = pygame.font.SysFont("ammericantypewriterttc", 25)
                text0 = font.render(f"{listScores[i]}", True, color)
                (x, y, w, h) = text0.get_rect()
                self.screen.blit(text0, (self.width//2 - w//2, 
                (i + 2) * self.height//10 - h//2))
        else:
            pass
    
    def createHiScoreScreen(self):
        #main running fxn
        bgColor = (255, 255, 255)
        lineColor = (0,125,144)
        pygame.draw.rect(self.screen, bgColor,(0,0,self.width,self.height))
        bgPic = pygame.transform.scale(self.bgImage, (self.width, self.height))
        self.screen.blit(bgPic,(0, 0,self.width//2, self.height//2))


        color = (74, 170, 199)
        (x,y,w,h) = self.makeReturn(color)
        self.writeScores(color)
        

        (x0, y0, x1, y1) = (self.width - self.margin - w//2 - 10, 
        9 * self.height//10 - h//2 - 10,
        self.width - self.margin + w//2 + 10, 
        9 * self.height//10 + h//2 + 10)

        self.createTitle(color)
        pygame.display.update()
        result = self.waitForKeyPress((x0, y0, x1, y1))
        if result != 0:
            return result
    
    def waitForKeyPress(self, startCoordinates):
        #see if user wants to return
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
        #check if point and object intersect
        (a0, b0, a1, b1) = bound1
        (x0, y0) = position
        if ((a0<x0) and (a1 > x0) and (b0 < y0) and (b1 > y0)):
            return True
        return False

