#makes the learning mode game

import pyaudio
from pygame.locals import *
import pygame
import numpy as np
import wave
import sys
import cv2
import random
import time


##########BEAT
class Beat(object):
    #make beat object
    def __init__(self, game, x, y, image, num):
        self.x= x
        self.y = y
        self.game = game
        self.width = (self.game.width-2 *self.game.margin)//8 - 2*10
        self.height = (self.game.width-2 *self.game.margin)//8
        self.image = image
        self.isHit = False
        self.binHit = False
        self.num = num
    def draw(self):
        self.game.screen.blit(self.image, 
        (self.x - self.width//2, self.y - self.height//2))
    def __hash__(self):
        hashables = (self.x, self.y, self.image, self.num)
        return hash(hashables)
    def __eq__(self,other):
        if isinstance(other, type(self)):
            return ((self.x == other.x) and (self.y == other.y) and 
         (self.image == other.image) and (self.num == other.num))
        else:
            return False


###### Hand

class Hand(object):
    #make hand object
    def __init__(self, game, x0, y0, x1, y1):
        self.refArea = None
        self.isClenched = False
        self.area = None
        self.sign = 1
        if x0 != None:
            self.x0 = x0 * 1/3
        else:
            self.x0 = None
        if y0 != None:
            self.y0 = y0 * 1/3
        else:
            self.y0 = None
        if (self.x0 != None and self.y0 != None):
            self.x1 = x1 * 1/3 + x0 
            self.y1 = y1 * 1/3 + y0 
        else:
            self.x1 = None
            self.y1 = None
        
        self.game = game
        self.color = (104, 149, 197)
        self.beat = []
    def draw(self):
        if (self.x0 != None and self.y0 != None):
            pygame.draw.rect(self.game, self.color,
            (self.x0,self.y0, self.x1 - self.x0,self.y1 - self.y0), 2)
    def draw2(self):
        if (self.x0 != None and self.y0 != None):
            pygame.draw.circle(self.game, self.color,
            ((self.x0 + self.x1)//2, (self.y1 + self.y0)//2), 10)

##### Trash Bin #########
class Bin(object):
    #make trash object
    def __init__(self, game, x, y, image):
        self.game = game
        self.x = x
        self.y = y
        self.image = image
        self.width = 100
        self.height = 75
    def draw(self):
        self.game.blit(self.image,
         (self.x - self.width//2,self.y - self.height//2))
    def __hash__(self):
        hashables = (self.x, self.y, self.image)
        return hash(hashables)

################# Game ##############        

#class base structure from
#https://stackoverflow.com/questions/19936347/pygame-window-and-sprite-class-python

class LearnGame(object):
    #general learning mode game
    def __init__(self, width, height, music):
        self.soundFile = music
        self.width = width
        self.height = height
        self.gameRunning = True
        self.running = False
        self.score = 0
        self.beatLong = False
        self.winning = False
        ########## Music ###################
        self.chunk = 1024
        self.time = 0
        self.setNotes = dict()
        self.beats = []
        self.color1 = (125, 0, 0)
        self.color2 = (200, 100, 50)
        self.color3 = (100, 30, 250)
        self.color4 = (50, 220, 10)
        ############## Display ###############
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.camera = cv2.VideoCapture(0)
        self.paused = False
        self.background = None 
        self.margin = 125
        self.leftHand = Hand(self.screen, None, None, None, None)
        self.rightHand = Hand(self.screen, None, None, None, None)
        self.SONG_END = pygame.USEREVENT + 3
        self.lose = False
        self.createBins()
        self.createTrash()
        self.bonus = 0
        pygame.init()

    def createTrash(self):
        #make trash
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
        #make bins
        trashImage = pygame.image.load("trash.png").convert_alpha()
        trashImage1 = pygame.transform.scale(trashImage, (100, 75))
        recycleImage = pygame.image.load("recycle.png").convert_alpha()
        recycleImage1 = pygame.transform.scale(recycleImage, (100, 75))
        compostingImage = pygame.image.load("composting.png").convert_alpha()
        compostingImage1 = pygame.transform.scale(compostingImage, (100, 75))
        self.recycle = Bin(self.screen, self.width//6, 
        self.height -75, recycleImage1)
        self.trash = Bin(self.screen, self.width//2, 
        self.height - 75  , trashImage1)
        self.composting = Bin(self.screen, 5*self.width//6, 
        self.height -75, compostingImage1)
    
    def drawBackground(self):
        pygame.draw.rect(self.screen, (0, 0, 0),(0,0,self.width,self.height))

    def checkHand(self):
        #check if hands are clenched
        if (self.leftHand.refArea != None and self.leftHand.area != None and
            self.leftHand.area > 5/6 * self.leftHand.refArea):
            self.leftHand.sign = 1
            self.leftHand.isClenched = False
                
        if (self.rightHand.refArea != None and self.rightHand.area != None and
            self.rightHand.area > 5/6 * self.rightHand.refArea):
            self.rightHand.sign = 1
            self.rightHand.isClenched = False
            

    def findArea(self):
        #find hand area
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

    def createBeats(self, listBeats):
        #make beats
        imageN = random.randint(0, len(self.imageList)-1)
        listBeat = []
        for beat in listBeats:
            beat2 = Beat(self, self.width//2, self.height//2 ,
                self.imageList[imageN], beat)
            self.beats.append(beat2)

    def checkGrabbed(self, hand, bounds, beat):
        #check if hand has grabbed a beat
        beatBounds = (beat.x, beat.y)
        if (hand.refArea != None and hand.area <= 5/6 * hand.refArea and
         not hand.isClenched):
            if (beat.isHit == False):
                if self.boundsIntersect(bounds, beatBounds):
                    hand.isClenched = True
                    beat.isHit == True
                    return True
                else:
                    beat.isHit = False
                    return False
            
        else:
            hand.isClenched = False
        return False

    def boundsIntersect(self, playerBounds, beatBounds):
        #check intersection of point and object
        (x0, y0, x1, y1) = playerBounds
        (a0, b0) = beatBounds 
        return ((x1 >= a0) and (a0 >= x0) and (y1 >= b0) and (b0 >= y0))
    
    def intersect(self, playerBounds, beatBounds):
        #check intersection of two objects
        (x0, y0, x1, y1) = playerBounds
        (a0, b0, a1, b1) = beatBounds 
        return ((x1 >= a0) and (a1 >= x0) and (y1 >= b0) and (b1 >= y0))

    def checkBin(self, beat):
        #create bins
        correctBin = self.imageDict[beat.image]
        beatBounds = self.getBounds(beat)
        binBounds = (correctBin.x - 10 - correctBin.width//2, 
        correctBin.y - 10 - correctBin.height//2,
        correctBin.x + correctBin.width//2 + 10, 
        correctBin.y + correctBin.height//2 + 10)
        if self.intersect(binBounds,beatBounds):          
            return True
        return False

    def checkIntersection(self):
        #check intersection of hands and beats
        leftHBounds = (self.leftHand.x0, self.leftHand.y0, self.leftHand.x1,
        self.leftHand.y1)
        rightHBounds = (self.rightHand.x0, self.rightHand.y0, self.rightHand.x1,
        self.rightHand.y1)
        for beat in self.beats:
            if self.checkGrabbed(self.leftHand, 
                leftHBounds, beat):
                beat.x = (self.leftHand.x0 + self.leftHand.x1)//2
                beat.y = (self.leftHand.y0 + self.leftHand.y1)//2
                if self.checkBin(beat):
                    self.score += 10
                    self.beats.remove(beat)
                break
            if self.checkGrabbed(self.rightHand, 
                rightHBounds, beat):
                beat.x = (self.rightHand.x0 + self.rightHand.x1)//2
                beat.y = (self.rightHand.y0 + self.rightHand.y1)//2
                if self.checkBin(beat):
                    self.score += 10
                    self.beats.remove(beat)
                break
            
    
    def textDraw(self):
        #draw score
        font = pygame.font.SysFont("comicsansms", 25)
        color = (0, 128, 0)
        text = font.render(f"Score: {self.score}", True, color)
        self.screen.blit(text, (self.margin//2, self.margin//2))
    
    def redrawAll(self):
        #draw everything
        self.drawBackground()
        self.trash.draw()
        self.recycle.draw()
        self.composting.draw()
        
        for beat in self.beats:
            beat.draw()
        self.leftHand.draw()
        self.rightHand.draw()
        if (self.time < 10):
            font = pygame.font.SysFont("comicsansms", 32)
            color = (0, 128, 0)
            text = font.render(f"Please keep hands steady", True, color)
            (x, h, w,h) = text.get_rect()
            self.screen.blit(text, 
            (self.width//2 - w//2, self.height//2 - h//2))
        self.textDraw()
        pygame.display.update()  
    
    def getBounds(self, obj):
        #get bounds of an object
        return (obj.x - obj.width//2, obj.y - obj.height//2, 
        obj.x + obj.width//2, obj.y + obj.height//2)
    
    def moveBeats(self):
        #make the beats move
        beatsRemoved = set()
        num = random.randint(-10,10)
        for beat in self.beats:
            if beat.num == 1:
                beat.x -= 20
                beat.y += num
            elif beat.num == 2:
                beat.x += 20
                beat.y += num
            elif beat.num == 3:
                beat.y -= 10 + num
                beat.x -= 10
            elif beat.num == 4:
                beat.y -= 10 + num
                beat.x += 10
        for beat in self.beats:
           
            (x0, y0, x1, y1) = self.getBounds(beat)
            if x1 < 0 or y0 < 0 or x0 > self.width or y1 > self.height:
                beatsRemoved.add(beat)
        self.beats = list(set(self.beats) - beatsRemoved)

    def timerFired(self):
        #do every timer fired, update area
        if not self.paused:
            self.findArea()
            self.checkHand()
            if (self.time - 10) * 3.5 in self.setNotes:
                self.createBeats(self.setNotes[(self.time - 10) * 3.5])
            if self.time % 2 == 0:
                self.moveBeats()
            self.checkIntersection()
            self.redrawAll()

    def getEvent(self):
        #see if user presses escape key or song ends
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False # esc to quit   
                    return (0, self.score)   
                if event.key == pygame.K_p:
                    if self.paused == False:
                        self.paused = True
                        pygame.mixer.music.pause()
                    else:
                        self.paused = False
                        pygame.mixer.music.unpause()
                    return "p"
            elif event.type == self.SONG_END:
                self.running = False
                return (1, self.score)
        return (None, None)

    def runTime(self):
        #general funciton
        result = self.getEvent()
        self.timerFired()
        return result

    def run(self):
        #main running function
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
        


    def createFile(self):
        #makes beat dictionary
        self.time1 = 0
        
        wf = wave.open(self.soundFile, 'rb')
        data = wf.readframes(self.chunk)
        self.fRate = wf.getframerate()
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


    def analyzeData(self, data, energySum1, energySum2, energySum3, energySum4):
        #analyze music for beats
        data_int = np.frombuffer(data, dtype = np.int16)
        fftdata0 = np.fft.rfft(data_int)
        fftdata0 = [abs(fftdata0.real[data]) for data in range(0, 
        len(fftdata0.real), 2)]
        range1 = len(fftdata0)//4
        range2 = len(fftdata0)//2
        range3 = len(fftdata0)//4 * 3
        local1 = []
        local2 = []
        local3 = []
        local4 = []
        if self.time1 == 8 or self.time1 % 8 == 0:
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
            local1a, beat1 = self.calcBeat(local1, energySum1, 1)
            local2a, beat2 = self.calcBeat(local2, energySum2, 2)
            local3a, beat3 = self.calcBeat(local3, energySum3, 3)
            local4a, beat4 = self.calcBeat(local4, energySum4, 4)
            self.findGreatest(local1a, beat1, local2a, beat2, local3a, beat3, 
            local4a, beat4)

    def checkLength(self, energySum):
        #check to make sure beat history is short enough
        if (len(energySum) > self.chunk//2):
            energySum.pop(0)
        return energySum

    def findGreatest(self, local1, beat1, local2, beat2, local3, beat3, 
            local4, beat4):
            #find a beat to output
        localList = [(local1,beat1), (local2, beat2), 
        (local3,beat3), (local4,beat4)]
        setBeats = set()
        beatNum = random.randint(0, 3)
        self.setNotes[self.time1] = {localList[beatNum][1]}

    #math logic from:
    #http://archive.gamedev.net/archive/reference/programming/features/beatdetection/
    def calcBeat(self, local, fftdata1, num):
        #calc if particular segment is a beat
        time2 = self.time1//32
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

        var = np.sqrt(np.var(energySum))
        sensitivity = -0.00257 * var + 1.65
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
        #detect user
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
                pygame.mixer.music.pause()
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
            pygame.mixer.music.pause()
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

    def playMusic(self, musicFile, loop):
        if (self.running == True):
            pygame.mixer.pre_init(frequency=44100, size=-16, buffer=2096)
            pygame.mixer.music.set_endevent(self.SONG_END)
            pygame.mixer.music.load(musicFile)
            pygame.mixer.music.play(loops = loop, start = 0.0)
            pygame.mixer.fadeout(1000)
        else:
            pygame.mixer.music.stop()

