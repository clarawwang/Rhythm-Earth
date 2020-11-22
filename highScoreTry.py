#write and input high score file 

import os.path
from os import path
import string

def addHighScore(score):
    #adds a high score to the file if it meets criteria
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
    if len(listScores) == 8:
        for i in range(8):
            if score >= listScores[i]:
                (score, listScores[i]) = (listScores[i], score)
    elif len(listScores) == 0:
        listScores = [score]
    elif len(listScores) < 8:
        smallest = (listScores[len(listScores)- 1])
        bigger = False
        for i in range(len(listScores)):
            if score >= listScores[i]:
                (score, listScores[i]) = (listScores[i], score)
                bigger = True
        if bigger == True:
            listScores.append(smallest)
        else:
            listScores.append(score)
    f = open("hiscore.txt","w+")
    for i in range(min(len(listScores), 8)):
        f.write(f"{listScores[i]} \n" )
    f.close()
    