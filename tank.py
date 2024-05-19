
from bullet import *
from elements import *
import PIL.Image
import random
import math



class tank():
    def __init__(self, topleft_x, topleft_y, speed, direction, health):
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.prev_topleft_x = topleft_x
        self.prev_topleft_y = topleft_y
        self.width = 38
        self.height = 38
        self.speed = speed
        self.canMove = True
        self.being = True
        self.direction = direction
        self.health = health
        self.attack = 1
        self.bullets = []
        self.fwdpath = dict()




    def __repr__(self):
        return (self.cx, self.cy)
    

    def fire(self):
        newBullet_x, newBullet_y = self.topleft_x, self.topleft_y
        if self.direction == 'up':
            newBullet_x += 20
            newBullet_y -= 3

        elif self.direction == 'right':
            newBullet_x += (40 + 3)
            newBullet_y += 20

        elif self.direction == 'down':
            newBullet_x += 20
            newBullet_y += (40 + 3)

        elif self.direction == 'left':
            newBullet_x -= 3
            newBullet_y += 20

        newBullet = bullet(cx = newBullet_x, cy = newBullet_y, attack = self.attack, direction = self.direction, being = True)
        self.bullets.append(newBullet)

# check if myTank collides with bricks, irons
    def isCollide(self, brickList, ironList):

        for brick in brickList:
            brickLeft = brick.topleft_x
            brickRight = brick.topleft_x + brick.width
            brickTop = brick.topleft_y
            brickBottom = brick.topleft_y + brick.height
            tankLeft = self.topleft_x
            tankRight = self.topleft_x + self.width
            tankTop = self.topleft_y
            tankBottom = self.topleft_y + self.height
            if brick.being:
                if (tankLeft < brickRight and tankRight > brickLeft and
                tankTop < brickBottom and tankBottom > brickTop):
                    self.topleft_x = self.prev_topleft_x
                    self.topleft_y = self.prev_topleft_y
                    return True # Collision detected
            
        for iron in ironList:
            ironLeft = iron.topleft_x
            ironRight = iron.topleft_x + iron.width
            ironTop = iron.topleft_y
            ironBottom = iron.topleft_y + iron.height
            tankLeft = self.topleft_x
            tankRight = self.topleft_x + self.width
            tankTop = self.topleft_y
            tankBottom = self.topleft_y + self.height
            
            if (tankLeft < ironRight and tankRight > ironLeft and
               tankTop < ironBottom and tankBottom > ironTop):
                self.topleft_x = self.prev_topleft_x
                self.topleft_y = self.prev_topleft_y
                return True # Collision detected
        return False # No collision
    



    # check the path to the target tank, return the next move direction
    def DFS_getDirection(self, target, board, row, col, brickList, ironList):
        return self.DFS_getDirection_Helper(target, board, row, col, brickList, ironList, L = [], visited = [], dfspath = {(row, col): (row, col)})
    
    def DFS_getDirection_Helper(self, target, board, row, col, brickList, ironList, L, visited, dfspath):
        startRow, startCol = int(self.topleft_y/20), int(self.topleft_x/20)
        targetRow, targetCol = int(target.topleft_y/20), int(target.topleft_x/20)
        # print(targetRow, targetCol) # correct

        rows, cols = len(board), len(board[0]) 
        # print(f'rows: {rows}, cols:{cols}') # correct

        row_minimum = getCrossLine_row_min(targetRow, targetCol, board, row_min = targetRow) 
        row_maximum = getCrossLine_row_max(targetRow, targetCol, board, row_max = targetRow)
        col_minimum = getCrossLine_col_min(targetRow, targetCol, board, col_min = targetCol) 
        col_maximum = getCrossLine_col_max(targetRow, targetCol, board, col_max = targetCol)
        # print(row_minimum, row_maximum, col_minimum, col_maximum) # correct

        # check if ai tank's topleft falls in the cross lines
        #print(f'inty_row, intx_col: {int(self.topleft_y/20)}, {int(self.topleft_x/20)}')
        #print(f'row, col: {row}, {col}')
        # check on the two cross lines
        if ((col==targetCol and 
            row_minimum <= row <= row_maximum) or
            (row==targetRow and
            col_minimum <= col <= col_maximum)):
           print('reached!!!')
           #print(f'dfspath: {dfspath}')
           fwdpath = getpath(startRow, startCol, row, col, dfspath)
           #print(f'path: {fwdpath}')
           if len(L) == 0: 
               return (0,0), fwdpath
           print(f'lastcheckfor L and path: {L, fwdpath}')
           return L[0], fwdpath
        
        else:
            # i = random.randint(0,3)
            # L = getSearchOrder2(startRow, startCol, targetRow, targetCol, i)
            # checkOrder = getSearchOrder(startRow, startCol, targetRow, targetCol)
            
            checkOrder = [(1,0), (0, 1),(0, -1), (-1, 0)] # down  right left up 
            #random.shuffle(checkOrder)
            for drow, dcol in checkOrder: # down right left up
                # if (row, col) == (37, 28):
                #     drow, dcol = -1, 0
                newRow, newCol = row + drow, col + dcol
                # print(f'newRow, newCol: {newRow}, {newCol}')
                if (0 <= newRow < rows-1 and 
                    0 <= newCol < cols-1 and 
                    board[newRow][newCol] == 0 and 
                    board[newRow+1][newCol] == 0 and
                    board[newRow][newCol+1] == 0 and
                    board[newRow+1][newCol+1] == 0 and
                    (newRow != 38 or newCol != 28) and
                    (newRow, newCol) not in visited):
                    visited.append((newRow, newCol))
                    dfspath[(newRow, newCol)] = (row, col)
                    L.append((drow, dcol))
                    #（not self.isCollide(brickList, ironList)):
                    #self.topleft_x += dcol * 20
                    #self.topleft_y += drow * 20
                    # print(f'direction: {L}')
                    solution = self.DFS_getDirection_Helper(target, board, newRow, newCol, brickList, ironList, L, visited, dfspath)
                    if solution != None:
                        #print(f'solution: {solution}')
                        return solution
                    L.pop()
            return None


def getCrossLine_row_min(targetRow, targetCol, board, row_min):
    #print(f'row_min: {row_min}')
    if board[row_min][targetCol] != 0 or row_min == 0:
        return row_min
    else:
        if board[row_min][targetCol] == 0:
            row_min -= 1
            return getCrossLine_row_min(targetRow, targetCol, board, row_min)
        
def getCrossLine_row_max(targetRow, targetCol, board, row_max):
    #print(f'row_max:{row_max}')
    if board[row_max][targetCol] != 0 or row_max == 38:
        return row_max
    else:
        if board[row_max][targetCol] == 0:
            row_max += 1
            return getCrossLine_row_max(targetRow, targetCol, board, row_max)

def getCrossLine_col_min(targetRow, targetCol, board, col_min):
    #print(f'col_min:{col_min}')
    if board[targetRow][col_min] != 0 or col_min == 0:
        return col_min
    else:
        if board[targetRow][col_min] == 0:
            col_min -= 1
            return getCrossLine_col_min(targetRow, targetCol, board, col_min)
        
def getCrossLine_col_max(targetRow, targetCol, board, col_max):
    #print(f'col_max:{col_max}')
    if board[targetRow][col_max] != 0 or col_max == 28:
        return col_max
    else:
        if board[targetRow][col_max] == 0:
            col_max += 1
            return getCrossLine_col_max(targetRow, targetCol, board, col_max)


def getpath(startRow, startCol, target_incross_row, target_incross_col, dfspath):
    fwdpath = dict()
    target_incross_cell = (target_incross_row, target_incross_col)
    start_cell = (startRow, startCol)
    #print(f'finalcell: {target_incross_row}, {target_incross_col}')
    #print(f'startcell: {startRow}, {startCol}')

    while start_cell != target_incross_cell:
        #print(f'dfspath: {dfspath}')
        fwdpath[dfspath[target_incross_cell]] = target_incross_cell
        #print(f'check: {target_incross_cell}, {dfspath[target_incross_cell]}')

        target_incross_cell = dfspath[target_incross_cell]

        #print(f'currfwdpath: {fwdpath}')
        #print(f'targertcell: {target_incross_cell}')
        #print(f'startcell: {start_cell}')
        #print(start_cell != target_incross_cell)
    #print('return fwdpath!!!')
    return fwdpath

# check comparative location of target from the ai tank
def getSearchOrder(startRow, startCol, targetRow, targetCol):
    if targetRow - startRow >= 0 and targetCol - startCol >= 0: # target is on the lower right side of ai tank
        if abs(targetRow - startRow) >= abs(targetCol - startCol): # right less
            return [(0, 1), (1, 0), (0, -1), (0, 1)] # search order: right down left up: (0, 1), (1, 0). (0, -1), (0, 1)
        else:
            return [(1, 0), (0, 1), (0, -1), (0, 1)]
    elif targetRow - startRow <= 0 and targetCol - startCol >= 0: # upper right
        if abs(targetRow - startRow) >= abs(targetCol - startCol): # right less
            return [(0, 1), (-1, 0), (0, -1), (1, 0)] # search order: right up left down: (0, 1), (-1, 0), (0, -1), (1, 0)
        else:
            return [(-1, 0), (0, 1), (0, -1), (1, 0)] 
    elif targetRow - startRow >= 0 and targetCol - startCol <= 0: # lower left
        if abs(targetRow - startRow) >= abs(targetCol - startCol): # left less
            return [(0, -1), (1, 0), (0, 1), (-1, 0)]  # left down right up
        else:
            return [(1, 0), (0, -1), (0, 1), (-1, 0)] 
    elif targetRow - startRow <= 0 and targetCol - startCol <= 0:
        if abs(targetRow - startRow) >= abs(targetCol - startCol): # left less
            return [(0, -1), (-1, 0), (0, 1), (1, 0)]  # left up right down
        else:
            return [(-1, 0), (0, -1), (0, 1), (1, 0)] 

# def getSearchOrder2(startRow, startCol, targetRow, targetCol, i):
#     if i == 0:
#         return[ (0, 1), (1, 0), (0, -1), (0, 1)]
#     elif i == 1:
#         pass

