#makes the start screen

from pygame.locals import *
import pygame
import numpy as np

#class base structure from
#https://stackoverflow.com/questions/19936347/pygame-window-and-sprite-class-python

class StartScreen(object):
    #creates start screen
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gameRunning = True
        self.running = False
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.margin = 125
        pygame.init()
        self.bgImage = pygame.image.load("backgroundPic.png").convert_alpha()

    def makeGameMode(self, bgColor, lineColor):
        #create "Game Mode"
        color = (18, 126, 190)
        font = pygame.font.SysFont("ammericantypewriterttc", 25)
        text0 = font.render(f"Game Mode", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width//2 - w//2 - 10, 
        self.height//2 - h//2 - 40))
        return (x,y,w,h)
    
    def makeLearnMode(self, bgColor, lineColor):
        #create "Learn Mode"
        color = (18, 126, 190)
        font = pygame.font.SysFont("ammericantypewriterttc", 25)
        text0 = font.render(f"Learning Mode", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width//2 - w//2 - 10, 
        6*self.height//10 - h//2 - 40))
        return (x,y,w,h)
    
    def makeHelpMode(self, bgColor, lineColor):
        #create "Help"
        color = (18, 126, 190)
        font = pygame.font.SysFont("ammericantypewriterttc", 25)
        text0 = font.render(f"Help", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width//2 - w//2 - 10, 
        7*self.height//10 - h//2 - 40))
        return (x,y,w,h)
        
    def makeHiScore(self, bgColor, lineColor):
        #create "High Scores"
        color = (18, 126, 190)
        font = pygame.font.SysFont("ammericantypewriterttc", 25)
        text0 = font.render(f"High Scores", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width//2 - w//2 - 10, 
        8*self.height//10 - h//2 - 40))
        return (x,y,w,h)
    
    def makeRecord(self, bgColor, lineColor):
        #create "Record Song"
        color = (18, 126, 190)
        font = pygame.font.SysFont("ammericantypewriterttc", 25)
        text0 = font.render(f"Record Song", True, color)
        (x, y, w, h) = text0.get_rect()
        self.screen.blit(text0, (self.width//2 - w//2 - 10, 
        9*self.height//10 - h//2 - 40))
        return (x,y,w,h)

    def createTitle(self):
        #Make Game Title
        color = (18, 126, 190)
        font2 = pygame.font.SysFont("ammericantypewriterttc", 60)
        text1 = font2.render(f"Rhythm", True, color)
        (a, b, w1, h1) = text1.get_rect()
        self.screen.blit(text1, (self.width//2 - w1 - 10, self.height//4))
        text2 = font2.render(f"Earth", True, color)
        self.screen.blit(text2, (self.width//2 + 10, self.height//4))

    def createStartScreen(self):
        #main function
        bgColor = (255, 255, 255)
        lineColor = (0,125,144)
        pygame.draw.rect(self.screen, bgColor,(0,0,self.width,self.height))
        bgPic = pygame.transform.scale(self.bgImage, (self.width, self.height))
        self.screen.blit(bgPic,(0, 0,self.width//2, self.height//2))

        (x,y,w,h) = self.makeGameMode(bgColor, lineColor)
        (a,b,w1,h1) = self.makeLearnMode(bgColor, lineColor)
        (c, d, w2, h2) = self.makeHelpMode(bgColor, lineColor)
        (e, f, w3, h3) = self.makeHiScore(bgColor, lineColor)
        (g, h, w4, h4) = self.makeRecord(bgColor, lineColor)
        

        (x0, y0, x1, y1) = (self.width//2 - w//2, 
        self.height//2 - h//2 - 10 - 40,
        self.width//2 + w//2 + 10, self.height//2 + h//2 + 10 - 40)

        (a0, b0, a1, b1) = (self.width//2 - w1//2, 
        6 * self.height//10 - h1//2 - 10 - 40,
        self.width//2 + w1//2 + 10, 6 * self.height//10 + h1//2 + 10 - 40)

        (c0, d0, c1, d1) = (self.width//2 - w2//2, 
        7 * self.height//10 - h2//2 - 10 - 40,
        self.width//2 + w2//2 + 10, 7 * self.height//10 + h2//2 + 10 - 40)

        (e0, f0, e1, f1) = (self.width//2 - w3//2, 
        8 * self.height//10 - h3//2 - 10 - 40,
        self.width//2 + w3//2 + 10, 8 * self.height//10 + h3//2 + 10 - 40)

        (g0, h0, g1, h1) = (self.width//2 - w4//2, 
        9 * self.height//10 - h4//2 - 10- 40,
        self.width//2 + w4//2 + 10, 9 * self.height//10 + h4//2 + 10 - 40)


        self.createTitle()
        pygame.display.update()
        result = self.waitForKeyPress((x0, y0, x1, y1), (a0,b0,a1,b1),
        (c0, d0, c1, d1), (e0, f0, e1, f1),(g0, h0, g1, h1))
        if result != 0:
            return result
    
    def waitForKeyPress(self, startCoordinates, coordOther, coordHelp, 
    coordScores, coordRecord):
    #find where user pressed
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN: 
                    (x,y) = pygame.mouse.get_pos()
                    if self.intersect(startCoordinates, (x,y)):
                        return 1
                    if self.intersect(coordOther, (x,y)):
                        return 2
                    if self.intersect(coordHelp, (x,y)):
                        return 3
                    if self.intersect(coordScores, (x,y)):
                        return 4
                    if self.intersect(coordRecord, (x,y)):
                        return 5
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 0
        return 0
        
    def intersect(self, bound1, position):
        (a0, b0, a1, b1) = bound1
        (x0, y0) = position
        if ((a0<x0) and (a1 > x0) and (b0 < y0) and (b1 > y0)):
            return True
        return False