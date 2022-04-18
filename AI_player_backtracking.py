from player import *
import random

class AI_player_backtracking(Player):
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

    def takeStep(self, app):
        possibleMove = []
        for each in [( + app.grid.gridWidth, 0), ( - app.grid.gridWidth, 0), (0, + app.grid.gridHeight), (0, - app.grid.gridHeight)]:
            if (self.isLegalMove(app, self.x + each[0], self.y + each[1])
                and ((self.x + each[0], self.y + each[1]) != (app.player1.x, app.player1.y))):
                possibleMove.append(each)
        if possibleMove != []:
            index = random.randint(0, len(possibleMove) - 1)
            return [possibleMove[index][0], possibleMove[index][1]]
        return [0, 0]



