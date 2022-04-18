from grid import *
from maze import *
import copy

class Player(object):
    def __init__(self, player_x, player_y, imageUrl_down, imageUrl_up, imageUrl_right, imageUrl_left):
        self.x = player_x
        self.y = player_y
        self.imageUrl_down = imageUrl_down
        self.imageUrl_up = imageUrl_up
        self.imageUrl_right = imageUrl_right
        self.imageUrl_left = imageUrl_left
        self.bombList = []
        self.hp = 2
        self.speed = 1
        self.bombDistance = 1
        self.bombLimit = 1
    
    def takeStep(self, app):
        possibleMove = []
        for each in [( + app.grid.gridWidth, 0), ( - app.grid.gridWidth, 0), (0, + app.grid.gridHeight), (0, - app.grid.gridHeight)]:
            if ((self.isLegalMove(app, self.x + each[0], self.y + each[1]))
                and ((self.x + each[0], self.y + each[1]) != (app.player1.x, app.player1.y))):
                possibleMove.append(each)
        
        if possibleMove != []:
            index = random.randint(0, len(possibleMove) - 1)
            return [possibleMove[index][0], possibleMove[index][1]]
        return [0, 0]

    def getTool(self, app):
        row, col = app.grid.boundToCell(self.x, self.y)
        if app.maze.toolsBoard[row][col] == 'health':
            self.hp += 1
            app.maze.toolsBoard[row][col] = 0
        elif app.maze.toolsBoard[row][col] == 'shoe':
            if self.speed <= 3 :
                self.speed += 1
            app.maze.toolsBoard[row][col] = 0
        elif app.maze.toolsBoard[row][col] == 'potion':
            if self.bombDistance <= 5:
                self.bombDistance += 1
            app.maze.toolsBoard[row][col] = 0
        elif app.maze.toolsBoard[row][col] == 'bomb':
            if self.bombLimit <= 5:
                self.bombLimit += 1
            app.maze.toolsBoard[row][col] = 0

    def isLegalMove(self, app, x, y):
        # get the row and col of the player
        row, col = app.grid.boundToCell(x, y)
        # check if it's out of boundary
        if ((row < 0 or row >= app.grid.rows)
            or (col < 0 or col >= app.grid.cols)):
            return False
        # check if it's a wall
        elif not self.isCrossWall(app, x, y):
            return False
        elif app.maze.bombBoard[row][col] == 1:
            return False
        else:
            return True

    def isCrossWall(self, app, x, y):
        cell_start, cell_arrive = app.grid.boundToCell(self.x, self.y), app.grid.boundToCell(x, y)
        if ((cell_start), (cell_arrive)) in app.mazeWall or ((cell_arrive), (cell_start))in app.mazeWall:
            return False
        else:
            return True
            
    def isInFire(self, app, legalFireList):
        dangerZone = legalFireList
        # position of player
        selfRow, selfCol = app.grid.boundToCell(self.x, self.y)
        selfPosition = [selfRow, selfCol]
        if selfPosition in dangerZone:
            return True
        return False

    def isLegalMove_path(self, app, x, y, x1, y1):
        # get the row and col of the player
        row, col = app.grid.boundToCell(x1, y1)
        cell_start, cell_arrive = app.grid.boundToCell(x, y), app.grid.boundToCell(x1, y1)
        # check if it's out of boundary
        if ((row < 0 or row >= app.grid.rows)
            or (col < 0 or col >= app.grid.cols)):
            return False
        # check if it's a wall
        elif ((cell_start), (cell_arrive)) in app.mazeWall or ((cell_arrive), (cell_start))in app.mazeWall:
            return False
        else:
            return True

# backtracking algorithm
    def findPath(self, app):
        result = self.findPathHelper(app, [app.AI_player.x, app.AI_player.y], [app.player1.x, app.player1.y], 
                                        [[app.AI_player.x, app.AI_player.y]])
        if result != None:
            return result[1:-1]
        else:
            return None

    def findPathHelper(self, app, start, final, path):
        if start == final:
            return path
        else:
            bestResult = [[0] for i in range(500)]
            x, y = start[0], start[1]
            # make a move
            nextMoves = [[x + app.grid.gridWidth, y], [x - app.grid.gridWidth, y], [x, y + app.grid.gridHeight], [x, y - app.grid.gridHeight]]
            for cell in nextMoves:
                # check if its legal
                x1, y1 = cell[0], cell[1]
                if self.isLegalMove_path(app, x, y, x1, y1) and (not cell in path):
                    currentResult = copy.deepcopy(self.findPathHelper(app, cell, final, path + [cell]))
                    if currentResult != None:
                        if len(currentResult) < len(bestResult):
                            bestResult = currentResult
                if cell == [x, y - app.grid.gridHeight] and (bestResult != [[0] for i in range(500)]):
                    return bestResult
            return None



        
