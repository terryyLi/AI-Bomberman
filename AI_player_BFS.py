from player import *
import random

class AI_player_BFS(Player):
    def __init__(self, player_x, player_y, imageUrl_down, imageUrl_up, imageUrl_right, imageUrl_left):
        super().__init__(player_x, player_y, imageUrl_down, imageUrl_up, imageUrl_right, imageUrl_left)
        self.bombList = []
        self.hp = 100
        self.speed = 1
        self.bombDistance = 1
        self.bombLimit = 1
        self.time = 0
        self.avoidTime = 0
        self.isAttack = True

# BFS algorithm
    def findPath(self, app):
        # map each cell to its neighbour
        # e.g. {(1,1):{(1,2),(1,0)}}
        pathMap = {}
        for row in range(app.grid.rows):
            for col in range(app.grid.cols):
                x1, y1, x2, y2 = app.grid.getCellBound(row, col)
                x, y = (x1 + x2) / 2, (y1 + y2) / 2
                pathMap[(row, col)] = set()
                for each in [[x + app.grid.gridWidth, y], [x - app.grid.gridWidth, y], [x, y + app.grid.gridHeight], [x, y - app.grid.gridHeight]]:
                    if self.isLegalMove_path(app, x, y, each[0], each[1]):
                        pathMap[(row, col)].add((app.grid.boundToCell(each[0], each[1])))

        # map each cell to its previous visited cell
        pathTable = {}
        for row in range(app.grid.rows):
            for col in range(app.grid.cols):
                pathTable[(row, col)] = None

        # BFS algorithm
        start = (app.grid.boundToCell(self.x, self.y))
        final = (app.grid.boundToCell(app.player1.x, app.player1.y))
        testList = [start]
        while not final in pathMap[testList[0]]:
            test = testList.pop(0)
            extendList = []
            # add its neighbours to the end of the queue
            for each in pathMap[test]:
                if not each in testList:
                    extendList.append(each)
                if pathTable[each] == None:
                    pathTable[each] = test
            testList.extend(extendList)
        path = [testList[0] ,final]
        trace = testList[0]
        while path[0] != start:     
            path.insert(0, pathTable[trace])
            trace = pathTable[trace]
        answer = []
        for each in path[1:-1]:
            x1, y1, x2, y2 = app.grid.getCellBound(each[0], each[1])
            answer.append(((x1 + x2) / 2, (y1 + y2) / 2))
        return answer