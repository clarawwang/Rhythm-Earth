#makes game mode

from pygame.locals import *
import pygame
import numpy as np
import wave
import sys
import cv2
import random
import time
import json
import os.path
from os import path
import pyaudio


class Beat(object):
    #create Beat class: keeps track of position, image, and whether or not it's
    #hit and it's bin is matched properly
    def __init__(self, game, x, y, image):
        self.x= x
        self.y = y
        self.game = game
        self.width = (self.game.width-2 *self.game.margin)//8 - 2*10
        self.height = (self.game.width-2 *self.game.margin)//8
        self.image = image
        self.isHit = False
        self.binHit = False
    def draw(self):
        self.game.screen.blit(self.image, 
        (self.x - self.width//2, self.y - self.height//2))
    def __hash__(self):
        hashables = (self.x, self.y, self.image)
        return hash(hashables)
    def __eq__(self,other):
        if isinstance(other, type(self)):
            return ((self.x == other.x) and (self.y == other.y) and 
         (self.image == other.image))
        else:
            return False

class Hand(object):
    #creates the hands in the game
    def __init__(self, game, x0, y0, x1, y1):
        self.refArea = None
        self.isClenched = False
        self.area = None
        self.sign = 1
        self.x0 = x0
        self.y0 = y0
        if (self.x0 != None and self.y0 != None):
            self.x1 = x0 + x1
            self.y1 = y0 + y1
        else:
            self.x1 = None
            self.y1 = None
        
        self.game = game
        self.color = (104, 149, 197)
    def draw(self):
        color = (255, 0 ,0)
        if (self.x0 != None and self.y0 != None):
            pygame.draw.rect(self.game, self.color,
            (self.x0,self.y0, self.x1 - self.x0,self.y1 - self.y0), 2)
    #for drawing right hand
    def draw2(self):
        color = (255, 0 ,0)
        if (self.x0 != None and self.y0 != None):
            pygame.draw.circle(self.game, self.color,
            (int((self.x0 + self.x1)/2), int((self.y1 + self.y0)/2)), 10)
    
class Bin(object):
    #creates the bin objects for right hand to fix
    def __init__(self, game, x, y, image):
        self.game = game
        self.x = x
        self.y = y
        self.image = image
        self.width = 75
        self.height = 50
    def draw(self):
        self.game.blit(self.image,
         (self.x - self.width//2,self.y - self.height//2))
    def __hash__(self):
        hashables = (self.x, self.y, self.image)
        return hash(hashables)
        

#class base structure from
#https://stackoverflow.com/questions/19936347/pygame-window-and-sprite-class-python

class Game(object):
    #initializes game
    def __init__(self, width, height, music, diff):
        self.songNum = music
        self.width = width
        self.height = height
        self.gameRunning = True
        self.running = False
        self.score = 0
        self.health = 100
        self.beatLong = False
        self.winning = False
        ########## Music ###################
        self.chunk = 1024
        self.time = 0
        self.time1 = 0
        self.setNotes = dict()
        self.beats = []
        self.color1 = (125, 0, 0)
        self.color2 = (200, 100, 50)
        self.color3 = (100, 30, 250)
        self.color4 = (50, 220, 10)
        self.soundFile = music
        ############## Display ###############
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.camera = cv2.VideoCapture(0)
        self.paused = False
        self.background = None 
        self.margin = 150
        self.leftHand = Hand(self.screen, None, None, None, None)
        self.rightHand = Hand(self.screen, None, None, None, None)
        self.SONG_END = pygame.USEREVENT + 2
        self.lose = False
        self.createBins()
        self.createTrash()
        self.bonus = 0
        pygame.init()
        self.diff = diff
        self.missed = None

    def createTrash(self):
        #initialize the trash pictures
        measurement = (self.width-2 *self.margin)//8
        plasticBottle = pygame.image.load("plasticBottle.png").convert_alpha()
        self.plasticBottle = pygame.transform.scale(plasticBottle, 
        (measurement, measurement))
        chipBag = pygame.image.load("chipBag.png").convert_alpha()
        self.chipBag = pygame.transform.scale(chipBag, 
        (measurement, measurement))
        applePeel = pygame.image.load("applePeel.png").convert_alpha()
        self.applePeel = pygame.transform.scale(applePeel, 
        (measurement, measurement))
        fish = pygame.image.load("fish.png").convert_alpha()
        self.fish = pygame.transform.scale(fish, (measurement, measurement))
        eggShells = pygame.image.load("eggShells.png").convert_alpha()
        self.eggShells = pygame.transform.scale(eggShells,
        (measurement, measurement))
        can = pygame.image.load("can.png").convert_alpha()
        self.can = pygame.transform.scale(can,
        (measurement, measurement))
        self.createExtraTrash()
        self.imageList= [self.plasticBottle, self.chipBag, self.applePeel, 
        self.fish, self.eggShells, self.can, self.coffee, 
        self.teaBag, self.eggCarton]
        self.imageDict = {self.plasticBottle:self.recycle, 
        self.chipBag:self.trash, self.applePeel: self.composting,
        self.fish:self.trash, self.eggShells:self.composting,
        self.can:self.recycle, self.coffee:self.trash, 
        self.teaBag:self.composting, self.eggCarton:self.recycle}
    
    def createExtraTrash(self):
        measurement = (self.width-2 *self.margin)//8
        coffee = pygame.image.load("coffee.png").convert_alpha()
        self.coffee = pygame.transform.scale(coffee, 
        (measurement, measurement))
        teaBag = pygame.image.load("teaBag.png").convert_alpha()
        self.teaBag = pygame.transform.scale(teaBag, 
        (measurement, measurement))
        eggCarton = pygame.image.load("eggCarton.png").convert_alpha()
        self.eggCarton = pygame.transform.scale(eggCarton, 
        (measurement, measurement))
    
    def createBins(self):
        #initialize the bins
        trashImage = pygame.image.load("trash.png").convert_alpha()
        trashImage1 = pygame.transform.scale(trashImage, (75, 50))
        recycleImage = pygame.image.load("recycle.png").convert_alpha()
        recycleImage1 = pygame.transform.scale(recycleImage, (75, 50))
        compostingImage = pygame.image.load("composting.png").convert_alpha()
        compostingImage1 = pygame.transform.scale(compostingImage, (75, 50))
        self.recycle = Bin(self.screen, self.width - self.margin + 50, 
        (self.height//2 - 100//2)//2, recycleImage1)
        self.trash = Bin(self.screen, self.width - self.margin + 50, 
        self.height//2 - 100//2  , trashImage1)
        self.composting = Bin(self.screen, self.width - self.margin + 50, 
        (3*self.height//2 - 100//2)//2, compostingImage1)
        self.binNames = {self.recycle: ("recycling",
        (self.margin//2, self.margin//2 + 50))
        , self.trash: ("trash", (self.margin//2, self.margin//2 + 75)), 
        self.composting: ("composting",(self.margin//2, self.margin//2 + 100))}
        self.totalRecycling = 0
        self.caughtRecycling = 0
        self.totalTrash = 0
        self.caughtTrash = 0
        self.totalComposting = 0
        self.caughtComposting = 0


    #code modified from: 
    # https://nerdparadise.com/programming/pygame/part5    
    def textDraw(self):
        #draw score and health
        font = pygame.font.SysFont("comicsansms", 25)
        color = (0, 128, 0)
        text = font.render(f"Score: {self.score}", True, color)
        self.screen.blit(text, (self.margin//2, self.margin//2))
        text = font.render(f"Bonus: {self.bonus}", True, color)
        self.screen.blit(text, (self.margin//2, self.margin//2 + 25))

    def healthDraw(self):
        #draws health bar
        color1 = (36, 156, 98)
        color2 = (255,242,0)
        color3 = (202, 0, 42)
        if self.health < 25:
            pygame.draw.rect(self.screen, color3,
            (0,0,self.width * self.health//100, 50))
        elif self.health < 50:
            pygame.draw.rect(self.screen, color2,
            (0,0,self.width * self.health//100, 50))
        else:
            pygame.draw.rect(self.screen, color1,
            (0,0,self.width * self.health//100, 50))
            

    def drawBackground(self):
        #drawa basic bg
        pygame.draw.rect(self.screen, (0, 0, 0),(0,0,self.width,self.height))
        pygame.draw.line(self.screen, (0,125,144), (0,self.height - 100),
         (self.width, self.height - 100))

    def drawAdvice(self, bin):
        #draws where the object should have gone
        (name, pos) = self.binNames[bin]
        font = pygame.font.SysFont("comicsansms", 25)
        color = (102, 162, 122)
        text = font.render(f"{name} ", True, color)
        self.screen.blit(text, pos)
    
    def redrawAll(self):
        #overall draw function
        self.drawBackground()
        self.textDraw()
        if self.missed != None:
            self.drawAdvice(self.missed)
        self.trash.draw()
        self.recycle.draw()
        self.composting.draw()
        
        for beats in self.beats:
            
            for beat1 in beats:
                beat1.draw()
            
        self.healthDraw()
        self.leftHand.draw()
        self.rightHand.draw2()
        if (self.time < 10):
            font = pygame.font.SysFont("comicsansms", 32)
            color = (0, 128, 0)
            text = font.render(f"Please keep hands steady", True, color)
            (x, h, w,h) = text.get_rect()
            self.screen.blit(text, 
            (self.width//2 - w//2, self.height//2 - h//2))
        pygame.display.update()

    def intersect(self, bound1, position):
        #find intersection of a point and an object
        (a0, b0, a1, b1) = bound1
        (x0, y0) = position
        if ((a0<x0) and (a1 > x0) and (b0 < y0) and (b1 > y0)):
            return True
        return False

    def boundsIntersect(self, playerBounds, beatBounds):
        #find intersection of two objects
        (x0, y0, x1, y1) = playerBounds
        (a0, b0, a1, b1) = beatBounds 
        return ((x1 >= a0) and (a1 >= x0) and (y1 >= b0) and (b1 >= y0))
    
    def checkHand(self):
        #checks to see if hand is clenched
        if (self.leftHand.refArea != None and self.leftHand.area != None and
            self.leftHand.area > 5/6 * self.leftHand.refArea):
            self.leftHand.sign = 1
            self.leftHand.isClenched = False
            
        if (self.rightHand.refArea != None and self.rightHand.area != None and
            self.rightHand.area > 5/6 * self.rightHand.refArea):
            self.rightHand.sign = 1
            self.rightHand.isClenched = False
    
    def getBeatBounds(self, beat):
        #find the beat bounds
        return (beat.x, beat.y,
                beat.x + beat.width, beat.y + beat.height)
    
    def checkBin(self, beat):
        #find if the beat is matched to the correct bin
        correctBin = self.imageDict[beat.image]
        playerBounds = ((self.rightHand.x0 + self.rightHand.x1)//2, 
        (self.rightHand.y0 + self.rightHand.y1)//2)
        binBounds = (correctBin.x - 10 - correctBin.width//2, 
        correctBin.y - 10 - correctBin.height//2,
        correctBin.x + correctBin.width//2 + 10, 
        correctBin.y + correctBin.height//2 + 10)
        if self.intersect(binBounds,playerBounds):
            return True
        return False
    
    def singleBeatIntersection(self, beat):
        #check for single beats if caught
        if (self.leftHand.refArea != None and 
        self.leftHand.area <= 5/6 * self.leftHand.refArea):
            self.leftHand.isClenched = True
            if self.leftHand.sign == 1:
                self.leftHand.sign = -1
                playerBounds = (self.leftHand.x0, self.leftHand.y0,
                self.leftHand.x1, self.leftHand.y1)
                beatBounds = self.getBeatBounds(beat)
                if (self.checkBin(beat) and 
                self.boundsIntersect(playerBounds, beatBounds)):
                    beat.isHit = True
                    beat.binHit = True  
                    return True
                elif (not self.checkBin(beat) and 
                self.boundsIntersect(playerBounds, beatBounds)):
                    beat.isHit = True
                    self.health -= 5  
                    return True
        return False
            
    
    def multipleBeatIntersection(self,beat):
        #check for multiple beats if all caught
        if self.leftHand.sign == -1:
            for beat0 in beat:
                playerBounds = (self.leftHand.x0, self.leftHand.y0,
                self.leftHand.x1, self.leftHand.y1)
                beatBounds = self.getBeatBounds(beat0)
                if (self.boundsIntersect(playerBounds, beatBounds) 
                and self.checkBin(beat0)):
                    beat0.isHit = True
                    beat0.binHit = True
                elif (self.boundsIntersect(playerBounds, beatBounds) 
                and not self.checkBin(beat0)):
                    beat0.isHit = True
                    
                    
                    

    def checkAllBeatsHit(self, beat):
        #checks for mult beat if all the centers hit
        for beat0 in beat:
            if beat0.isHit == False:
                return False
        return True
    
    def checkAllBeatsBin(self, beat):
        #checks for mult beat if bin matched for all beats
        for beat0 in beat:
            if beat0.binHit == False:
                return False
        return True
    
    def getPoints(self,bin1, dCaught, dTotal):
        #find user stats for learning/playing game
        if bin1 == self.recycle:
            self.caughtRecycling += dCaught
            self.totalRecycling += dTotal
        elif bin1 == self.composting:
            self.caughtComposting += dCaught
            self.totalComposting += dTotal
        elif bin1 == self.trash:
            self.caughtTrash += dCaught
            self.totalTrash += dTotal

    def singleBeat(self, beat):
        #checks and calc score for single beats
        if (beat[0].y <= self.height 
        and 
        beat[0].y + beat[0].height >= self.height - 150):
            self.beatLong = False
            if self.singleBeatIntersection(beat[0]):
                self.health += 5   
                self.score += 10  
                self.beats.remove(beat)
                if not self.checkBin(beat[0]):
                    self.missed = self.imageDict[beat[0].image]
                    self.getPoints(self.missed, 0, 1)
                else:
                    self.missed = None
                    bin1 = self.imageDict[beat[0].image]
                    self.getPoints(bin1, 1, 1)
        elif (beat[0].y > self.height 
        and beat[0].isHit == False):
            self.score -= 2  
            self.health -= 2 
            self.beats.remove(beat)
            self.missed = self.imageDict[beat[0].image]
            self.getPoints(self.missed, 0, 1)
    
    def multipleBeats(self, beat):
        #checks and calc score for multiple beats
        if (beat[0].y <= self.height
        and 
        beat[0].y + beat[0].height >= self.height - 150):
            self.beatLong = True
            if (self.leftHand.refArea != None and 
            self.leftHand.area <= 5/6 * self.leftHand.refArea):
                self.leftHand.isClenched = True
                self.leftHand.sign = -1
                self.multipleBeatIntersection(beat)
                if self.checkAllBeatsHit(beat):
                    self.score += 10
                    if self.checkAllBeatsBin(beat):
                        self.health += 10
                        self.missed = None
                        bin1 = self.imageDict[beat[0].image]
                        self.getPoints(bin1, 1, 1)      
                    else:
                        self.health -= 5
                        self.getPoints(self.missed, 0, 1)
                    self.beats.remove(beat)
        elif beat[0].y > self.height:
            if self.checkAllBeatsHit(beat):
                self.score += 5
            else:
                self.score -= 2  
            if self.checkAllBeatsBin(beat):
                self.health += 2 
                self.missed = None
                bin1 = self.imageDict[beat[0].image]
                self.getPoints(bin1, 1, 1)
            else:
                self.missed = self.imageDict[beat[0].image]
                self.getPoints(self.missed, 0, 1)
                self.health -= 2
            self.beats.remove(beat)       
        else:
            self.beatLong = False


    def checkIntersection(self):
        #checks last four beats to see if user hit
        self.missed = None
        for beat in self.beats[-4:]:
            if len(beat) == 1:
                self.singleBeat(beat)
            else:
                self.multipleBeats(beat)


    def createBeats(self, listBeats):
        #makes the beats from note dictionary
        imageUse = random.randint(0, len(self.imageList)-1)
        ypos = 1
        listBeat = []
        for beat in listBeats:
            if beat == 1:
                xpos = (self.width - 2*self.margin - 50)//8 + self.margin
            elif beat == 2:
                xpos = 3*(self.width - 2*self.margin -50)//8 + self.margin
            elif beat == 3:
                xpos = 5*(self.width - 2*self.margin -50)//8 + self.margin
            else:
                xpos = 7*(self.width - 2*self.margin -50)//8 + self.margin
            beat = Beat(self, xpos, ypos, self.imageList[imageUse])
            listBeat.append(beat)
        self.beats.append(listBeat)

    def playMusic(self, musicFile, loop):
        #plays music
        if (self.running == True):
            pygame.mixer.pre_init(frequency=44100, size=-16, buffer=2096)
            pygame.mixer.music.set_endevent(self.SONG_END)
            pygame.mixer.music.load(musicFile)
            pygame.mixer.music.play(loops = loop, start = 0.0)
        else:
            pygame.mixer.music.stop()

    def timerFired(self):
        #check every timer fired mostly to create beats
        if not self.paused:
            self.findArea()
            self.checkHand()
            timeNeed = int((self.timeDiff) * (self.time+ 6))
            if timeNeed in self.setNotes:
                self.createBeats(self.setNotes[timeNeed])
                del self.setNotes[timeNeed]
            elif timeNeed-1 in self.setNotes:
                self.createBeats(self.setNotes[timeNeed-1])
                del self.setNotes[timeNeed-1]
            elif timeNeed-2 in self.setNotes:
                self.createBeats(self.setNotes[timeNeed-2])
                del self.setNotes[timeNeed-2]
            elif timeNeed-3 in self.setNotes:
                self.createBeats(self.setNotes[timeNeed-3])
                del self.setNotes[timeNeed-3]
            self.moveBeats()
            self.checkIntersection()
            self.redrawAll()
        if self.paused:
            self.drawPause()
    
    def drawPause(self):
        #draws "pause" when paused
        font = pygame.font.SysFont("comicsansms", 25)
        color = (0, 128, 0)
        text = font.render(f"Pause", True, color)
        self.screen.blit(text, (self.width//2, self.height//2))
    
    def moveBeats(self):
    #move the beats
        for beats in self.beats:
            for beat in beats:
                beat.y += int(self.height//20)
            
    
    def runTime(self):
        #check for conditions during runtime
        result = self.getEvent()
        self.timerFired()
        
        if self.health > 100:
            self.bonus += self.health - 100
            self.health = 100
        return result
    
    #basic structure taken from:
    #https://riptutorial.com/pygame/example/18046/event-loop 
    def getEvent(self):
        #get events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False # esc to quit 
                    return (0, self.score + self.bonus * 2, 0, 0, 0)
                if event.key == pygame.K_p:
                    if self.paused == False:
                        self.paused = True
                    else:
                        self.paused = False
                    return "p"
            elif event.type == self.SONG_END:
                self.winning = True
                self.running = False
                return (2, self.score + self.bonus*2, 
                (self.caughtRecycling, self.totalRecycling), 
                (self.caughtComposting, self.totalComposting),
                (self.caughtTrash, self.totalTrash))
        if self.health < 0:
            self.lose = True
            self.running = False 
            return (1, self.score + self.bonus*2, 0, 0, 0)
        return (None, None)
    
    def findArea(self):
        #finds hand area
        if (self.leftHand.x0 != None and self.leftHand.y0 != None):
            self.leftHand.area = (abs(self.leftHand.x0 - self.leftHand.x1) 
            * abs(self.leftHand.y0 - self.leftHand.y1))
        else:
            self.leftHand.area = None
        if (self.rightHand.x0 != None and self.rightHand.y0 != None):
            self.rightHand.area = (abs(self.rightHand.x0 - self.rightHand.x1) * 
            abs(self.rightHand.y0 - self.rightHand.y1))
        else:
            self.rightHand.area = None


    def run(self):
        #overall run function
        ret, frame = self.camera.read()
        frame = cv2.flip(frame, 1)
        frame = self.detectAndDisplay(frame)


        self.createFile()
        self.running = True
        
        while self.running: 
            if self.time == 10:
                self.playMusic(self.soundFile, 1)
            if (self.time <= 10):
                self.leftHand.refArea = self.leftHand.area
                self.rightHand.refArea = self.rightHand.area
            ret, frame = self.camera.read()
            frame = cv2.flip(frame, 1)
            frame = self.detectAndDisplay(frame)
            if self.paused:
                pygame.mixer.music.pause()
            result = self.runTime()
            self.time += 1
            pygame.time.Clock().tick(43)
            if result != (None, None) and result != "p":
                pygame.mixer.music.stop()
                return result
            elif result == "p":
                if self.paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

    def checkDictFile(self, tup):
        #writing into and opening json file code modified from
        #https://stackoverflow.com/questions/7100125/storing-python-dictionaries
        # creates json file with dictionary 
        if os.path.exists("songsDict.txt"):
            diff = str(tup[1])
            newKey = tup[0] + diff
            with open("songsDict.txt") as json_data:
                dictPy = json.load(json_data)
                newDict = {}
                if newKey not in dictPy.keys():
                    self.findBeatsDict()
                    dataDict = self.setNotes
                    dictPy[newKey] = dataDict
                    with open("songsDict.txt", 'w') as outfile:
                        json.dump(dictPy, outfile)
                    return dataDict
                else:
                    dataDict = dictPy[newKey]
                    for key in dataDict:
                        newDict[int(key)] = dataDict[key]
                    return newDict
        else:
            diff = str(tup[1])
            newKey = tup[0] + diff
            self.findBeatsDict()
            dataDict = self.setNotes
            dict1 = {newKey:dataDict}
            with open("songsDict.txt", 'w') as outfile:
                json.dump(dict1, outfile)
            return dataDict

        
    def findBeatsDict(self):
        #finds beats
        self.time1 = 0
        it = 0
        wf = wave.open(self.soundFile, 'rb')
        data = wf.readframes(self.chunk)
        self.fRate = wf.getframerate()
        self.frames = wf.getnframes()
        self.channels = wf.getnchannels()
        energySum1 = []
        energySum2 = []
        energySum3 = []
        energySum4 = []
        while len(data) > 0:
            data = wf.readframes(self.chunk)
            if (len(data)!= 0):
                self.analyzeData(data, energySum1, energySum2,
                energySum3, energySum4)
            self.time1 += 1
    
    def findTime(self):
        #finds time if not running through find beats
        self.time1 = 0
        it = 0
        wf = wave.open(self.soundFile, 'rb')
        data = wf.readframes(self.chunk)
        self.fRate = wf.getframerate()
        self.frames = wf.getnframes()
        self.channels = wf.getnchannels()
        while len(data) > 0:
            data = wf.readframes(self.chunk)
            self.time1 += 1
        

    def createFile(self):
        #makes json file if needed
        tup = (self.soundFile, self.diff)
        self.setNotes = self.checkDictFile(tup)
        self.findTime()
        timeList = list(self.setNotes.keys())
        self.timeDiff = self.time1/430
        coeff = -0.75/(430 * 4.3)*(self.time1 - 430) + 1.5
        #if coeff >= 2.3:
            #coeff = 2.3
        if coeff <= 0.3:
            coeff = 0.3
        self.timeDiff *= coeff
        
        

    def analyzeData(self, data, energySum1, energySum2, energySum3, energySum4):
        #separate beats into diff freq and perform analysis
        data_int = np.frombuffer(data, dtype = np.int16)
        fftdata0 = np.fft.rfft(data_int)
        fftdata0 = [np.sqrt(c.real **2 + c.imag **2) for c in fftdata0]
        range1 = len(fftdata0)//4
        range2 = len(fftdata0)//2
        range3 = len(fftdata0)//4 * 3
        local1 = []
        local2 = []
        local3 = []
        local4 = []
        if self.time1%2 == 0:
            for dataPoint in range(len(fftdata0)):
                if dataPoint <= range1:
                    energySum1.append(fftdata0[dataPoint])
                    energySum1 = self.checkLength(energySum1)
                    local1.append(fftdata0[dataPoint])
                elif dataPoint <= range2:
                    energySum2.append(fftdata0[dataPoint])
                    energySum2 = self.checkLength(energySum2)
                    local2.append(fftdata0[dataPoint])
                elif dataPoint <= range3:
                    energySum3.append(fftdata0[dataPoint])
                    local3.append(fftdata0[dataPoint])
                    energySum3 = self.checkLength(energySum3)
                elif dataPoint > range3:
                    energySum4.append(fftdata0[dataPoint])
                    energySum4 = self.checkLength(energySum4)
                    local4.append(fftdata0[dataPoint]) 
        diff = 2**(7-self.diff)
        if self.time1 == 2 or self.time1 % diff == 0: 
            local1a, beat1 = self.calcBeat(local1, energySum1, 1)
            local2a, beat2 = self.calcBeat(local2, energySum2, 2)
            local3a, beat3 = self.calcBeat(local3, energySum3, 3)
            local4a, beat4 = self.calcBeat(local4, energySum4, 4)
            self.findGreatest(local1a, beat1, local2a, beat2, local3a, beat3, 
            local4a, beat4)
        

    def checkLength(self, energySum):
        #make sure to take last 1024 samples
        if (len(energySum) > self.chunk):
            energySum.pop(0)
        return energySum

    def findGreatest(self, local1, beat1, local2, beat2, local3, beat3, 
            local4, beat4):
        #find the beat structure so it is playable
        localList = [(local1,beat1), (local2, beat2), 
        (local3,beat3), (local4,beat4)]
        setBeats = set()
        
        for local in range(len(localList)-1):
            
            if localList[local][0] != 0 and localList[local + 1][0] != 0:
                
                if self.time1 in self.setNotes:
                    if localList[local][1] not in self.setNotes[self.time1]:
                        self.setNotes[self.time1].append(localList[local][1])
                    self.setNotes[self.time1].append(localList[local+1][1])
                
                else:
                    self.setNotes[self.time1]= [localList[local][1]]
                    self.setNotes[self.time1].append(localList[local+1][1])
                setBeats.add(beat1)
        
        if len(setBeats) == 0:
        
            maxList = sorted([local1, local2, local3, local4], 
            reverse = True)
            if maxList != [0, 0, 0, 0]:
                if maxList[0] == local1:
                    self.setNotes[self.time1] = [beat1]
                elif maxList[0] == local2:
                    self.setNotes[self.time1] = [beat2]
                elif maxList[0] == local3:
                    self.setNotes[self.time1] = [beat3]
                elif maxList[0] == local4:
                    self.setNotes[self.time1] = [beat4]
        


    #math logic from:
    #http://archive.gamedev.net/archive/reference/programming/features/beatdetection/
    def calcBeat(self, local, fftdata1, num):
        #calculates if something is a beat
        ypos = 0
        if len(local) != 0:
            localE = np.sum(local)//len(local)
        else:
            localE = 0
        energySum = fftdata1   

        if len(energySum) != 0: 
            energyAvg = np.sum(energySum)//len(energySum) 
        else:
            energyAvg = 0 
        
        prev = list(self.setNotes.keys())
        if (len(prev)!= 0 and self.time1 > 
        (2**(7-self.diff))* (4-self.diff) + prev[-1]):
            var = np.var(energySum)
            sensitivity = -0.00257 * var + 1.0
        else:
            sensitivity = 1.3
        
        if (localE!= 0 and energySum != 0 and 
        (localE > sensitivity * energyAvg)):
            beat = num
            return (localE, beat)
            
        return (0, 0)

#webcam opening modified from:
    #https://gist.github.com/tedmiston/6060034
    #contour understood from documentation and 
    #https://datacarpentry.org/image-processing/09-contours/
    #color dtection modified from: 
    # https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
    def detectAndDisplay(self, frame):
        #finds user BLUE hands
        color = (225,144,30)
        color1 = (0,0, 225)
        thickness = 2
        frame=cv2.GaussianBlur(frame, (3, 3), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #blue
        lower = np.array([100,50,50])
        upper = np.array([130,255,255])

        mask = cv2.inRange(hsv, lower, upper)
        contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,
        cv2.CHAIN_APPROX_NONE)   
        if len(contours)!= 0:
            cnt = sorted(contours, key=cv2.contourArea, reverse=True)
            if len(contours) >= 2:
                values = []
                for c in range(2):
                    x,y,w,h = cv2.boundingRect(cnt[c]) 
                    values.append((x * self.width//800,
                    y,
                     w * self.width//800,
                     h))   
                    img3 = cv2.rectangle(frame,(x,y),(x+w,y+h),
                    color1, thickness)
                self.setValues(values)
                return frame
                
            else:
                x,y,w,h = cv2.boundingRect(cnt[0]) 
                img3 = cv2.rectangle(frame,(x,y),(x+w,y+h),color, thickness)
                self.leftHand.x0 = x + w/4
                self.leftHand.y0 = y + h/4          
                self.leftHand.x1 = x + w * 3/4
                self.leftHand.y1 = y + h * 3/4
                self.rightHand.x0 = None
                self.rightHand.y0 = None
                self.rightHand.x1 = None
                self.rightHand.y1 = None
                self.paused = True
                return frame
        else:
            self.leftHand.x0 = None
            self.leftHand.y0 = None
            self.leftHand.x1 = None
            self.leftHand.y1 = None
            self.rightHand.x0 = None
            self.rightHand.y0 = None
            self.rightHand.x1 = None
            self.rightHand.y1 = None
            self.paused = True
            return frame


    def setValues(self, values):
        if values[0][0] > values[1][0]:
            self.rightHand.x0 = values[0][0] + values[0][2] * 1/4
            self.rightHand.y0 = values[0][1] + values[0][3] * 1/4
            self.rightHand.x1 = values[0][0] + values[0][2] * 3/4
            self.rightHand.y1 = values[0][1] + values[0][3] * 3/4
            self.leftHand.x0 = values[1][0] + values[1][2] * 1/4
            self.leftHand.y0 = values[1][1] + values[1][3] * 1/4
            self.leftHand.x1 = values[1][0] + values[1][2] * 3/4
            self.leftHand.y1 = values[1][1] + values[1][3] * 3/4

            
        else:
            self.leftHand.x0 = values[0][0] + values[0][2] * 1/4
            self.leftHand.y0 = values[0][1] + values[0][3] * 1/4
            self.leftHand.x1 = values[0][0] + values[0][2] * 3/4
            self.leftHand.y1 = values[0][1] + values[0][3] * 3/4
            self.rightHand.x0 = values[1][0]+ values[1][2] * 1/4
            self.rightHand.y0 = values[1][1]+ values[1][3] * 1/4
            self.rightHand.x1 = values[1][0] + values[1][2] * 3/4
            self.rightHand.y1 = values[1][1] + values[1][3] * 3/4
