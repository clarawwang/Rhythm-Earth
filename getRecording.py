#makes screen to take in recordings

import pyaudio
from pygame.locals import *
import pygame
import numpy as np
import wave
import sys



class recordingScreen(object):
    # makes screen for recording page
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.recording = False
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.stream = None
        self.running = True
        pygame.init()
        self.chunk = 1024
        self.bgImage = pygame.image.load("backgroundPic.png").convert_alpha()
        self.r = 50

    def createHeading(self, color):
        #create text
        font2 = pygame.font.SysFont("ammericantypewriterttc", 60)
        text2 = font2.render(f"Double Click to Record", True, color)
        (a, b, w1, h1) = text2.get_rect()
        self.screen.blit(text2, (self.width//2 - w1//2, self.height//4 - h1//2))
    
    def run2(self):
        #main running function
        while self.running:
            color = (255,255,0)
            color2 = (12,184,206)
            pygame.draw.rect(self.screen, 
            (255,255,255),(0,0,self.width,self.height))
            pygame.draw.circle(self.screen, color, 
            (self.width//2, self.height//2), 50)
            bgPic = pygame.transform.scale(self.bgImage, 
            (self.width, self.height))
            self.screen.blit(bgPic,(0, 0,self.width//2, self.height//2))
            self.createHeading(color2)
            pygame.display.update() 
            if self.getEvent() == 0:
                break
            elif self.getEvent() == 1:
                if self.recording == False:
                    self.recording = True
                    time = int(input
                    ("How many seconds do you want to record for?"))
                    self.record(time)

            
        return 
                    

    def intersect(self, bound1, position):
        #find intersection of point and object
        (a0, b0, a1, b1) = bound1
        (x0, y0) = position
        if ((a0<x0) and (a1 > x0) and (b0 < y0) and (b1 > y0)):
            return True
        return False
    
    def getEvent(self):
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN: 
                    #check if clicking the record button
                    (x,y) = pygame.mouse.get_pos()
                    if self.intersect((self.width//2 - 50, self.height//2 - 50,
                    self.width//2 + 50, self.height//2 + 50), (x,y)):
                        pygame.draw.circle(self.screen, (255, 0, 0), 
                        (self.width//2, self.height//2), 50)
                        pygame.display.update()
                        return 1
                    
                if event.type == KEYDOWN:
                    #check if want to exit
                    if event.key == pygame.K_ESCAPE:
                        self.running = False 
                        return 0        
        return 0
        
    #code modified from https://people.csail.mit.edu/hubert/pyaudio/docs/
    def record(self, time1):
        #take in input from microphone
        p = pyaudio.PyAudio()
        print("Start recording")
        frames = []
        format1 = pyaudio.paInt16
        rate1 = 44100
        channels1 = 2
        time1 = time1
        stream = p.open(format= format1,
                channels=channels1,
                rate=rate1,
                input=True,
                frames_per_buffer = self.chunk)
        for i in range(0, int(rate1 / self.chunk * time1)):
            data = stream.read(self.chunk)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate
        print("Stop Recording")
        name = input('''What would you like to name this file?
         Please add a '.wav' ending! ''')
        wf = wave.open(name, 'wb')
        wf.setnchannels(channels1)
        wf.setsampwidth(p.get_sample_size(format1))
        wf.setframerate(rate1)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        self.recording = False
        return


