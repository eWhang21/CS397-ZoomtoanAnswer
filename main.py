# Import everything needed to edit video clips
from moviepy.editor import *
import sys
import os
import os.path
import fnmatch
from os import path

FOLDER_PATH = "/Users/russellmacquarrie/Documents/GitHub/CS397-ZoomtoanAnswer"
zoomFolder = sys.argv[2]

def formatTime(time_string):
    string_list = time_string.split(":")
    temp = 0
    for i in range(len(string_list)):
        temp += int(string_list[i]) * (60**(2-i))
    return temp

def videoStartTimestamp():
    name_list = zoomFolder.split(" ")
    start_time = name_list[1].replace(".", ":")
    return start_time

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


def findStart(f):
    for filename in [sys.argv[1]]:
        line = f.readline()
        if len(line) == 0:
            return 0
        cnt = 1
        while line:
            # print("Line {}: {}".format(cnt, line.strip()))
            #print(line.strip())
            line = f.readline()
            if len(line) == 0:
                return 0
            cnt += 1
            if 'START: ' in line.strip():
                #print("Start found {}".format(line.strip()))
                #print("End found {}".format(line.strip()))
                start_string = "Start found {}".format(line.strip())
                start_time = start_string.split("START:")
                print(start_time[1])
                return(start_time[1])


def findEnd(f):
    for filename in [sys.argv[1]]:
        line = f.readline()
        if len(line) == 0:
            return 0
        cnt = 1
        while line:
            # print("Line {}: {}".format(cnt, line.strip()))
            # print(line.strip())
            line = f.readline()
            if len(line) == 0:
                return 0
            cnt += 1
            if 'END: ' in line.strip():
                #print("End found {}".format(line.strip()))
                end_string = "End found {}".format(line.strip())
                end_time = end_string.split("END:")
                print(end_time[1])
                return end_time[1]


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


def splice(startTime, endTime, name):
    # loading video
    clip = VideoFileClip(findVideo())
    # Splice video
    clip = clip.subclip(startTime, endTime)
    #output new video
    clip.write_videofile(name + ".mp4")

def calc_splice(starter, starts, ends):
    start_time = formatTime(starter)
    for i in range(len(starts)):
        splice((formatTime(starts[i]) -  start_time), (formatTime(ends[i]) - start_time))



if __name__ == '__main__':
    start_time = videoStartTimestamp()
    print("Full FileSTART")
    printFile()
    print("Full FileEND")
    starts = []
    ends = []
    f = open(sys.argv[1])
    while True:
        thisStart = findStart(f)
        thisEnd = findEnd(f)
        if (thisStart == 0) or (thisEnd == 0):
            break
        starts.append(thisStart)
        ends.append(thisEnd)
    print(starts, ends)
    calc_splice(start_time, starts, ends)
    print("all notes")
    printNotes()
    print(findVideo())
    print(sys.path)
   # splice()
