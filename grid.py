class AppGrid(object):
    def __init__(self, rows, cols, margin, height, width):
        self.rows = rows
        self.cols = cols
        self.margin = margin
        self.gridHeight = (height - 2 * margin) / rows
        self.gridWidth = (width - 2 * margin - 180) / cols

    def getCellBound(self, row, col):
        x1, y1 = self.margin + col * self.gridWidth, self.margin + row * self.gridHeight
        x2, y2 = self.margin + (col + 1) * self.gridWidth, self.margin + (row + 1) * self.gridHeight
        return x1, y1, x2, y2

    def boundToCell(self, x, y):
        return int((y - self.margin) // self.gridHeight), int((x - self.margin) // self.gridWidth)

    # get the position of a wall
    def getWall(self, wall):
        cell1 = wall[0]
        cell2 = wall[1]
        cell1_x1, cell1_y1, cell1_x2, cell1_y2 = self.getCellBound(cell1[0], cell1[1])
        if cell1[0] == cell2[0]:
            return cell1_x2, cell1_y1, cell1_x2, cell1_y2
        else:
            return cell1_x1, cell1_y2, cell1_x2, cell1_y2




    