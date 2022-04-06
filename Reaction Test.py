import pygame as pg
import random
import time
import sys
import os

# RESOLUTION

(width, height) = (400,400)

# COLOURS

white = (255,255,255)
black = (0,0,0)
grey = (200,200,200)
green = (0,255,0)
red = (255,0,0)

# INITIALISE

pg.init()
sc = pg.display.set_mode((width, height))
pg.display.set_caption('Reaction Test')
background = pg.image.load('start.png')
backgroundMenu = pg.image.load('start1.png')
backgroundStart = pg.image.load('start2.png')
menu = pg.image.load('menu.png')
menuBack = pg.image.load('menu1.png')
game = pg.image.load('game.png')
menuBox = pg.draw.rect(sc, white, (295, 0, 110, 100))
startBox = pg.draw.rect(sc, white, (0, 105, 400, 400))
exitBox = pg.draw.rect(sc, black, (312, 120, 72, 72))
resetBox = pg.draw.rect(sc, black, (312, 210, 72, 72))
textFont = pg.font.SysFont("monospace", 24)
exitText = textFont.render("Exit", 3, (black))
resetText = textFont.render("Reset", 3, (black))
dataText = textFont.render("Data", 3, (black))
earlyText = textFont.render("Too fast! 500ms", 1, (black))

print("Welcome to Bradzie's reaction test! \n...\n...\n...")

# AVERAGE METHOD

def average(data, length):
    average = 0
    for x in data:
        x = x // length
        average = average + x
    return average

# LOWEST NUMBER METHOD

def best(data):
    best = 999
    for x in data:
        if x < best:
            best = x
    return best

# FILE HANDLING

try:
    data = open("data.txt", "x")
    print("Data file created!")
    data.close()

except FileExistsError:
    #Check for empty file
    if os.stat("data.txt").st_size == 0:
        print("Data file exists, but is empty! \nStats set to 0!")
        timesPlayed = 0
        lastAverage = 0
        overallAverage = []
        bestReaction = 0

    else:
        #Open file, initialise data
        data = open("data.txt", "r")
        timesPlayed = int(data.readline())
        lastAverage = int(data.readline())
        overallAverage = []
        overallAverageData = data.readline()
        i = 0
        for char in overallAverageData:
            if char == ",":
                charTime = overallAverageData[(i-3):(i)]
                overallAverage.append(int(charTime))
            i = i + 1
        totalAverage = average(overallAverage, len(overallAverage))
        bestReaction = int(data.readline())
        print("File read!")
        timesPlayedText = textFont.render("Times Played: " + str(timesPlayed), 1, (black))
        lastAverageText = textFont.render("Last Average: " + str(lastAverage) + "ms", 1, (black))
        totalAverageText = textFont.render("Total Average: " + str(totalAverage) + "ms", 1, (black))
        bestReactionText = textFont.render("Best Average: " + str(bestReaction) + "ms", 1, (black))
        data.close()

# START

def start():
    turns = 0
    times = []
    react = False

    while turns < 5:
        click = False
        mousePos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                click = True

        if react == False:
            pg.draw.rect(sc, red, (0, 105, 400, 400))
            pg.display.flip()
            timer = random.randint(2,6)
            beginReact = time.time() + timer
            startOfReaction = time.time()
            react = True

        if react == True:
            if time.time() > beginReact:
                pg.draw.rect(sc, green, (0, 105, 400, 400))
                pg.display.flip()
                if click:
                    reactionTime = round(((time.time() - (startOfReaction + timer))* 1000))
                    pg.draw.rect(sc, white, (0, 105, 400, 400))
                    reactText = textFont.render("Nice! " + str(reactionTime) + "ms", 2, (black))
                    remainingText = textFont.render(str(4 - turns) + " to go!", 1, (black))
                    sc.blit(reactText, (width // 8, height // 2))
                    sc.blit(remainingText, (width // 8, (height // 2) + 30))
                    pg.display.flip()
                    times.append(reactionTime)
                    turns = turns + 1
                    time.sleep(1)
                    react = False
            else:
                if click:
                    reactionTime = 500
                    pg.draw.rect(sc, white, (0, 105, 400, 400))
                    sc.blit(earlyText, (width // 8, height // 2))
                    pg.display.flip()
                    times.append(reactionTime)
                    turns = turns + 1
                    print(turns)
                    time.sleep(1)
                    react = False

    returnAverage = average(times, len(times))
    return returnAverage
        
# LOOP

screen = 0
# SCREEN | 0 = START, 1 = MENU, 2 = RUN
while True:
    click = False
    mousePos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            click = True

    if screen == 0:
        if startBox.collidepoint(mousePos):
            sc.blit(backgroundStart, (0, 0))
            if click == True:
                screen = 2
        
        elif menuBox.collidepoint(mousePos):
            sc.blit(backgroundMenu, (0, 0))
            if click == True:
                screen = 1

        else:
            sc.blit(background, (0, 0))

    elif screen == 1:

        if timesPlayed == 0:
            lastAverageText = textFont.render("Last Average: 0", 1, (black))
            totalAverageText = textFont.render("Total Average: 0", 1, (black)) # IMPLEMENT
            bestReactionText = textFont.render("Best Average: 0", 1, (black)) # IMPLEMENT
            timesPlayedText = textFont.render("Times Played: 0", 1, (black))

        if menuBox.collidepoint(mousePos):
            sc.blit(menuBack, (0, 0))
            if click == True:
                screen = 0

        else:
            sc.blit(menu, (0, 0))

        if exitBox.collidepoint(mousePos):
            pg.draw.rect(sc, grey, (312, 120, 72, 72))
            if click == True:
                exit()

        if resetBox.collidepoint(mousePos):
            pg.draw.rect(sc, grey, (312, 210, 72, 72))
            if click == True:
                data = open("data.txt", "w")
                data.close()
                timesPlayed = 0
                lastAverage = 0
                overallAverage = []
                bestReaction = 0
                print("Data reset succesfully!")
                
                
        pg.draw.rect(sc, black, (312, 120, 72, 72), 2)
        pg.draw.rect(sc, black, (312, 210, 72, 72), 2)
        sc.blit(resetText, (314, (height // 2) + 20))
        sc.blit(dataText, (320, (height // 2) + 40))
        sc.blit(exitText, (320, (height // 2) - 60))
        sc.blit(lastAverageText, (10, height // 2))
        sc.blit(totalAverageText, (10, (height // 2) + 30))
        sc.blit(bestReactionText, (10, (height // 2) + 60))
        sc.blit(timesPlayedText, (10, (height // 2) + 90))


    elif screen == 2:
        sc.blit(game, (0, 0))
        lastAverage = start()
        if lastAverage > 999:
            lastAverage = 999

        # update data
        timesPlayed = timesPlayed + 1
        overallAverage.append(lastAverage)
        totalAverage = average(overallAverage, len(overallAverage))
        bestReaction = best(overallAverage)

        #update labels
        timesPlayedText = textFont.render("Times Played: " + str(timesPlayed), 1, (black))
        lastAverageText = textFont.render("Last Average: " + str(lastAverage) + "ms", 1, (black))
        totalAverageText = textFont.render("Total Average: " + str(totalAverage) + "ms", 1, (black))
        bestReactionText = textFont.render("Best Average: " + str(bestReaction) + "ms", 1, (black))


        # update display
        pg.draw.rect(sc, white, (0, 105, 400, 400))
        sc.blit(lastAverageText, (width // 8, height // 2))
        pg.display.flip()

        # update file
        data = open("data.txt", "w")
        print("File opened, updating stats...")
        data.write(str(timesPlayed)+"\n")
        data.write(str(lastAverage)+"\n")
        for charTime in overallAverage:
            data.write(str(charTime)+",")
        data.write("\n"+(str(bestReaction))+"\n")
        data.close()
        print("File closed and saved!")
        
        time.sleep(1)
        screen = 0

    pg.display.flip()
