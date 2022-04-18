import random


class Maze(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # 'u' represents unvisited cell
        self.maze = [['u'] * width for i in range(height)]
        self.wallList = []
        self.bombBoard = [[0] * width for i in range(height)]
        self.walls = []
        self.toolsBoard = [[0] * width for i in range(height)]
        self.toolList = ['shoe', 'potion', 'bomb', 'health']


    def mazeCreate(self):
        setToCell = {}
        cellToSet = {}
        count = 1
        # map each cell to a set
        for i in range(self.height):
            for j in range(self.width):
                setToCell[count] = {(i, j)}
                count += 1
        count = 1
        for i in range(self.height):
            for j in range(self.width):
                cellToSet[(i, j)] = count
                count += 1
        # create walls by expressing row/col of its neighbor cells
        for i in range(self.height):
            for j in range(self.width - 1):
                self.wallList.append(((i,j), (i,j+1)))
        for i in range(self.height - 1):
            for j in range(self.width):
                self.wallList.append(((i,j), (i+1,j)))
        # join the cells it connects if they are not already connected by a path.
        while len(setToCell) > 1:
            # get a randomWall
            randomWall = self.wallList[random.randint(0, len(self.wallList) - 1)]
            # get the corresponding cells
            cell1, cell2 = randomWall[0], randomWall[1]
            # get the corresponding sets for these cells
            cell1_set, cell2_set = cellToSet[cell1], cellToSet[cell2]
            if cell1_set != cell2_set:
                if len(setToCell[cell1_set]) >= len(setToCell[cell2_set]):
                    # merge two sets
                    for cell in setToCell[cell2_set]:
                        setToCell[cell1_set].add(cell)
                    for cell in setToCell[cell1_set]:
                        # map these cells to the same set
                        cellToSet[cell] = cell1_set
                    del setToCell[cell2_set]
                else:
                    # merge two sets
                    for cell in setToCell[cell1_set]:
                        setToCell[cell2_set].add(cell)
                    for cell in setToCell[cell2_set]:
                        # map these cells to the same set
                        cellToSet[cell] = cell2_set
                    del setToCell[cell1_set]
                self.wallList.remove(randomWall)
        return set(self.wallList)


