#main code for running program

import pyaudio
from pygame.locals import *
import pygame
import numpy as np
import wave
import sys
import cv2
import random
from gameAlg import *
from startScreen import *
from loseScreen import *
from learnMode import *
import winScreen 
from chooseSong import *
from highScorePage import *
from helpScreen import *
from findSongs import *
from getRecording import * 

#image citations in the imageCit.txt file

class AllScreen(object):
    def __init__(self, width, height):
        self.running = True
        self.width = width
        self.height = height
        pygame.init()
        self.time = 0
        self.songList = findSongs()
        

    def runner(self):
        while self.running:
            self.inRunning()
            self.time += 1
            startScreen = StartScreen(self.width, self.height)
            menuOpt = startScreen.createStartScreen()
            if self.getEvent == 0:
                return
            if menuOpt == 1:
                chooseMenu = Menu(800, 500, self.songList)
                (songName, diff) = chooseMenu.createMenu()
                if diff != 0:
                    song = songName
                    game = Game(800, 500, song, diff)
                    (resultGame, score, perR, perC, perT) = game.run()
                    if resultGame == 1:
                        loseScreen = LoseScreen(self.width, self.height, score)
                        loseScreen.createScreen()
                    elif resultGame == 2:
                        winScreen1 = winScreen.WinScreen(score, menuOpt, perR
                        , perC, perT)
                        winScreen1.createScreen()
            elif menuOpt == 2:
                learnGame = LearnGame(self.width, self.height, "audsample2.wav")
                (resultLearn, scoreLearn) = learnGame.run()
                if resultLearn == 1:
                    winScreen1 = winScreen.WinScreen(scoreLearn, menuOpt, 0, 0,
                     0)
                    winScreen1.createScreen()
            elif menuOpt == 3:
                helpScreen = HelpScreen(self.width, self.height)
                helpScreen.createHelpScreen()
            elif menuOpt == 4:
                hiScorePage = HighScorePage(self.width, self.height)
                hiScorePage.createHiScoreScreen()
            elif menuOpt == 5:
                recordPage = recordingScreen(self.width, self.height)
                recordPage.run2()
            self.inRunning()
            pygame.time.Clock().tick(43)
        if self.running == False:
            return

    def inRunning(self):
        self.getEvent()
        


    def getEvent(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False # esc to quit  
                    return 0    
                


def main():
    MyApp = AllScreen(800, 500)
    MyApp.runner()
    pygame.display.quit()
    pygame.mixer.quit()
    pygame.quit()

if __name__ == '__main__':
    main()