from PIL import Image
import time
import pyautogui
from pathlib import Path
from PIL import ImageGrab
import math as Math
import keyboard
import os
from colorama import Fore
pyautogui.FAILSAFE = False
#100Y
#163Y
noMoves = 0
path = Path(__file__).parent.absolute()
boxHeight = 0
boxWidth = 0
screenStart = 0
canvasWidth = 600
canvasHeight = 500
board = []
def setup():
    global screenStart
    global boxWidth
    global boxHeight
    pyautogui.screenshot("board.png")
    time.sleep(0.1)
    im = Image.open("board.png")
    pix = im.load()
    yboard = 0
    for y in range(im.height):
        if pix[0, y] == (74, 117, 44):
            yboard = y
            break
    for y in range(yboard, im.height):
        if pix[0, y] != (74, 117, 44):
            yboard = y
            break
    ysave = yboard
    for y in range(yboard, im.height):
        if pix[0, y] != (170, 215, 81):
            yboard = y
            break
    xboard = 0
    for x in range(im.width):
        if pix[x, ysave] != (170, 215, 81):
            xboard = x
            break
    boxHeight = yboard-ysave
    boxWidth = xboard
    screenStart = ysave
    os.remove("board.png")
def checkBox(boardX, boardY, im):
    pix = im.load()
    for y in range(boardY*boxHeight, (boardY*boxHeight)+boxHeight):
        for x in range(boardX*boxWidth, (boardX*boxWidth)+boxWidth):
            if pix[x, y] == (25, 118, 210):
                return "1"
            if pix[x, y] == (56, 142, 60):
                return "2"
            if pix[x, y] == (211, 47, 47):
                return "3"
            if pix[x, y] == (123, 31, 162):
                return "4"
            if pix[x, y] == (255, 143, 0):
                return "5"
            if pix[x, y] == (0, 151, 167):
                return "6"
    for y in range(boardY*boxHeight, (boardY*boxHeight)+boxHeight):
        for x in range(boardX*boxWidth, (boardX*boxWidth)+boxWidth):
            if pix[x, y] == (170, 215, 81): # Nothing / Not uncovered
                return "N"
            if pix[x, y] == (162, 209, 73): # Nothing / Not uncovered
                return "N"
            if pix[x, y] == (215, 184, 153): # Uncovered
                return "U"
            if pix[x, y] == (229, 194, 159): # Uncovered
                return "U"
def makeBoard():
    global board
    pyautogui.click(400, 500)
    pyautogui.moveTo(0, 0)
    im = ImageGrab.grab(bbox=(0, screenStart, canvasWidth, screenStart+canvasHeight))
    for y in range(Math.floor(canvasHeight/boxHeight)):
        board.append([])
        for x in range(Math.floor(canvasWidth/boxWidth)):
            board[y].append(checkBox(x, y, im))
def changeBoard():
    global board
    pyautogui.moveTo(0, 0)
    im = ImageGrab.grab(bbox=(0, screenStart, canvasWidth, screenStart+canvasHeight))
    for y in range(Math.floor(canvasHeight/boxHeight)):
        for x in range(Math.floor(canvasWidth/boxWidth)):
            if board[y][x] != "F":
                board[y][x] = checkBox(x, y, im)
def countAroundPoint(find, x, y):
    count = 0
    if y != 0:
        if x != 0:
            if board[y-1][x-1] == find: count += 1
        if board[y-1][x] == find: count += 1
        if x != (Math.floor(canvasWidth/boxWidth))-1:
            if board[y-1][x+1] == find: count += 1
    if x != 0:
        if board[y][x-1] == find: count += 1
    if x != (Math.floor(canvasWidth/boxWidth))-1:
        if board[y][x+1] == find: count += 1
    if y != (Math.floor(canvasHeight/boxHeight))-1:
        if x != 0:
            if board[y+1][x-1] == find: count += 1
        if board[y+1][x] == find: count += 1
        if x != (Math.floor(canvasWidth/boxWidth))-1:
            if board[y+1][x+1] == find: count += 1
    return count
def findPoint(find, x, y):
    if y != 0:
        if x != 0:
            if board[y-1][x-1] == find: return [x-1, y-1]
        if board[y-1][x] == find: return [x, y-1]
        if x != (Math.floor(canvasWidth/boxWidth))-1:
            if board[y-1][x+1] == find: return [x+1, y-1]
    if x != 0:
        if board[y][x-1] == find: return [x-1, y]
    if x != (Math.floor(canvasWidth/boxWidth))-1:
        if board[y][x+1] == find: return [x+1, y]
    if y != (Math.floor(canvasHeight/boxHeight))-1:
        if x != 0:
            if board[y+1][x-1] == find: return [x-1, y+1]
        if board[y+1][x] == find: return [x, y+1]
        if x != (Math.floor(canvasWidth/boxWidth))-1:
            if board[y+1][x+1] == find: return [x+1, y+1]
    return -1
def guess():
    global board, noMoves
    m = False
    for y in range(Math.floor(canvasHeight/boxHeight)):
        for x in range(Math.floor(canvasWidth/boxWidth)):
            # Skip
            if board[y][x] == "U":
                continue
            if board[y][x] == "N":
                continue
            # = 1 =
            if board[y][x] == "1":
                if countAroundPoint("N", x, y) == 1 and countAroundPoint("F", x, y) == 0:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
            # = 2 =
            if board[y][x] == "2":
                if countAroundPoint("N", x, y) == 1 and countAroundPoint("F", x, y) == 1:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 2 and countAroundPoint("F", x, y) == 0:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
            # = 3 =
            if board[y][x] == "3":
                if countAroundPoint("N", x, y) == 3 and countAroundPoint("F", x, y) == 0:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 2 and countAroundPoint("F", x, y) == 1:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 1 and countAroundPoint("F", x, y) == 2:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
            # = 4 =
            if board[y][x] == "4":
                if countAroundPoint("N", x, y) == 4 and countAroundPoint("F", x, y) == 0:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 3 and countAroundPoint("F", x, y) == 1:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 2 and countAroundPoint("F", x, y) == 2:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 1 and countAroundPoint("F", x, y) == 3:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
            # = 5 =
            if board[y][x] == "5":
                if countAroundPoint("N", x, y) == 5 and countAroundPoint("F", x, y) == 0:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 4 and countAroundPoint("F", x, y) == 1:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 3 and countAroundPoint("F", x, y) == 2:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 2 and countAroundPoint("F", x, y) == 3:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 1 and countAroundPoint("F", x, y) == 4:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
            # = 6 =
            if board[y][x] == "5":
                if countAroundPoint("N", x, y) == 6 and countAroundPoint("F", x, y) == 0:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 5 and countAroundPoint("F", x, y) == 1:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 4 and countAroundPoint("F", x, y) == 2:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 3 and countAroundPoint("F", x, y) == 3:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 2 and countAroundPoint("F", x, y) == 4:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
                if countAroundPoint("N", x, y) == 1 and countAroundPoint("F", x, y) == 5:
                    board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "F"
    click = []
    for y in range(Math.floor(canvasHeight/boxHeight)):
        for x in range(Math.floor(canvasWidth/boxWidth)):
            if board[y][x] == "U":
                continue
            if board[y][x] == "N":
                continue
            if board[y][x] == "1":
                if countAroundPoint("F", x, y) == 1:
                    for i in range(8):
                        if findPoint("N", x, y) != -1:
                            click.append([findPoint("N", x, y)[0], findPoint("N", x, y)[1]])
                            board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "U"
            if board[y][x] == "2":
                if countAroundPoint("F", x, y) == 2:
                    for i in range(8):
                        if findPoint("N", x, y) != -1:
                            click.append([findPoint("N", x, y)[0], findPoint("N", x, y)[1]])
                            board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "U"
            if board[y][x] == "3":
                if countAroundPoint("F", x, y) == 3:
                    for i in range(8):
                        if findPoint("N", x, y) != -1:
                            click.append([findPoint("N", x, y)[0], findPoint("N", x, y)[1]])
                            board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "U"
            if board[y][x] == "4":
                if countAroundPoint("F", x, y) == 4:
                    for i in range(8):
                        if findPoint("N", x, y) != -1:
                            click.append([findPoint("N", x, y)[0], findPoint("N", x, y)[1]])
                            board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "U"
            if board[y][x] == "5":
                if countAroundPoint("F", x, y) == 5:
                    for i in range(8):
                        if findPoint("N", x, y) != -1:
                            click.append([findPoint("N", x, y)[0], findPoint("N", x, y)[1]])
                            board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "U"
            if board[y][x] == "6":
                if countAroundPoint("F", x, y) == 6:
                    for i in range(8):
                        if findPoint("N", x, y) != -1:
                            click.append([findPoint("N", x, y)[0], findPoint("N", x, y)[1]])
                            board[findPoint("N", x, y)[1]][findPoint("N", x, y)[0]] = "U"
    for c in click:
        pyautogui.click(c[0]*boxWidth+5, c[1]*boxHeight+screenStart+5)
        m = True
        noMoves = 0
    if not m:
        noMoves += 1
def solve():
    global noMoves
    makeBoard()
    guess()
    noMoves = 0
    for e in range(50):
        if keyboard.is_pressed("u") or noMoves == 5:
            if noMoves == 5:
                for y in range(len(board)):
                    for x in range(len(board[y])):
                        if board[y][x] == "F":
                            pyautogui.rightClick(x * boxWidth + 5, y * boxHeight + screenStart + 5)
            e = 49
            break
        changeBoard()
        guess()
keyboard.wait("u")
while keyboard.is_pressed("u"): pass
setup()
solve()
