#-coding:utf-8
import os,time
import pyautogui as pag
import pyperclip as ppc


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def paste(str):
    pag.hotkey('ctrl', 'a')
    time.sleep(0.5)
    ppc.copy(str)
    time.sleep(0.5)
    pag.hotkey('ctrl', 'v')

def splitTime(str,type):
    times = []
    strs = str.split("-")
    if is_number(strs[2]):
        times.append(getTime(strs[1], type)[0])
        times.append(getTime(strs[2], type)[1])
    else:
        times = getTime(strs[1], type)
    return times

def secTotime(seconds):
    h = int(seconds/3600)
    m = int((seconds%3600)/60)
    s = seconds%60
    if h < 10:
        strh = "0"+str(h)
    else:
        strh = str(h)
    if m < 10:
        strm = "0"+str(m)
    else:
        strm = str(m)
    if s < 10:
        strs = "0"+str(s)
    else:
        strs = str(s)

    time = strh+":"+strm+":"+strs
    return time

def getTime(time,type):
    times = []
    x = 10
    y = 5
    if type == "list":
        x = 20
        y = 20
    h = int(time[0:2])
    m = int(time[2:4])
    s = int(time[4:6])
    seconds1 = h * 3600 + m * 60 + s - x
    seconds2 = h * 3600 + m * 60 + s + y
    time1 = secTotime(seconds1)
    time2 = secTotime(seconds2)
    times.append(time1)
    times.append(time2)
    return times


def fileList(file_dir,type):
    for root, dirs, files in os.walk(file_dir):
        if type == 1:
            return dirs
        if type == 2:
            return files
    return list

def mkdir(dirPath):
    if os.path.exists(dirPath) == False:
        os.makedirs(dirPath)
        return 1
    else:
        return 2

def rmdir(dirPath):
    if os.path.exists(dirPath) == False:
        return 1
    else:
        os.system("rmdir /s/q " + dirPath)
        return 2

def getPosition():
    x, y = pag.position()
    pos=[]
    pos.append(x)
    pos.append(y)
    return pos
def addPos(lineEdit,positions):
    list = []
    pos = lineEdit.split(",")
    list.append(int(pos[0]))
    list.append(int(pos[1]))
    positions.append(list)
    return positions


def getScreenshot(x,y):
    im = pag.screenshot()
    scr = im.getpixel((x,y))
    return scr

def isScreenshot(x,y,scr):
    flag = pag.pixelMatchesColor(x, y,scr)
    return flag


def doWork(dirPath,positions,dirname,times,scr):
    pag.click(positions[0][0], positions[0][1], button='left')
    time.sleep(0.3)
    pag.click(positions[1][0], positions[1][1], button='left')
    time.sleep(0.3)
    pag.doubleClick(positions[2][0], positions[2][1])
    time.sleep(0.3)
    paste(dirPath + "\\" + dirname)
    time.sleep(0.3)
    pag.click(positions[3][0], positions[3][1])
    time.sleep(0.3)
    paste(times[0])
    time.sleep(0.3)
    pag.click(positions[4][0], positions[4][1])
    time.sleep(0.3)
    paste(times[1])
    time.sleep(0.3)
    pag.click(positions[7][0], positions[7][1], button='left')
    while True:
        time.sleep(1)
        if isScreenshot(positions[6][0],positions[6][1],scr) == False:
            break

    while True:
        time.sleep(1)
        if isScreenshot(positions[6][0],positions[6][1],scr) == True:
            break

def doAVI(positions,dirPath,times,scr):
    pag.click(positions[0][0], positions[0][1], button='left')
    time.sleep(0.3)
    pag.click(positions[1][0], positions[1][1], button='left')
    time.sleep(0.3)
    if dirPath!="":
        pag.doubleClick(positions[2][0], positions[2][1])
        time.sleep(0.3)
        paste(dirPath)
        time.sleep(0.3)
    pag.doubleClick(positions[5][0], positions[5][1])
    time.sleep(0.3)
    pag.click(positions[3][0], positions[3][1])
    time.sleep(0.3)
    paste(times[0])
    time.sleep(0.3)
    pag.click(positions[4][0], positions[4][1])
    time.sleep(0.3)
    paste(times[1])
    time.sleep(0.3)
    pag.click(positions[7][0], positions[7][1], button='left')
    while True:
        time.sleep(1)
        if isScreenshot(positions[6][0],positions[6][1],scr) == False:
            break

    while True:
        time.sleep(1)
        if isScreenshot(positions[6][0],positions[6][1],scr) == True:
            break

def check(dirPath,type):
    times = splitTime(dirPath, type)
    dirs = fileList(dirPath,1)
    for dir in dirs:
        if dir == "h":
            rmdir(dir+"\\h")
        if dir == "QFWANG411":
            dir1s = fileList(dirPath+"\\"+dir, 1)
            f = open(dirPath+"\\"+dir+"\\"+dir1s+"\\clipinfo.ini", "r")
            get = f.read()
            result = get.split('\n')
            f.close()
            if result[2].split("=")[1] == times[0]+"-"+times[1]:
                return True
            else:
                return False
    return False
def checkAVI(dirPath,type):
    times = splitTime(dirPath, type)
    files = fileList(dirPath,2)
    for file in files:
        filesplit = file.split("-")
        if filesplit[2] == times[0] and filesplit[3] == times[1]:
            return True
        else:
            return False


