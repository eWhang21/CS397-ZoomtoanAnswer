# Import everything needed to edit video clips
from moviepy.editor import *
import sys
import os
import os.path
import fnmatch
import cgi
from os import path

#for exporting txt file
#import os
import io
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload



ZOOM_FOLDER_PATH = "/Users/russellmacquarrie/Documents/Zoom"
DOWNLOADS_FOLDER_PATH = "/Users/russellmacquarrie/Downloads"
SCRIPT_PATH = "file:///Users/russellmacquarrie/Documents/Github/CS397-ZoomtoanAnswer/"
WORKING_DIRECTORY = "/Users/russellmacquarrie/Documents/Github/CS397-ZoomtoanAnswer"
notes_txtfile = sys.argv[1]
lines = [[]]

#input_zoom_folder = sys.argv[2]


#find most recent file within all zoom recording files
def find_most_recent_zoom_folder():
    list = listDir(ZOOM_FOLDER_PATH)
    date_list = []
    time_list = []
    same_day_time_list = []

    for i in list:
        if i != ".DS_Store":
            i_file = i.split(" ")
            date = i_file[0]
            time = i_file[1]
            time_replace = time.replace(".", ":")
            date_list.append(date)
            time_list.append(time_replace)
            time_list = sorted(time_list, reverse=True)

            if date == max(date_list):
                same_day_time_list.append(time)

    #find most recent date: max(date_list)
    #how many times most recent date occured
    if date_list.count(max(date_list)) == 0:
        raise Exception("No files recorded Zoom files exist.")
    if date_list.count(max(date_list)) >= 1:
        for j in list:
            file_split = j.split(" ")
            if file_split[0] == max(date_list) and file_split[1] == max(same_day_time_list):
                return j


def formatTime(time_string):
    string_list = time_string.split(":")
    temp = 0
    for i in range(len(string_list)):
        temp += int(string_list[i]) * (60**(2-i))
    return temp

#find start timestamp of recording from the downloaded zoom recording file
def videoStartTimestamp():
    name_list = find_most_recent_zoom_folder().split(" ")
    start_time = name_list[1].replace(".", ":")
    return start_time

#export txt file from google drive into corresponding (most recent) zoom directory
def exportFile():
    CLIENT_SECRET_FILE = "client_secret_290484746034-g2jo5esvo50gs2ckfenl4c172m8rflps.apps.googleusercontent.com.json"
    API_Name = 'drive'
    API_Version = "v3"
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.metadata']

    service = Create_Service(CLIENT_SECRET_FILE, API_Name, API_Version, SCOPES)

    file_id = ["1p_RVPF0YjMOX1z2XZeStz_wEbt4OqOACy2mjLz4-hls"]
    file_name = [sys.argv[1]]

    for file_id, file_name in zip(file_id, file_name):
        request = service.files().export_media(fileId=file_id, mimeType='text/plain')

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            print("Download Progress {0}".format(status.progress() * 100))

        fh.seek(0)

        most_recent_zoom_folder_path = ZOOM_FOLDER_PATH + "/" + find_most_recent_zoom_folder()

        with open(os.path.join(most_recent_zoom_folder_path, file_name), 'wb') as f:
            f.write(fh.read())
            f.close()

def printFile():
    #f = open(findtxtfile())
    for filename in [sys.argv[1]]:
        with open(findtxtfile()) as f:
            line = f.readline()
            cnt = 1
            while line:
                #print("Line {}: {}".format(cnt, line.strip()))
                print(line.strip())
                line = f.readline()
                cnt += 1

def printNotes():
    for filename in [sys.argv[1]]:
        with open(findtxtfile()) as f:
        #with open(filename) as f:
            line = f.readline()
            cnt = 1
            cnt2 = 0
            lines = [[]]
            while line:
                # print("Line {}: {}".format(cnt, line.strip()))
                #print(line.strip())
                line = f.readline()
                cnt += 1
                if 'START: ' in line.strip():
                    cnt2 += 1
                    lines.append([])
                    #print("Start found {}".format(line.strip()))
                    #print("End found {}".format(line.strip()))
                    start_string = "Start found {}".format(line.strip())
                    print(start_string)
                    while 'END: ' not in line:
                        print("Line {}: {}".format(cnt, line.strip()))
                        # print(line.strip())
                        line = f.readline()
                        lines[cnt2].append([line, "note"])
                        cnt += 1
                    if 'END: ' in line.strip():
                        cnt2 += 1
                        lines.append([])
                        end_string = "End found {}".format(line.strip())
                        print(end_string)
                elif line != '\n':
                    lines[cnt2].append([line, "notnote"])
            return lines


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
                return (start_time[1])


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
    # list all files/folders in input folder (the selected meeting)
    allFileNames = os.listdir(dir)
    #print(allFileNames)
    return allFileNames


#find specific files (returns list: ['/Users/estherwhang/Downloads/Steno1.txt'] )
def find_files(filename, search_path):
    result = []
    # Walking top-down from the root
    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))
    return result

###         find txt file in downloads folder
#def findtxtfile():
#    find_files(notes_txtfile, DOWNLOADS_FOLDER_PATH)
#    return find_files(notes_txtfile, DOWNLOADS_FOLDER_PATH)[0]

###         find txt file in most recent zoom folder
def findtxtfile():
    most_recent_zoom_folder_path = ZOOM_FOLDER_PATH + "/" + find_most_recent_zoom_folder()

    #find_files(notes_txtfile, most_recent_zoom_folder_path)
    #return find_files(notes_txtfile, most_recent_zoom_folder_path)[0]
    return most_recent_zoom_folder_path + "/" + sys.argv[1]

def findVideo(path):
    list = listDir(path + "/" + find_most_recent_zoom_folder())
    counter = 0
    for i in list:
        if fnmatch.fnmatch(i, '*.mp4'):
            return i
        counter+=1

def findVideoPath():
    vidpath = ZOOM_FOLDER_PATH + "/" + find_most_recent_zoom_folder() + "/" + findVideo(ZOOM_FOLDER_PATH)
    return vidpath

def findVidPaths(names, noteNum):
    vidpath = WORKING_DIRECTORY
    paths = []
    list = listDir(vidpath)
    counter = 0
    for j in names:
        for i in list:
            if i.startswith(j):
                paths.append(i)
                counter+=1
            if counter == noteNum:
                return paths



def splice(startTime, endTime, name):
    # loading video
    clip = VideoFileClip(findVideoPath())
    # Splice video
    clip = clip.subclip(startTime, endTime)
    #output new video
    clip.write_videofile(name + ".mp4")

def calc_splice(starter, starts, ends, name):
    start_time = formatTime(starter)
    #for i in range(len(starts)):
    splice((formatTime(starts[i]) - start_time), (formatTime(ends[i]) - start_time), name)

def htmlify(names, lines):
    out = "<head> <link rel='stylesheet' href='layout.css'> </head> <header id=title> Steno </header><p class='head'>"
    lines.pop(0)
    noteNum = len(names)
    paths = tuple(findVidPaths(names, noteNum))
    for eachline in lines:
        if eachline[0][1] == 'note':
            eachline.pop()
            out += "<h2>New Note</h2> <video class=video width='620' height='540' controls id=video> <source src='%s' type='video/mp4'> Your browser does not support the video tag. </video> <p class='notes'>"
        else:
            out += "<h2>New Note</h2> <p class='notes'>"
        for j in eachline:
            out += "<br>" + j[0] + "</br>"
        out += "</p></div>"
    print(out)
    print(paths)
    wrapStringInHTMLMac("Steno", "www.steno.co.uk", out % paths)

def wrapStringInHTMLMac(program, url,  body):
    import datetime
    from webbrowser import open_new_tab

    now = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    filename = program + '.html'
    f = open(filename,'w')

    wrapper = """<html>
    <head>
    <title>%s output - %s</title>
    </head>
    <body><p id=url>URL: <a href=\"%s\">%s</a></p>%s</body>
    </html>"""

    whole = wrapper % (program, now, url, url, body)
    f.write(whole)
    f.close()

    #Change the filepath variable below to match the location of your directory
    filename = SCRIPT_PATH + filename

    open_new_tab(filename)
    return

if __name__ == '__main__':
    exportFile()
    if len(sys.argv) < 2:
        raise Exception("Please enter three arguments: python3 main.py notes.txt_file")
    start_time = videoStartTimestamp()
    # print("Full FileSTART")

    print("Content-type:/html\n\n")
    form = cgi.FieldStorage()
    Title = form.getvalue("Title")
    print(Title)

    # print("Full FileEND")
    starts = []
    ends = []
    counter = 0
    name = ""
    print(findtxtfile())
    f = open(findtxtfile())
    lines = printNotes()
    while True:
        thisStart = findStart(f)
        thisEnd = findEnd(f)
        if (thisStart == 0) or (thisEnd == 0):
            break
        starts.append(thisStart)
        ends.append(thisEnd)
        # print(starts, ends)
    names = []
    for i in range(len(starts)):
        nameFile = str(counter)
        names.append("name"+nameFile)
       #calc_splice(start_time, starts, ends, "name" + nameFile)
        counter += 1
    htmlify(names, lines)

#  python3 main.py Steno1.txt "2020-11-10 15.46.20 Esther Whang's Zoom Meeting 94237206986"
#  python3 main.py Steno1.txt
