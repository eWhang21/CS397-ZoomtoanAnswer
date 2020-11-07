# Import everything needed to edit video clips
from moviepy.editor import *
import sys
import os
import os.path
import fnmatch
from os import path

FOLDER_PATH = "/Users/estherwhang/Documents/Zoom"
zoomFolder = sys.argv[2]

def videoStartTimestamp():
    start_time = zoomFolder.split(" ")
    print(start_time[1])

def printFile():
    for filename in [sys.argv[1]]:
        with open(filename) as f:
            line = f.readline()
            cnt = 1
            while line:
                print("Line {}: {}".format(cnt, line.strip()))
                #print(line.strip())
                line = f.readline()
                cnt += 1

def printNotes():
    for filename in [sys.argv[1]]:
        with open(filename) as f:
            line = f.readline()
            cnt = 1
            while line:
                # print("Line {}: {}".format(cnt, line.strip()))
                #print(line.strip())
                line = f.readline()
                cnt += 1
                if 'START: ' in line.strip():
                    #print("Start found {}".format(line.strip()))
                    #print("End found {}".format(line.strip()))
                    start_string = "Start found {}".format(line.strip())
                    print(start_string)
                    while 'END: ' not in line:
                        print("Line {}: {}".format(cnt, line.strip()))
                        # print(line.strip())
                        line = f.readline()
                        cnt += 1
                    if 'END: ' in line.strip():
                        end_string = "End found {}".format(line.strip())
                        print(end_string)


def findStart():
    for filename in [sys.argv[1]]:
        with open(filename) as f:
            line = f.readline()
            cnt = 1
            while line:
                # print("Line {}: {}".format(cnt, line.strip()))
                #print(line.strip())
                line = f.readline()
                cnt += 1
                if 'START: ' in line.strip():
                    #print("Start found {}".format(line.strip()))
                    #print("End found {}".format(line.strip()))
                    start_string = "Start found {}".format(line.strip())
                    start_time = start_string.split("START:")
                    print(start_time[1])

def findEnd():
    for filename in [sys.argv[1]]:
        with open(filename) as f:
            line = f.readline()
            cnt = 1
            while line:
                # print("Line {}: {}".format(cnt, line.strip()))
               # print(line.strip())
                line = f.readline()
                cnt += 1
                if 'END: ' in line.strip():
                    #print("End found {}".format(line.strip()))
                    end_string = "End found {}".format(line.strip())
                    end_time = end_string.split("END:")
                    print(end_time[1])

#retrieve all files in the Zoom directory, searches for input directory, and lists all files so we can access the video
def listDir(dir):
    #list all files/folders in Zoom folder
    #fileNames = os.listdir(dir)
    #for fileName in fileNames:
    #    print(fileName)

    # list all files/folders in input folder (the selected meeting)
    allFileNames = os.listdir(zoomFolder)
    #print(allFileNames)
    return allFileNames

def findVideo():
    list = listDir(FOLDER_PATH)
    counter = 0
    for i in list:
        #if ".mp4" in i:
        if fnmatch.fnmatch(i, '*.mp4'):
            return i
        counter+=1
        #if ".mp4" in list[i]:
        #    return list[i]

startTime = 4
endTime = 10

def splice():
    # loading video
    clip = VideoFileClip(findVideo())
    # Splice video
    clip = clip.subclip(startTime, endTime)
    #output new video
    clip.write_videofile("Done.mp4")


if __name__ == '__main__':
    print(videoStartTimestamp())
    print("Full FileSTART")
    printFile()
    print("Full FileEND")
    findStart()
    findEnd()
    print("all notes")
    printNotes()
    print(findVideo())
    print(sys.path)
   # splice()




