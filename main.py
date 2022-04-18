from cmu_112_graphics import *
from maze import *
from bomb import *
from player import *
from grid import *
from AI_player_backtracking import *
import copy
import pygame
from sound import*
from AI_player_BFS import*

# author: Terry
# andrewID: jielinl
# pictures are from https://github.com/lr555/SuperBomb
# music are from https://www.aigei.com/music/game/cartoon_33-come_to_tafang_every/

# model
def appStarted(app):
    # splashScreenMode
    app.mode = 'splashScreenMode'
    app.image_splashScreen = app.loadImage('resources/login.png')
    app.image_help = app.loadImage('resources/help.png')

    # gameMode
    app.grid = AppGrid(11, 19, 25, 600, 1180)
    app.player1 = Player(app.grid.margin + 3 * app.grid.gridWidth / 2, app.grid.margin + 3 * app.grid.gridHeight / 2, 
    'resources/player1_down.png', 'resources/player1_up.png', 'resources/player1_right.png', 'resources/player1_left.png')
    app.player2 = Player(app.width - 180 - app.grid.margin - 3 * app.grid.gridWidth / 2, app.height - app.grid.margin - 3 * app.grid.gridHeight / 2, 
    'resources/player2_down.png', 'resources/player2_up.png', 'resources/player2_right.png', 'resources/player2_left.png')
    app.AI_player = AI_player_BFS(app.width - 180 - app.grid.margin - 3 * app.grid.gridWidth / 2, app.height - app.grid.margin - 3 * app.grid.gridHeight / 2, 
    'resources/player2_down.png', 'resources/player2_up.png', 'resources/player2_right.png', 'resources/player2_left.png')
    app.maze = Maze(app.grid.cols, app.grid.rows)
    app.mazeWall = app.maze.mazeCreate()

    app.AI_path_draw = app.AI_player.findPath(app)
    app.AI_player_path = app.AI_path_draw
    app.image_AI_player = app.loadImage(app.AI_player.imageUrl_down)
 
    app.image_background = app.loadImage('resources/background.png')
    app.image_bomb = app.loadImage('resources/bomb.png')
    app.image_fire = app.loadImage('resources/fire.png')
    app.image_player1 = app.loadImage(app.player1.imageUrl_down)
    app.image_player2 = app.loadImage(app.player2.imageUrl_down)
    app.image_state = app.loadImage('resources/state.png')
    app.image_tool_shoe = app.loadImage('resources/tool_shoe.png')
    app.image_tool_health = app.loadImage('resources/tool_health.png')
    app.image_tool_potion = app.loadImage('resources/tool_potion.png')
    app.image_tool_bomb = app.loadImage('resources/tool_bomb.png')

    app.image_youlose = app.loadImage('resources/youlose.png')
    app.image_youwin = app.loadImage('resources/youwin.png')
    app.image_player1win = app.loadImage('resources/player1win.png')
    app.image_player2win = app.loadImage('resources/player2win.png')
    app.image_pause = app.loadImage('resources/pause.png')
    

    app.timerDelay = 100
    app.isGameOver = False
    app.isPaused = False
    app.isAIMode = False
    app.player = [app.player1, app.player2]
    
    # music
    pygame.mixer.init()
    app.gameSound = Sound('resources/game.mp3')
    app.gameSound.start()
    

    
# controller
def gameMode_keyPressed(app, event):
    if event.key == '0':
        appStarted(app)
        app.mode = 'gameMode'
        app.isAIMode = True
        app.player = [app.player1, app.AI_player]
    elif event.key == '9':
        appStarted(app)
        app.mode = 'gameMode'
        app.isAIMode = False
    elif event.key == 'r' and app.isGameOver:
        appStarted(app)
    elif event.key == 'p':
        app.isPaused = not app.isPaused
        if app.gameSound.isPlaying():
            app.gameSound.pause()
        else:
            app.gameSound.unpause()
    elif app.isGameOver or app.isPaused: return
    else:
        # player 1
        if event.key == 'f':
            fireWall = copy.deepcopy(app.mazeWall)
            bomb = Bomb(app.player1.x, app.player1.y, True, False, 'resources/bomb.png', 'resources/fire.png', fireWall)
            if len(app.player1.bombList) < app.player1.bombLimit:
                app.player1.bombList.append(bomb)
                row, col = app.grid.boundToCell(bomb.x, bomb.y)
                app.maze.bombBoard[row][col] = 1
        elif event.key == 'd':
            app.image_player1 = app.loadImage(app.player1.imageUrl_right)
            if app.player1.isLegalMove(app, app.player1.x + app.grid.gridWidth, app.player1.y):
                app.player1.x += app.grid.gridWidth
                app.player1.getTool(app)
                if app.isAIMode:
                    app.AI_path_draw = app.AI_player.findPath(app)
                    app.AI_player_path = app.AI_path_draw
        elif event.key == 'a':
            app.image_player1 = app.loadImage(app.player1.imageUrl_left)
            if app.player1.isLegalMove(app, app.player1.x - app.grid.gridWidth, app.player1.y):
                app.player1.x -= app.grid.gridWidth
                app.player1.getTool(app)
                if app.isAIMode:
                    app.AI_path_draw = app.AI_player.findPath(app)
                    app.AI_player_path = app.AI_path_draw
        elif event.key == 'w':
            app.image_player1 = app.loadImage(app.player1.imageUrl_up)
            if app.player1.isLegalMove(app, app.player1.x, app.player1.y - app.grid.gridHeight):
                app.player1.y -= app.grid.gridHeight
                app.player1.getTool(app)
                if app.isAIMode:
                    app.AI_path_draw = app.AI_player.findPath(app)
                    app.AI_player_path = app.AI_path_draw
        elif event.key == 's':
            app.image_player1 = app.loadImage(app.player1.imageUrl_down)
            if app.player1.isLegalMove(app, app.player1.x, app.player1.y + app.grid.gridHeight):
                app.player1.y += app.grid.gridHeight
                app.player1.getTool(app)
                if app.isAIMode:
                    app.AI_path_draw = app.AI_player.findPath(app)
                    app.AI_player_path = app.AI_path_draw
        # player 2
        else:
            if not app.isAIMode:
                if event.key == 'Space':
                    fireWall = copy.deepcopy(app.mazeWall)
                    bomb = Bomb(app.player2.x, app.player2.y, True, False, 'resources/bomb.png', 'resources/fire.png', fireWall)
                    if len(app.player2.bombList) < app.player2.bombLimit:
                        app.player2.bombList.append(bomb)
                        row, col = app.grid.boundToCell(bomb.x, bomb.y)
                        app.maze.bombBoard[row][col] = 1
                elif event.key == 'Right':
                    app.image_player2 = app.loadImage(app.player2.imageUrl_right)
                    if app.player2.isLegalMove(app, app.player2.x + app.grid.gridWidth, app.player2.y):
                        app.player2.x += app.grid.gridWidth
                        app.player2.getTool(app)
                        
                elif event.key == 'Left':
                    app.image_player2 = app.loadImage(app.player2.imageUrl_left)
                    if app.player2.isLegalMove(app, app.player2.x - app.grid.gridWidth, app.player2.y):
                        app.player2.x -= app.grid.gridWidth
                        app.player2.getTool(app)
                        
                elif event.key == 'Up':
                    app.image_player2 = app.loadImage(app.player2.imageUrl_up)
                    if app.player2.isLegalMove(app, app.player2.x, app.player2.y - app.grid.gridHeight):
                        app.player2.y -= app.grid.gridHeight
                        app.player2.getTool(app)
                        
                elif event.key == 'Down':
                    app.image_player2 = app.loadImage(app.player2.imageUrl_down)
                    if app.player2.isLegalMove(app, app.player2.x, app.player2.y + app.grid.gridHeight):
                        app.player2.y += app.grid.gridHeight
                        app.player2.getTool(app)

def gameMode_mousePressed(app, event):
    if app.isGameOver:
        if (((event.x >= ((app.width - 180) / 2 - 200 / 2 + 16))
            and (event.x <= ((app.width - 180) / 2 - 200 / 2 + 181)))
            and ((event.y >= (app.height / 2 - 200 / 2 + 107))
            and (event.y <= (app.height / 2 - 200 / 2 + 177)))):
            appStarted(app)
            app.gameSound = Sound('resources/win.mp3')
            app.gameSound.start(loops = 1)
    elif app.isPaused:
        if (((event.x >= ((app.width - 180) / 2 - 200 / 2 + 16))
            and (event.x <= ((app.width - 180) / 2 - 200 / 2 + 181)))
            and ((event.y >= (app.height / 2 - 200 / 2 + 107))
            and (event.y <= (app.height / 2 - 200 / 2 + 177)))):
            appStarted(app)
        elif (((event.x >= ((app.width - 180) / 2 - 200 / 2 + 16))
            and (event.x <= ((app.width - 180) / 2 - 200 / 2 + 181)))
            and ((event.y >= (app.height / 2 - 200 / 2 + 23))
            and (event.y <= (app.height / 2 - 200 / 2 + 93)))):
            app.gameSound.unpause()
            app.isPaused = not app.isPaused


def splashScreenMode_mousePressed(app, event):
    if event.x >= 153 and event.x <= 438 and event.y >= 300 and event.y <= 396:
        app.mode = 'gameMode' 
        if app.gameSound.path != 'resources/game.mp3':
            app.gameSound.path = Sound('resources/game.mp3')
            app.gameSound.start()
    elif event.x >= 153 and event.x <= 438 and event.y >= 426 and event.y <= 523:
        app.mode = 'helpMode'

def helpMode_mousePressed(app, event):
    if event.x >= 876 and event.x <= 1160 and event.y >= 483 and event.y <= 578:
        app.mode = 'splashScreenMode' 
    

def gameMode_timerFired(app):
    if app.isGameOver or app.isPaused:
        return
    # press space then draw a bomb
    for player in app.player:
        for bomb in player.bombList:
            if bomb.status:
                bomb.time += 1
                # after few seconds bomb disappear and destroy map and fire appears
                if bomb.time % 10 == 0:
                    bomb.status = not bomb.status
                    bomb.fire_status = not bomb.fire_status
                    row, col = app.grid.boundToCell(bomb.x, bomb.y)
                    app.maze.bombBoard[row][col] = 0
                    bomb.destroyMap(app, player.bombDistance)
                    if app.isAIMode:
                        app.AI_path_draw = app.AI_player.findPath(app)
                        app.AI_player_path = app.AI_path_draw
                    # if the player is in the danger zone, it hurt
                    legalFireList = bomb.getLegalFireList(app, player.bombDistance)
                    for each in app.player:
                        if each.isInFire(app, legalFireList): 
                            each.hp -= 1
                            if each.hp == 0:
                                app.isGameOver = True
                                app.gameSound.fadeout(3000)
                                return

        # after few seconds fire disappears
            elif bomb.fire_status:
                bomb.fire_time += 1
                if bomb.fire_time % 2 == 0:
                    bomb.fire_status = not bomb.fire_status
                    player.bombList.remove(bomb)
                    bomb.removeWall(app)
    # AI move
    if app.isAIMode:
        if app.AI_player.isAttack:
            app.AI_player.time += 1
            if app.AI_player.time % (4 - app.AI_player.speed) == 0:
                if app.AI_player_path:
                    path = app.AI_player_path.pop(0)
                    # AI face
                    dx, dy = path[0] - app.AI_player.x, path[1] - app.AI_player.y
                    if (dx, dy) == (+ app.grid.gridWidth, 0):
                        app.image_AI_player = app.loadImage(app.AI_player.imageUrl_right)
                    elif (dx, dy) == (- app.grid.gridWidth, 0):
                        app.image_AI_player = app.loadImage(app.AI_player.imageUrl_left)
                    elif (dx, dy) == (0, + app.grid.gridHeight):
                        app.image_AI_player = app.loadImage(app.AI_player.imageUrl_down)
                    elif (dx, dy) == (0, - app.grid.gridHeight):
                        app.image_AI_player = app.loadImage(app.AI_player.imageUrl_up)
                    app.AI_player.x, app.AI_player.y = app.AI_player.x + dx, app.AI_player.y + dy
                    app.AI_player.getTool(app)
                else:
                    fireWall = copy.deepcopy(app.mazeWall)
                    bomb = Bomb(app.AI_player.x, app.AI_player.y, True, False, 'resources/bomb.png', 'resources/fire.png', fireWall)
                    if len(app.AI_player.bombList) < app.AI_player.bombLimit:
                        app.AI_player.bombList.append(bomb)
                        row, col = app.grid.boundToCell(bomb.x, bomb.y)
                        app.maze.bombBoard[row][col] = 1
                        app.AI_player.isAttack = False
        else:
            app.AI_player.time += 1
            if app.AI_player.time % 3 == 0:
                direc = app.AI_player.takeStep(app)
                dx, dy = direc[0], direc[1]
                app.AI_player.x, app.AI_player.y = app.AI_player.x + dx, app.AI_player.y + dy
                app.AI_path_draw = app.AI_player.findPath(app)
                app.AI_player_path = app.AI_path_draw
            app.AI_player.avoidTime += 1
            if app.AI_player.avoidTime % 10 == 0:
                app.AI_player.isAttack = True
         
# view

def draw_maze(app, canvas):
    canvas.create_image((app.width-180)/2, app.height/2, image=ImageTk.PhotoImage(app.image_background))
    # draw the maze
    for wall in app.mazeWall:
        x1, y1, x2, y2 = app.grid.getWall(wall)
        canvas.create_line(x1, y1, x2, y2, fill = 'black', width = 4)
    # draw the boundary
    canvas.create_line(app.grid.margin, app.grid.margin, app.width - 180 - app.grid.margin, app.grid.margin, fill = 'black', width = 4)
    canvas.create_line(app.grid.margin, app.grid.margin, app.grid.margin, app.height - app.grid.margin, fill = 'black', width = 4)
    canvas.create_line(app.grid.margin, app.height - app.grid.margin, 
        app.width - 180 - app.grid.margin, app.height - app.grid.margin, fill = 'black', width = 4)
    canvas.create_line(app.width - 180 - app.grid.margin, app.grid.margin
        , app.width - 180 - app.grid.margin, app.height - app.grid.margin, fill = 'black', width = 4)
    

    # for row in range(app.grid.rows):
    #     for col in range(app.grid.cols):
    #         x1, y1, x2, y2 = app.grid.getCellBound(row, col)
    #         if (app.mazeWall[row][col] == 'w'):
    #             canvas.create_image((x1 + x2) / 2, (y1 + y2)/2 - 7.5, image=ImageTk.PhotoImage(app.image_brick))
                #canvas.create_rectangle(x1, y1, x2, y2, fill = 'yellow', outline = 'yellow')
            #canvas.create_rectangle(x1, y1, x2, y2)

def draw_fire(app, canvas):
    for player in app.player:
        for bomb in player.bombList:
            if bomb.fire_status:
                legalFireList = bomb.getLegalFireList(app, player.bombDistance)
                for fire in legalFireList:
                    x1, y1, x2, y2 = app.grid.getCellBound(fire[0], fire[1])
                    canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=ImageTk.PhotoImage(app.image_fire))                

def draw_player1(app, canvas, x, y):
    #sprite = app.player_sprites[app.player_spriteCounter]
    canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image_player1))

def draw_player2(app, canvas, x, y):
    canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image_player2))

def draw_AI_player(app, canvas, x, y):
    canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image_AI_player))

def draw_bomb(app, canvas):
    for player in app.player:
        for bomb in player.bombList:
            if bomb.status:
                canvas.create_image(bomb.x, bomb.y, image=ImageTk.PhotoImage(app.image_bomb))

def draw_path(app, canvas):
    if app.AI_path_draw != None:
        for each in app.AI_path_draw:
            row, col = app.grid.boundToCell(each[0], each[1])
            x1, y1, x2, y2 = app.grid.getCellBound(row, col)
            canvas.create_oval(x1 + 3 * app.grid.gridWidth / 7, y1 + 3 * app.grid.gridHeight / 7,
                x2 - 3 * app.grid.gridWidth / 7, y2 - 3 * app.grid.gridHeight / 7, fill = 'red')

def draw_state(app, canvas):
    canvas.create_image(app.width - 180 / 2, app.height/2, image = ImageTk.PhotoImage(app.image_state))
    canvas.create_text(app.width - 35, 83, text = app.player1.hp)
    canvas.create_text(app.width - 35, 140, text = app.player1.speed)
    canvas.create_text(app.width - 35, 197, text = app.player1.bombDistance)
    canvas.create_text(app.width - 35, 254, text = app.player1.bombLimit)
    if app.isAIMode:
        canvas.create_text(app.width - 35, 83 + 280, text = app.AI_player.hp)
        canvas.create_text(app.width - 35, 140 + 280, text = app.AI_player.speed)
        canvas.create_text(app.width - 35, 197 + 280, text = app.AI_player.bombDistance)
        canvas.create_text(app.width - 35, 254 + 280, text = app.AI_player.bombLimit)
    else:
        canvas.create_text(app.width - 35, 83 + 280, text = app.player2.hp)
        canvas.create_text(app.width - 35, 140 + 280, text = app.player2.speed)
        canvas.create_text(app.width - 35, 197 + 280, text = app.player2.bombDistance)
        canvas.create_text(app.width - 35, 254 + 280, text = app.player2.bombLimit)

def draw_tools(app, canvas):
    for row in range(len(app.maze.toolsBoard)):
        for col in range(len(app.maze.toolsBoard[0])):
            x1, y1, x2, y2 = app.grid.getCellBound(row, col)
            if app.maze.toolsBoard[row][col] == 'shoe':
                canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=ImageTk.PhotoImage(app.image_tool_shoe))
            elif app.maze.toolsBoard[row][col] == 'potion':
                canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=ImageTk.PhotoImage(app.image_tool_potion))
            elif app.maze.toolsBoard[row][col] == 'bomb':
                canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=ImageTk.PhotoImage(app.image_tool_bomb))
            elif app.maze.toolsBoard[row][col] == 'health':
                canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=ImageTk.PhotoImage(app.image_tool_health))

def gameMode_redrawAll(app, canvas):
    draw_maze(app, canvas)
    draw_bomb(app, canvas)
    draw_fire(app, canvas)
    draw_player1(app, canvas, app.player1.x, app.player1.y)
    #draw_player2(app, canvas, app.player2.x, app.player2.y)
    if app.isAIMode:
        draw_AI_player(app, canvas, app.AI_player.x, app.AI_player.y)
    else:
        draw_player2(app, canvas, app.player2.x, app.player2.y)
    #draw_path(app, canvas)
    draw_state(app, canvas)
    draw_tools(app, canvas)

    if app.isGameOver:
        if app.isAIMode:
            if app.player1.hp == 0:
                canvas.create_image((app.width - 180)/2, app.height/2, image=ImageTk.PhotoImage(app.image_youlose))
            elif app.AI_player.hp == 0:
                canvas.create_text((app.width - 180)/2, app.height/2, image=ImageTk.PhotoImage(app.image_you1win))
        else:
            if app.player1.hp == 0:
                canvas.create_image((app.width - 180)/2, app.height/2, image=ImageTk.PhotoImage(app.image_player2win))
            elif app.player2.hp == 0:
                canvas.create_image((app.width - 180)/2, app.height/2, image=ImageTk.PhotoImage(app.image_player1win))

        
    elif app.isPaused:
        canvas.create_image((app.width - 180)/2, app.height/2, image=ImageTk.PhotoImage(app.image_pause))

def splashScreenMode_redrawAll(app, canvas):
    canvas.create_image(app.width / 2, app.height / 2, image=ImageTk.PhotoImage(app.image_splashScreen))

def helpMode_redrawAll(app, canvas):
    canvas.create_image(app.width / 2, app.height / 2, image=ImageTk.PhotoImage(app.image_help))

runApp(width = 1180, height = 600)
