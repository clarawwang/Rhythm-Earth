#finds all the songs in the folder of the program

import os.path
from os import path
import string


#modified from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html 
def findSongs(suffix='.wav'):
    #find all wav files in directory
    songList = []
    for file in os.listdir():
        if file.endswith(suffix):
            songList.append(file)
    return songList

