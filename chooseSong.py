#make menu to choose song from

from pygame.locals import *
import pygame
import numpy as np
from findSongs import *

class Menu(object):
    #make menu to choose song from
    def __init__(self, width, height, songList):
        self.width = width
        self.height = height
        self.num = 0
        self.songList = findSongs()
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.margin = self.width//5
        pygame.init()
        self.running = True
        self.bgImage = pygame.image.load("backgroundImage3.png").convert_alpha()
        self.songName = self.songList[self.num]

    def makeEasyMode(self, color):
        #create "Easy"
        font = pygame.font.SysFont("ammericantypewriterttc", 25)
        text0 = font.render(f"Easy", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width//2 - w//2 - 10, 
        self.height//2 - h//2))
        return (x,y,w,h)
    
    def makeMediumMode(self, color):
        #create "medium"
        font = pygame.font.SysFont("ammericantypewriterttc", 25)
        text0 = font.render(f"Medium", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width//2 - w//2 - 10, 
        5 * self.height//8 - h//2))
        return (x,y,w,h)
    
    def makeHardMode(self, color):
        #create "hard"
        font = pygame.font.SysFont("ammericantypewriterttc", 25)
        text0 = font.render(f"Hard", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width//2 - w//2 - 10, 
        3*self.height//4 - h//2))
        return (x,y,w,h)
    
    def createTitle(self, color):
        #create title
        font2 = pygame.font.SysFont("ammericantypewriterttc", 60)
        text2 = font2.render(f"{self.songName}", True, color)
        (a, b, w1, h1) = text2.get_rect()
        self.screen.blit(text2, (self.width//2 - w1//2, self.height//4 - h1//2))

    def makeButtons(self, color, h):
        #make return button
        pygame.draw.polygon(self.screen, color, 
        [(self.margin//3, self.height//2), 
        (2*self.margin//3, self.height//2 - h//2),
        (2*self.margin//3, self.height//2 + h//2)])
        pygame.draw.polygon(self.screen, color, 
        [(self.width - self.margin//3, self.height//2), 
        (self.width - 2*self.margin//3, self.height//2 - h//2),
        (self.width - 2*self.margin//3, self.height//2 + h//2)])

    def createMenu(self):
        #main running fxn
        while self.running:
            (easyPos, medPos, hardPos) = self.redrawAll() 
            result = self.waitForKeyPress(easyPos,
            medPos, hardPos)
            if result != 0 and result != 4:
                self.running = False
                return (self.songName, result)
            elif result == 4:
                self.redrawAll()
            elif result == 0:
                return (100, 0)
    
    def redrawAll(self):
        #main drawing fxn
        bgColor = (255, 255, 255)
        lineColor = (0,125,144)
        h = 40
        pygame.draw.rect(self.screen, bgColor,(0,0,self.width,self.height))
        bgPic = pygame.transform.scale(self.bgImage, (self.width, self.height))
        self.screen.blit(bgPic,(0, 0,self.width//2, self.height//2))
        color = (51, 204, 204)
        color2 = (23, 96,135)
        (a,b,w1,h1) = self.makeEasyMode(color2)
        (c,d,w2, h2) = self.makeMediumMode(color2)
        (e,f,w3, h3) = self.makeHardMode(color2)
        self.makeButtons(color, h)

        (a0, b0, a1, b1) = (self.width//2 - w1//2 - 10, 
        self.height//2 - h1//2 - 10,
        self.width//2 + w1//2 + 10, self.height//2 + h1//2 + 10)

        (c0, d0, c1, d1) = (self.width//2 - w2//2 - 10, 
        5 * self.height//8 - h2//2 - 10,
        self.width//2 + w2//2 + 10, 5 * self.height//8 + h2//2 + 10)

        (e0, f0, e1, f1) = (self.width//2 - w3//2 - 10, 
        3 * self.height//4 - h3//2 - 10,
        self.width//2 + w3//2 + 10, 3 * self.height//4 + h3//2 + 10)
        color3 = (13, 47, 92)
        self.createTitle(color3)
        pygame.display.update()
        return ((a0, b0, a1, b1), (c0, d0, c1, d1) , (e0, f0, e1, f1))
        
    
    def waitForKeyPress(self, coordEasy, coordMed, coordHard):
        #get key press
        color = (51, 204, 204)
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN: 
                    (x,y) = pygame.mouse.get_pos()
                    if self.intersect(coordEasy, (x,y)):
                        return 1
                    if self.intersect(coordMed, (x,y)):
                        return 2
                    if self.intersect(coordHard, (x,y)):
                        return 3
                    if self.hitLeft((x,y)):
                        self.num = (self.num - 1)%(len(self.songList))
                        self.songName = self.songList[self.num]
                        return 4
                    if self.hitRight((x,y)):
                        self.num = (self.num + 1)%(len(self.songList))
                        self.songName = self.songList[self.num]
                        return 4
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False 
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

