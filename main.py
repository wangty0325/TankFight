from cmu_graphics import *
#from PIL import Image
import PIL.Image
from tank import *
from bullet import *
from elements import *
import os, pathlib
from cmu_graphics import *


filename = 'setup.txt'
with open(filename, encoding='utf-8') as f:
    fileString = f.read()
                
print(fileString)



# CITATION: I got the images of greenTank, redTank, bullet, brick, iron from https://www.bilibili.com/video/BV1bE411P7Uw/?spm_id_from=333.337.search-card.all.click&vd_source=428d71e073aa442b8cecdb51339301ce
# CITATION : I got the music including on-the-road.mp3 and gameStart.mp3 from https://www.zophar.net/music/nintendo-nes-nsf/battle-city

def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

def onAppStart(app):
    app.height = 800
    app.width = 600
    app.tankWidth = 38
    app.tankHeight = 38
    app.player1 = tank(280, 760, speed = 2, direction = 'up', health = 2)
    app.player2 = tank(280, 120, speed = 2, direction = 'down', health = 2)
    # app.playerAI = wtank(0, 0, speed = 2, direction = 'down', health = 2) 

    app.myTankList = [app.player1]
    app.enemyTankList = [app.player2]
    app.backgroundColor = 'black' # black

    app.greenTank = PIL.Image.open('greenTank.png')
    app.greenTank = app.greenTank.resize((38, 38))
    app.greenTank = CMUImage(app.greenTank) # Cast image type to CMUImage to allow for faster drawing
    app.redTank = PIL.Image.open('redTank.png')
    app.redTank = app.redTank.resize((38, 38))
    app.redTank = CMUImage(app.redTank)
    
    app.Map = Map()
    app.Map1 = app.Map.map1()
    app.board = app.Map1.board
    
    app.gameStartScreen = True
    app.gameOverScreen = False
    app.gaming_pvai = False
    app.gaming_pvp = False
    app.gameOverScreen_player1_win = False
    app.gameOverScreen_player2_win = False
    app.gameOverScreen_beatai = False
    app.gameOverScreen_beatbyai = False
    app.ai_test_mode = True
    app.music_start = loadSound('gameStart.mp3')
    app.music_start_counter = 0
    app.music_start_endsignal = False
    app.music_ai = loadSound("on-the-road.mp3")
    app.playing = False
    app.stepsPerSecond = 60
    app.player2_firecounter = 0
    app.player2_canfire = True
    app.player1_firecounter = 0
    app.player1_canfire = True
    app.searchpath_counter = 0
    

    # initialize
    # row, col = int(app.player2.topleft_y/20), int(app.player2.topleft_x/20)
    # (nextD_row, nextD_col), app.player2.fwdpath = app.player2.DFS_getDirection(app.player1, app.Map1.board, row, col, app.Map1.brickList, app.Map1.ironList)
    # print(nextD_row, nextD_col)
    # print(f'initial: fwdpath: {app.player2.fwdpath}')

def redrawAll(app):
    if app.gameStartScreen:
        drawStart(app)
        if not app.music_start_endsignal:
            app.music_start.play()
        else:
            app.music_start.pause()

    elif app.gaming_pvai and not app.gameStartScreen:
        app.music_ai.play(loop = True)
        drawRect(0, 0, app.width, app.height, fill=app.backgroundColor)
        drawPlayersTank(app)
        drawBullets(app)
        app.Map1.drawMap()
        if app.ai_test_mode:
            for i in range(40):
                drawLine(0, i*20, 600, i*20, fill='white', lineWidth = 1)
            for j in range(30):
                drawLine(j*20, 0, j*20, 800, fill='white', lineWidth = 1)
            if app.player2.being:
                for eachstep in app.player2.fwdpath:
                    step_row, step_col = eachstep[0], eachstep[1]
                    drawCircle(step_col*20, step_row*20, 5, fill='red')
                    (last_step_row, last_step_col) = app.player2.fwdpath[(step_row, step_col)]
                    drawCircle(last_step_col*20, last_step_row*20, 5, fill='red')
        drawHealth(app)

    elif app.gaming_pvp and not app.gameStartScreen:
        drawRect(0, 0, app.width, app.height, fill=app.backgroundColor)
        app.Map1.drawMap()
        drawPlayersTank(app)
        drawBullets(app)
        drawHealth(app)
        
        

    elif app.gameOverScreen:
        drawGameOver(app)

def drawHealth(app):
    cx_1 = app.player1.topleft_x + app.tankWidth/2 
    cy_1 = app.player1.topleft_y - 15
    if app.player1.health == 2:
        drawRect(cx_1, cy_1, 60, 10, fill='red', border='white', align='center')
    elif app.player1.health == 1:
        drawRect(cx_1, cy_1, 60, 10, fill='red', border='white', align='center')
        drawRect(cx_1 + 15, cy_1, 30, 10, fill='white', align='center')
    
    cx_2 = app.player2.topleft_x + app.tankWidth/2 
    cy_2 = app.player2.topleft_y - 15
    if app.player2.health == 2:
        drawRect(cx_2, cy_2, 60, 10, fill='red', border='white', align='center')
    elif app.player2.health == 1:
        drawRect(cx_2, cy_2, 60, 10, fill='red', border='white', align='center')
        drawRect(cx_2 + 15, cy_2, 30, 10, fill='white', align='center')

def drawStart(app):
    drawRect(0, 0, 600, 800, fill='black')
    drawLabel('Tank', 300, 150, fill='red', font = 'monospace', size = 100, bold=True)
    drawLabel('Fight', 300, 240, fill='red', font = 'monospace', size = 100, bold=True)
    drawLabel('Player vs AI: Press A', 300, 400, fill = 'white', font='monospace', size = 30, bold=True)
    drawLabel('Player vs Player: Press B', 300, 450, fill = 'white', font='monospace', size = 28, bold = True)
    drawLabel('Instructions', 300, 520, fill='white', font='monospace', size=24, bold=True)
    drawLabel("if you choose PvAI mode, use 'wasd' to control your tank", 300, 600,  font='monospace', size = 14, fill='white')
    drawLabel("use 'space' key to shoot", 300, 620, font='monospace', size = 14, fill='white')
    drawLabel("if you choose PvP mode, player1 uses 'wasd' and player2 uses arrows", 300, 660, font='monospace', size = 14, fill='white')
    drawLabel("use 'enter' key to shoot", 300, 680, font='monospace', size = 14, fill='white')

# Game Over Screen
def drawGameOver(app):
    drawRect(0, 0, 600, 800, fill='black')
    if app.gameOverScreen_player2_win:
        drawLabel('Player2 won the game', app.width/2, app.height/2, size = 50, fill = 'red', font = 'garamond')
    elif app.gameOverScreen_player1_win:
        drawLabel('Player1 won the game', app.width/2, app.height/2, size = 50, fill = 'red', font = 'garamond')
    if app.gameOverScreen_beatai:
        drawLabel('You won the game', app.width/2, app.height/2, size = 50, fill = 'red', font = 'garamond')
    elif app.gameOverScreen_beatbyai:
        drawLabel('Game Over', app.width/2, app.height/2, size = 60, fill = 'red', font = 'garamond')
        drawLabel('You lost the game', 300, 600, font = 'monospace', fill='white', size=20)

def drawBullets(app):
    for myTank in app.myTankList:
        for bullet in myTank.bullets:
            if bullet.being:
                bullet.drawBullet()
    
    for enemyTank in app.enemyTankList:
        for bullet in enemyTank.bullets:
            if bullet.being:
                bullet.drawBullet()

def onStep(app):
    if app.gameStartScreen:
        if not app.music_start_endsignal:
            app.music_start_counter += 1
        if app.music_start_counter == 360:
            app.music_start_endsignal = True
            
    # PvP mode
    if app.gaming_pvp:

        app.player1.speed=4
        app.player2.speed=4
        if not app.player1_canfire:
            app.player1_firecounter += 1
        if app.player1_firecounter == 10:
            app.player1_canfire = True
            app.player1_firecounter = 0
        # check if ai can fire
        if not app.player2_canfire:
            app.player2_firecounter += 1
        if app.player2_firecounter == 10:
            app.player2_canfire = True
            app.player2_firecounter = 0
        # check who won the game
        if not app.player1.being:
            app.gaming_pvp = False
            app.gameOverScreen_player2_win = True
            app.gameOverScreen = True
        if not app.player2.being:
            app.gaming_pvp = False
            app.gameOverScreen_player1_win = True
            app.gameOverScreen = True

        for myTank in app.myTankList:
            for bullet in myTank.bullets:
                bullet.bulletDestroyTank(app.enemyTankList)
                for brick in app.Map1.brickList:
                    if bullet.isBulletCollideWithBrick(brick):  # bullet collides with the brick
                        bullet.being = False
                        brick.being = False
                        app.Map1.board[brick.row][brick.col] = 0
                else:
                    if bullet.being:
                        bullet.move()

        for enemyTank in app.enemyTankList:
            for bullet in enemyTank.bullets:
                bullet.bulletDestroyTank(app.myTankList)  # bullet shoots myTank
                for brick in app.Map1.brickList:
                    if bullet.isBulletCollideWithBrick(brick):  # bullet collides with the brick
                        bullet.being = False
                        brick.being = False
                        app.Map1.board[brick.row][brick.col] = 0
                else:
                    if bullet.being:
                        bullet.move()


    # PvAI mode
    elif app.gaming_pvai:

        if not app.player1.being:
            app.gaming_pvai = False
            app.gameOverScreen = True
            app.gameOverScreen_beatbyai = True
        elif not app.player2.being:
            app.gaming_pvai = False
            app.gameOverScreen = True
            app.gameOverScreen_beatai = True

        # check if player1 can fire 
        if not app.player1_canfire:
            app.player1_firecounter += 1
        if app.player1_firecounter == 10:
            app.player1_canfire = True
            app.player1_firecounter = 0
        # check if ai can fire
        if not app.player2_canfire:
            app.player2_firecounter += 1
        if app.player2_firecounter == 10:
            app.player2_canfire = True
            app.player2_firecounter = 0

        # check collision between bullets and cells
        for myTank in app.myTankList:
            for bullet in myTank.bullets:
                bullet.bulletDestroyTank(app.enemyTankList)
                for brick in app.Map1.brickList:
                    if bullet.isBulletCollideWithBrick(brick):  # bullet collides with the brick
                        bullet.being = False
                        brick.being = False
                        app.Map1.board[brick.row][brick.col] = 0
                else:
                    if bullet.being:
                        bullet.move()
        for enemyTank in app.enemyTankList:
            for bullet in enemyTank.bullets:
                bullet.bulletDestroyTank(app.myTankList)  # bullet shoots myTank
                for brick in app.Map1.brickList:
                    if bullet.isBulletCollideWithBrick(brick):  # bullet collides with the brick
                        bullet.being = False
                        brick.being = False
                        app.Map1.board[brick.row][brick.col] = 0
                else:
                    if bullet.being:
                        bullet.move()
        
        # AI auto movement parameters
        row, col = int(app.player2.topleft_y/20), int(app.player2.topleft_x/20)
        print(f'here: {row, col}')

        # search path every one second
        if app.searchpath_counter % 100 == 0:
            
            nextD_cell, app.player2.fwdpath = app.player2.DFS_getDirection(app.player1, app.Map1.board, row, col, app.Map1.brickList, app.Map1.ironList)
            # the direction of next move
            nextD_row, nextD_col = nextD_cell[0], nextD_cell[1]
            print(f'move:{nextD_row, nextD_col}') 
        print(f'fwdpath: {app.player2.fwdpath}')
        print(f'beforemove{app.player2.topleft_x, app.player2.topleft_y}')
        print(f'rightcell:{app.Map1.board[row][col+1]}')

        (nextD_row, nextD_col) = (1,0)
        if (row, col) not in app.player2.fwdpath:
            nextstep_row, nextstep_col = row, col
        else:
            nextstep_row, nextstep_col = app.player2.fwdpath[(row, col)]
        drow, dcol = nextstep_row - row, nextstep_col - col
        # ai tank automatically changes its direction and moves


        print(f'check:{row,col}:{nextstep_row, nextstep_col}:{drow, dcol}')
        if (drow, dcol) == (1, 0):
            app.player2.direction = 'down'
            app.player2.topleft_y += app.player2.speed
        elif (drow, dcol) == (-1, 0):
            app.player2.direction = 'up'
            app.player2.topleft_y -= app.player2.speed
        elif (drow, dcol) == (0, 1):
            app.player2.direction = 'right'
            app.player2.topleft_x += app.player2.speed
        elif (drow, dcol) == (0, -1):
            app.player2.direction = 'left'
            app.player2.topleft_x -= app.player2.speed

        targetRow, targetCol = int(app.player1.topleft_y/20), int(app.player1.topleft_x/20)
        row_minimum = getCrossLine_row_min(targetRow, targetCol, app.Map1.board, row_min = targetRow) 
        row_maximum = getCrossLine_row_max(targetRow, targetCol, app.Map1.board, row_max = targetRow)
        col_minimum = getCrossLine_col_min(targetRow, targetCol, app.Map1.board, col_min = targetCol) 
        col_maximum = getCrossLine_col_max(targetRow, targetCol, app.Map1.board, col_max = targetCol)
        if ((col==targetCol and 
            row_minimum <= row <= row_maximum)):
            if row <= targetRow:
                app.player2.direction = 'down'
                if app.player2_canfire:
                    app.player2.fire()
                    app.player2_canfire = False
            else:
                app.player2.direction = 'up'
                if app.player2_canfire:
                    app.player2.fire()
                    app.player2_canfire = False

        elif(row==targetRow and
            col_minimum <= col <= col_maximum):
            if col <= targetCol:
                app.player2.direction = 'right'
                if app.player2_canfire:
                    app.player2.fire()
                    app.player2_canfire = False
            else:
                app.player2.direction = 'left'
                if app.player2_canfire:
                    app.player2.fire()
                    app.player2_canfire = False
        
        app.searchpath_counter += 1
        print(f'aftermove{app.player2.topleft_x, app.player2.topleft_y}')

        # nextmove_row, nextmove_col = app.player2.fwdpath[(app.player2.row, app.player2.col)]
        # app.player2.automove(nextD_row, nextD_col)




def drawPlayersTank(app):
    for myTank in app.myTankList:
        if myTank.being:
            if myTank.direction == 'up':
                drawImage(app.greenTank, myTank.topleft_x, myTank.topleft_y, rotateAngle = 0)
            elif myTank.direction == 'right':
                drawImage(app.greenTank, myTank.topleft_x, myTank.topleft_y, rotateAngle = 90)
            elif myTank.direction == 'down':
                drawImage(app.greenTank, myTank.topleft_x, myTank.topleft_y, rotateAngle = 180)
            elif myTank.direction == 'left':
                drawImage(app.greenTank, myTank.topleft_x, myTank.topleft_y, rotateAngle = 270)

    for enemyTank in app.enemyTankList:
        if enemyTank.being:
            if enemyTank.direction == 'up':
                drawImage(app.redTank, enemyTank.topleft_x, enemyTank.topleft_y, rotateAngle = 0)
            elif enemyTank.direction == 'right':
                drawImage(app.redTank, enemyTank.topleft_x, enemyTank.topleft_y, rotateAngle = 90)
            elif enemyTank.direction == 'down':
                drawImage(app.redTank, enemyTank.topleft_x, enemyTank.topleft_y, rotateAngle = 180)
            elif enemyTank.direction == 'left':
                drawImage(app.redTank, enemyTank.topleft_x, enemyTank.topleft_y, rotateAngle = 270)
            

def onKeyHold(app, keys):
    for myTank in app.myTankList:
        if myTank.being:
            if 'w' in keys:
                # make a copy tank to check whether it will collide after the move
                frontierTank = tank(myTank.topleft_x, myTank.topleft_y - myTank.speed, myTank.speed, myTank.direction, myTank.health)
                # change the direction
                if myTank.direction != 'up':
                    myTank.direction = 'up'
                # check is move legal : not beyond the boundary and not colliding with bricks and irons
                if frontierTank.topleft_y > 0 and not frontierTank.isCollide(app.Map1.brickList, app.Map1.ironList):
                    myTank.prev_topleft_x = myTank.topleft_x
                    myTank.prev_topleft_y = myTank.topleft_y
                    myTank.topleft_y -= myTank.speed  # move
                    
            elif 's' in keys:
                frontierTank = tank(myTank.topleft_x, myTank.topleft_y + myTank.speed, myTank.speed, myTank.direction, myTank.health)
                if myTank.direction != 'down':
                    myTank.direction = 'down'
                if frontierTank.topleft_y < 800 - app.tankWidth and not frontierTank.isCollide(app.Map1.brickList, app.Map1.ironList):
                    myTank.prev_topleft_x = myTank.topleft_x
                    myTank.prev_topleft_y = myTank.topleft_y
                    myTank.topleft_y += myTank.speed
                
            elif 'a' in keys:
                frontierTank = tank(myTank.topleft_x - myTank.speed, myTank.topleft_y, myTank.speed, myTank.direction, myTank.health)
                if myTank.direction != 'left':
                    myTank.direction = 'left'
                if frontierTank.topleft_x > 0 and not frontierTank.isCollide(app.Map1.brickList, app.Map1.ironList):
                    myTank.prev_topleft_x = myTank.topleft_x
                    myTank.prev_topleft_y = myTank.topleft_y
                    myTank.topleft_x -= myTank.speed
            elif 'd' in keys:
                frontierTank = tank(myTank.topleft_x + myTank.speed, myTank.topleft_y, myTank.speed, myTank.direction, myTank.health)
                if myTank.direction != 'right':
                    myTank.direction = 'right'
                if frontierTank.topleft_x < 600 - app.tankWidth and not frontierTank.isCollide(app.Map1.brickList, app.Map1.ironList):
                    myTank.prev_topleft_x = myTank.topleft_x
                    myTank.prev_topleft_y = myTank.topleft_y
                    myTank.topleft_x += myTank.speed

    for enemyTank in app.enemyTankList:
        if enemyTank.being:     
            if 'up' in keys:
                frontierTank = tank(enemyTank.topleft_x, enemyTank.topleft_y - enemyTank.speed, enemyTank.speed, enemyTank.direction, enemyTank.health)
                # change the direction
                if enemyTank.direction != 'up':
                    enemyTank.direction = 'up'
                # check not beyond boundary or colliding with cells
                if frontierTank.topleft_y > 0 and not frontierTank.isCollide(app.Map1.brickList, app.Map1.ironList):
                    enemyTank.prev_topleft_x = enemyTank.topleft_x
                    enemyTank.prev_topleft_y = enemyTank.topleft_y
                    enemyTank.topleft_y -= enemyTank.speed
            elif 'down' in keys:
                frontierTank = tank(enemyTank.topleft_x, enemyTank.topleft_y + enemyTank.speed, enemyTank.speed, enemyTank.direction, enemyTank.health)
                # change the direction
                if enemyTank.direction != 'down':
                    enemyTank.direction = 'down'
                if frontierTank.topleft_y < 800 - app.tankWidth  and not frontierTank.isCollide(app.Map1.brickList, app.Map1.ironList):
                    enemyTank.prev_topleft_x = enemyTank.topleft_x
                    enemyTank.prev_topleft_y = enemyTank.topleft_y
                    enemyTank.topleft_y += enemyTank.speed
                
            elif 'left' in keys:
                frontierTank = tank(enemyTank.topleft_x - enemyTank.speed, enemyTank.topleft_y, enemyTank.speed, enemyTank.direction, enemyTank.health)
                # change the direction
                if enemyTank.direction != 'left':
                    enemyTank.direction = 'left'
                if frontierTank.topleft_x > 0 and not frontierTank.isCollide(app.Map1.brickList, app.Map1.ironList):
                    enemyTank.prev_topleft_x = enemyTank.topleft_x
                    enemyTank.prev_topleft_y = enemyTank.topleft_y
                    enemyTank.topleft_x -= enemyTank.speed
            elif 'right' in keys:
                frontierTank = tank(enemyTank.topleft_x + enemyTank.speed, enemyTank.topleft_y, enemyTank.speed, enemyTank.direction, enemyTank.health)
                if enemyTank.direction != 'right':
                    enemyTank.direction = 'right'
                if frontierTank.topleft_x < 600 - app.tankWidth and not frontierTank.isCollide(app.Map1.brickList, app.Map1.ironList):
                    enemyTank.prev_topleft_x = enemyTank.topleft_x
                    enemyTank.prev_topleft_y = enemyTank.topleft_y
                    enemyTank.topleft_x += enemyTank.speed


def onKeyPress(app, key):
    if app.gameStartScreen:
        if key == 'a':
            app.gameStartScreen = False
            app.gaming_pvai = True
        elif key == 'b':
            app.gameStartScreen = False
            app.gaming_pvp = True
    else: 
        if key == "m":
            app.music.play(loop = True)
            app.playing = True
        if app.player1.being:
            if key == 'space' and app.player1_canfire:
                app.player1.fire()
                app.player1_canfire = False
        if app.player2.being:
            if key == 'enter' and app.player2_canfire:
                app.player2.fire()
                app.player2_canfire = False


    


def main():
    runApp()
    

main()