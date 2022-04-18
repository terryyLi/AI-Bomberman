import random

class Bomb(object):
    def __init__(self, bomb_x, bomb_y, bomb_status, fire_status, bomb_imageUrl, fire_imageUrl, fireWall):
        self.x = bomb_x
        self.y = bomb_y
        self.status = bomb_status
        self.fire_status = fire_status
        self.imageUrl = bomb_imageUrl
        self.fire_imageUrl = fire_imageUrl
        self.time = 0
        self.fire_time = 0
        self.fireWall = fireWall

    def destroyMap(self, app, bombDistance):
        currentRow, currentCol = app.grid.boundToCell(self.x, self.y)
        # right
        for i in range(1, bombDistance + 1):
            if ((currentRow, currentCol + i - 1), (currentRow, currentCol + i)) in app.mazeWall:
                app.mazeWall.remove(((currentRow, currentCol + i - 1), (currentRow, currentCol + i)))
                self.createTools(currentRow, currentCol + i, app.maze)
                break
            if ((currentRow, currentCol + i), (currentRow, currentCol + i - 1)) in app.mazeWall:
                app.mazeWall.remove(((currentRow, currentCol + i), (currentRow, currentCol + i - 1)))
                self.createTools(currentRow, currentCol + i, app.maze)
                break
        # left
        for i in range(1, bombDistance + 1):
            if ((currentRow, currentCol - i + 1), (currentRow, currentCol - i)) in app.mazeWall:
                app.mazeWall.remove(((currentRow, currentCol - i + 1), (currentRow, currentCol - i)))
                self.createTools(currentRow, currentCol - i, app.maze)
                break
            if ((currentRow, currentCol - i), (currentRow, currentCol - i + 1)) in app.mazeWall:
                app.mazeWall.remove(((currentRow, currentCol - i), (currentRow, currentCol - i + 1)))
                self.createTools(currentRow, currentCol - i, app.maze)
                break

        # down
        for i in range(1, bombDistance + 1):
            if ((currentRow + i - 1, currentCol), (currentRow + i, currentCol)) in app.mazeWall:
                app.mazeWall.remove(((currentRow + i - 1, currentCol), (currentRow + i, currentCol)))
                self.createTools(currentRow + i, currentCol, app.maze)
                break
            if ((currentRow + i, currentCol), (currentRow + i - 1, currentCol)) in app.mazeWall:
                app.mazeWall.remove(((currentRow + i, currentCol), (currentRow + i - 1, currentCol)))
                self.createTools(currentRow + i, currentCol, app.maze)
                break

        # up
        for i in range(1, bombDistance + 1):
            if ((currentRow - i + 1, currentCol), (currentRow - i, currentCol)) in app.mazeWall:
                app.mazeWall.remove(((currentRow - i + 1, currentCol), (currentRow - i, currentCol)))
                self.createTools(currentRow - i, currentCol, app.maze)
                break
            if ((currentRow - i, currentCol), (currentRow - i + 1, currentCol)) in app.mazeWall:
                app.mazeWall.remove(((currentRow - i, currentCol), (currentRow - i + 1, currentCol)))
                self.createTools(currentRow - i, currentCol, app.maze)
                break
        
    def createTools(self, row, col, maze):
        if random.randint(1, 5) % 3 == 0:
            index = random.randint(0, len(maze.toolList) - 1)
            if maze.toolsBoard[row][col] == 0:
                 maze.toolsBoard[row][col] = maze.toolList[index]
    
    def getLegalFireList(self, app, bombDistance):
        row, col = app.grid.boundToCell(self.x, self.y)
        legalFireList = [[row, col]]
        # right
        for i in range(1, bombDistance + 1):
            if self.isLegalFire(app.grid, self.x + i * app.grid.gridWidth, self.y,
                                    self.x + (i - 1) * app.grid.gridWidth, self.y):
                legalFireList.append([row, col + i])
            else:
                break
            
        # left
        for i in range(1, bombDistance + 1):
            if self.isLegalFire(app.grid, self.x - i * app.grid.gridWidth, self.y,
                                    self.x - (i - 1) * app.grid.gridWidth, self.y):
                legalFireList.append([row, col - i])
            else:
                break
            
        # down
        for i in range(1, bombDistance + 1):
            if self.isLegalFire(app.grid, self.x, self.y + i * app.grid.gridHeight,
                                    self.x, self.y + (i - 1) * app.grid.gridHeight):
                legalFireList.append([row + i, col])
            else:
                break
        
            
        # up
        for i in range(1, bombDistance + 1):
            if self.isLegalFire(app.grid, self.x, self.y - i * app.grid.gridHeight,
                                    self.x, self.y  - (i - 1) * app.grid.gridHeight):
                legalFireList.append([row - i, col])
            else:
                break
        
        return legalFireList

    def isLegalFire(self, grid, x, y, x1, y1):
        # get the row and col of fire
        row, col = grid.boundToCell(x, y)
        # get the row and col of the bomb
        rowb, colb = grid.boundToCell(x1, y1)
        if ((row, col), (rowb, colb)) in self.fireWall:
            return False
        elif ((rowb, colb), (row, col)) in self.fireWall:
            return False
        elif (not row in range(grid.rows)
            or not col in range (grid.cols)):
            return False
        else:
            return True

    # remove fire walls in the list
    def removeWall(self, app):
        grid = app.grid
        row, col = grid.boundToCell(self.x, self.y)
        # right
        if ((row, col), (row + 1, col)) in self.fireWall:
            self.fireWall.remove(((row, col), (row + 1, col)))
        if ((row, col), (row - 1, col)) in self.fireWall:
            self.fireWall.remove(((row, col), (row - 1, col)))
        if ((row + 1, col), (row, col)) in self.fireWall:
            self.fireWall.remove(((row + 1, col), (row, col)))
        if ((row - 1, col), (row, col)) in self.fireWall:
            self.fireWall.remove(((row - 1, col), (row, col)))
        if ((row, col), (row, col + 1)) in self.fireWall:
            self.fireWall.remove(((row, col), (row, col + 1)))
        if ((row, col), (row, col - 1)) in self.fireWall:
            self.fireWall.remove(((row, col), (row, col - 1)))
        if ((row, col + 1), (row, col)) in self.fireWall:
            self.fireWall.remove(((row, col + 1), (row, col)))
        if ((row, col - 1), (row, col)) in self.fireWall:
            self.fireWall.remove(((row, col - 1), (row, col)))

        
