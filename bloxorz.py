# x-axis is vertical, point down
# y-axis is horizontal, point right

# 0: DEAD
# 1: NORMAL
# 2: GOAL
# 3: X - ON and OFF (heavy)
# 4: O - ON and OFF (soft)
# 5: Orange tiles
# 6: O - Only ON (soft)
# 7: O - Only OFF (soft)
# 8: Teleport and Split gate
# 9: X - Only OFF (heavy)
# 10: X - Only ON (heavy)
# 11: O - ON a bridge and OFF a bridge (soft)
# 12: X - ON a bridge and OFF a bridge (heavy)

import sys
import copy
import time
import random
import numpy as np

import timeit
import os, psutil

random.seed(time.time())

def printBoard(board):
    row, col = np.shape(board)
    f.write("BOARD:\n")
    f.write('=' * col * 3 + '\n')
    for i in board:
        f.write(str(i) + '\n')
    f.write('=' * col * 3 + '\n')
    
def readBoard(file):
    with open(file) as ff:
        # Read the first line to get shape of board, initialize coordinate of block
        row, init_x, init_y = [int(x) for x in next(ff).split()]
        
        # Read the board
        board = []
        count = 0
        for line in ff:
            board.append([int(x) for x in line.split()])
            count += 1
            if count == row: 
                break
            
        # Read the items
        items = []
        for line in ff:
            items.append([int(x) for x in line.split()])
            
    return board, items, init_x, init_y

def fullBoard(board, items):
    b = copy.deepcopy(board)
    for i in items:
        x, y = i[0], i[1]
        b[i[2]][i[3]] = 1
        if i[4] != - 1:
            b[i[4]][i[5]] = 1
        if len(i) > 6:
            b[i[6]][i[7]] = 1
            if i[8] != -1:
                b[i[8]][i[9]] = 1
    return b

class Cube:
    def __init__(self, 
                 X: int, 
                 Y: int,
                 prev: 'Cube' = None,
    ):
        self.x = copy.deepcopy(X)
        self.y = copy.deepcopy(Y)
        self.prev = prev
        
    def up(self):
        return self.x - 1, self.y
    
    def down(self):
        return self.x + 1, self.y
    
    def right(self):
        return self.x, self.y + 1
    
    def left(self):
        return self.x, self.y - 1
    
    def visited(self, passed: list):
        for i in passed:
            if self.x == i.x and self.y == i.y:
                return True
        return False
    
    def Dead(self, board):
        if board[self.x][self.y] == 0:
            return True
        return False
    
    def Goal(self, board):
        if board[self.x][self.y] == 2:
            return True
        return False

class Block:
    def __init__(self, 
                 cube_1: Cube,
                 cube_2: Cube,
                 parent: 'Block' = None,
                 parent_step: str = "- START",
                 board: list = None,
                 split: bool = False,
    ):
        self.cube_1 = cube_1
        self.cube_2 = cube_2
        self.parent = parent
        self.parent_step = parent_step
        self.board = copy.deepcopy(board)
        self.split = split
        
    def isStanding(self):
        if (self.cube_1.x == self.cube_2.x and self.cube_1.y == self.cube_2.y):
            return True
        return False
    
    def up(self):
        # STANDING
        if self.isStanding():
            return Cube(self.cube_1.x - 1, self.cube_1.y), Cube(self.cube_2.x - 2, self.cube_2.y)
        # LAYING ALONG X-AXIS
        elif self.cube_1.y == self.cube_2.y:
            if self.cube_1.x < self.cube_2.x:
                return Cube(self.cube_1.x - 1, self.cube_1.y), Cube(self.cube_2.x - 2, self.cube_2.y)
            else:
                return Cube(self.cube_1.x - 2, self.cube_1.y), Cube(self.cube_2.x - 1, self.cube_2.y)
        # LAYING ALONG Y-AXIS
        return Cube(self.cube_1.x - 1, self.cube_1.y), Cube(self.cube_2.x - 1, self.cube_2.y)
    
    def down(self):
        # STANDING
        if self.isStanding():
            return Cube(self.cube_1.x + 1, self.cube_1.y), Cube(self.cube_2.x + 2, self.cube_2.y)
        # LAYING ALONG X-AXIS
        elif self.cube_1.y == self.cube_2.y:
            if self.cube_1.x > self.cube_2.x:
                return Cube(self.cube_1.x + 1, self.cube_1.y), Cube(self.cube_2.x + 2, self.cube_2.y)
            else:
                return Cube(self.cube_1.x + 2, self.cube_1.y), Cube(self.cube_2.x + 1, self.cube_2.y)
        # LAYING ALONG Y-AXIS
        return Cube(self.cube_1.x + 1, self.cube_1.y), Cube(self.cube_2.x + 1, self.cube_2.y)
            
    def right(self):
        # STANDING
        if self.isStanding():
            return Cube(self.cube_1.x, self.cube_1.y + 1), Cube(self.cube_2.x, self.cube_2.y + 2)
        # LAYING ALONG Y-AXIS
        elif self.cube_1.x == self.cube_2.x:
            if self.cube_1.y > self.cube_2.y:
                return Cube(self.cube_1.x, self.cube_1.y + 1), Cube(self.cube_2.x, self.cube_2.y + 2)
            else:
                return Cube(self.cube_1.x, self.cube_1.y + 2), Cube(self.cube_2.x, self.cube_2.y + 1)
        # LAYING ALONG X-AXIS
        return Cube(self.cube_1.x, self.cube_1.y + 1), Cube(self.cube_2.x, self.cube_2.y + 1)
    
    def left(self):
        # STANDING
        if self.isStanding():
            return Cube(self.cube_1.x, self.cube_1.y - 1), Cube(self.cube_2.x, self.cube_2.y - 2)
        # LAYING ALONG Y-AXIS
        elif self.cube_1.x == self.cube_2.x:
            if self.cube_1.y < self.cube_2.y:
                return Cube(self.cube_1.x, self.cube_1.y - 1), Cube(self.cube_2.x, self.cube_2.y - 2)
            else:
                return Cube(self.cube_1.x, self.cube_1.y - 2), Cube(self.cube_2.x, self.cube_2.y - 1)
        # LAYING ALONG X-AXIS
        return Cube(self.cube_1.x, self.cube_1.y - 1), Cube(self.cube_2.x, self.cube_2.y - 1)
    
    def cube_1_up(self):
        return Cube(self.cube_1.x - 1, self.cube_1.y), Cube(self.cube_2.x, self.cube_2.y)
    
    def cube_1_down(self):
        return Cube(self.cube_1.x + 1, self.cube_1.y), Cube(self.cube_2.x, self.cube_2.y)
    
    def cube_1_right(self):
        return Cube(self.cube_1.x, self.cube_1.y + 1), Cube(self.cube_2.x, self.cube_2.y)
    
    def cube_1_left(self):
        return Cube(self.cube_1.x, self.cube_1.y - 1), Cube(self.cube_2.x, self.cube_2.y)
    
    def cube_2_up(self):
        return Cube(self.cube_1.x, self.cube_1.y), Cube(self.cube_2.x - 1, self.cube_2.y)
    
    def cube_2_down(self):
        return Cube(self.cube_1.x, self.cube_1.y), Cube(self.cube_2.x + 1, self.cube_2.y)
    
    def cube_2_right(self):
        return Cube(self.cube_1.x, self.cube_1.y), Cube(self.cube_2.x, self.cube_2.y + 1)
    
    def cube_2_left(self):
        return Cube(self.cube_1.x, self.cube_1.y), Cube(self.cube_2.x, self.cube_2.y - 1)
    
    # BUTTON 3: X - ON and OFF (heavy)
    def button3(self, items: list):
        if self.board[self.cube_1.x][self.cube_1.y] != 3 or self.board[self.cube_2.x][self.cube_2.y] != 3:
            return
        
        for i in items:
            if i[0] == self.cube_1.x and i[1] == self.cube_1.y:
                if i[2] == -1: 
                    return # X button but no bridge is created
                if self.board[i[2]][i[3]] == 0:
                    self.board[i[2]][i[3]] = 1
                    if i[4] != -1: # Sometimes we just creat one tile
                        self.board[i[4]][i[5]] = 1
                else:
                    self.board[i[2]][i[3]] = 0
                    if i[4] != -1: # Sometimes we just erase one tile
                        self.board[i[4]][i[5]] = 0
                if len(i) > 6: # Creat 2 bridge
                    if self.board[i[6]][i[7]] == 0:
                        self.board[i[6]][i[7]] = 1
                        if i[8] != -1:
                            self.board[i[8]][i[9]] = 1
                    else:
                        self.board[i[6]][i[7]] = 0
                        if i[8] != -1: 
                            self.board[i[8]][i[9]] = 0
                if len(i) > 10:
                    if self.board[i[10]][i[11]] == 0:
                        self.board[i[10]][i[11]] = 1
                        if i[12] != -1:
                            self.board[i[12]][i[13]] = 1
                    else:
                        self.board[i[10]][i[11]] = 0
                        if i[12] != -1:
                            self.board[i[12]][i[13]] = 0
                if len(i) > 14:
                    if self.board[i[14]][i[15]] == 0:
                        self.board[i[14]][i[15]] = 1
                        if i[16] != -1:
                            self.board[i[16]][i[17]] = 1
                    else:
                        self.board[i[14]][i[15]] = 0
                        if i[16] != -1:
                            self.board[i[16]][i[17]] = 0
                return
    
    # BUTTON 4: O - ON and OFF (soft)
    def button4(self, items: list):
        if self.board[self.cube_1.x][self.cube_1.y] != 4 and self.board[self.cube_2.x][self.cube_2.y] != 4:
            return
        
        X, Y = -1, -1
        if self.board[self.cube_1.x][self.cube_1.y] == 4:
            X = self.cube_1.x
            Y = self.cube_1.y
            save = 1
        else:
            X = self.cube_2.x
            Y = self.cube_2.y
            save = 2
            
        for i in items:
            if i[0] == X and i[1] == Y:
                if i[2] == -1: 
                    return # O button but no bridge is created
                if self.board[i[2]][i[3]] == 0:
                    self.board[i[2]][i[3]] = 1
                    if i[4] != -1:
                        self.board[i[4]][i[5]] = 1
                else:
                    self.board[i[2]][i[3]] = 0
                    if i[4] != -1:
                        self.board[i[4]][i[5]] = 0
                if len(i) == 10: # Creat 2 bridge
                    if self.board[i[6]][i[7]] == 0:
                        self.board[i[6]][i[7]] = 1
                        if i[8] != -1: # Sometimes we just erase one tile
                            self.board[i[8]][i[9]] = 1
                    else:
                        self.board[i[6]][i[7]] = 0
                        if i[8] != -1: # Sometimes we just erase one tile
                            self.board[i[8]][i[9]] = 0
                break
            
        two_button = False
        duplicate = False
        
        if save == 1 and (self.board[self.cube_2.x][self.cube_2.y] == 4 or 
                          self.board[self.cube_2.x][self.cube_2.y] == 6 or 
                          self.board[self.cube_2.x][self.cube_2.y] == 7 or
                          self.board[self.cube_2.x][self.cube_2.y] == 11):
            X = self.cube_2.x
            Y = self.cube_2.y
            two_button = True
            if self.board[self.cube_2.x][self.cube_2.y] == 4:
                duplicate = True
        elif save == 2 and (self.board[self.cube_1.x][self.cube_1.y] == 4 or
                            self.board[self.cube_1.x][self.cube_1.y] == 6 or
                            self.board[self.cube_1.x][self.cube_1.y] == 7 or
                            self.board[self.cube_1.x][self.cube_1.y] == 11):
            X = self.cube_1.x
            Y = self.cube_1.y
            two_button = True
            if self.board[self.cube_1.x][self.cube_1.y] == 4:
                duplicate = True
            
        if two_button:
            if duplicate:
                for i in items:
                    if i[0] == X and i[1] == Y:
                        if i[2] == -1: 
                            return
                        self.board[i[2]][i[3]] = 0
                        if i[4] != -1:
                            self.board[i[4]][i[5]] = 0
                        if len(i) > 6:
                            self.board[i[6]][i[7]] = 0
                            if i[8] != -1:
                                self.board[i[8]][i[9]] = 0
                        if len(i) > 10:
                            self.board[i[10]][i[11]] = 0
                            if i[12] != -1:
                                self.board[i[12]][i[13]] = 0
                        if len(i) > 14:
                            self.board[i[14]][i[15]] = 0
                            if i[16] != -1:
                                self.board[i[16]][i[17]] = 0
                        return
            else:
                self.button6(items)
                self.button7(items)
                self.button11(items)
                return
            
    # BUTTON 6: O - Only ON (soft)
    def button6(self, items: list):
        if self.board[self.cube_1.x][self.cube_1.y] != 6 and self.board[self.cube_2.x][self.cube_2.y] != 6:
            return

        X, Y = -1, -1
        if self.board[self.cube_1.x][self.cube_1.y] == 6:
            X = self.cube_1.x
            Y = self.cube_1.y
            save = 1
        else:
            X = self.cube_2.x
            Y = self.cube_2.y
            save = 2
            
        for i in items:
            if i[2] == -1: 
                return
            if i[0] == X and i[1] == Y:
                self.board[i[2]][i[3]] = 1
                if i[4] != -1:
                    self.board[i[4]][i[5]] = 1
                if len(i) == 10: # Creat 2 bridge
                    self.board[i[6]][i[7]] = 1
                    if i[8] != -1: # Sometimes we just erase one tile
                        self.board[i[8]][i[9]] = 1
                break
            
        two_button = False
        duplicate = False
        
        if save == 1 and (self.board[self.cube_2.x][self.cube_2.y] == 4 or 
                          self.board[self.cube_2.x][self.cube_2.y] == 6 or 
                          self.board[self.cube_2.x][self.cube_2.y] == 7 or
                          self.board[self.cube_2.x][self.cube_2.y] == 11):
            X = self.cube_2.x
            Y = self.cube_2.y
            two_button = True
            if self.board[self.cube_2.x][self.cube_2.y] == 6:
                duplicate = True
        elif save == 2 and (self.board[self.cube_1.x][self.cube_1.y] == 4 or
                            self.board[self.cube_1.x][self.cube_1.y] == 6 or
                            self.board[self.cube_1.x][self.cube_1.y] == 7 or
                            self.board[self.cube_1.x][self.cube_1.y] == 11):
            X = self.cube_1.x
            Y = self.cube_1.y
            two_button = True
            if self.board[self.cube_1.x][self.cube_1.y] == 6:
                duplicate = True
            
        if two_button:
            if duplicate:
                for i in items:
                    if i[0] == X and i[1] == Y:
                        if i[2] == -1: 
                            return
                        self.board[i[2]][i[3]] = 0
                        if i[4] != -1:
                            self.board[i[4]][i[5]] = 0
                        if len(i) > 6:
                            self.board[i[6]][i[7]] = 0
                            if i[8] != -1:
                                self.board[i[8]][i[9]] = 0
                        if len(i) > 10:
                            self.board[i[10]][i[11]] = 0
                            if i[12] != -1:
                                self.board[i[12]][i[13]] = 0
                        if len(i) > 14:
                            self.board[i[14]][i[15]] = 0
                            if i[16] != -1:
                                self.board[i[16]][i[17]] = 0
                        return
            else:
                self.button4(items)
                self.button7(items)
                self.button11(items)
                return
    
    # BUTTON 7: O - Only OFF (soft)
    def button7(self, items: list):
        if self.board[self.cube_1.x][self.cube_1.y] != 7 and self.board[self.cube_2.x][self.cube_2.y] != 7:
            return

        X, Y = -1, -1
        if self.board[self.cube_1.x][self.cube_1.y] == 7:
            X = self.cube_1.x
            Y = self.cube_1.y
            save = 1
        else:
            X = self.cube_2.x
            Y = self.cube_2.y
            save = 2
            
        for i in items:
            if i[0] == X and i[1] == Y:
                if i[2] == -1: 
                    return
                self.board[i[2]][i[3]] = 0
                if i[4] != -1:
                    self.board[i[4]][i[5]] = 0
                if len(i) > 6:
                    self.board[i[6]][i[7]] = 0
                    if i[8] != -1:
                        self.board[i[8]][i[9]] = 0
                if len(i) > 10:
                    self.board[i[10]][i[11]] = 0
                    if i[12] != -1:
                        self.board[i[12]][i[13]] = 0
                if len(i) > 14:
                    self.board[i[14]][i[15]] = 0
                    if i[16] != -1:
                        self.board[i[16]][i[17]] = 0
                break
        
        two_button = False
        duplicate = False
        
        if save == 1 and (self.board[self.cube_2.x][self.cube_2.y] == 4 or 
                          self.board[self.cube_2.x][self.cube_2.y] == 6 or 
                          self.board[self.cube_2.x][self.cube_2.y] == 7 or
                          self.board[self.cube_2.x][self.cube_2.y] == 11):
            X = self.cube_2.x
            Y = self.cube_2.y
            two_button = True
            if self.board[self.cube_2.x][self.cube_2.y] == 7:
                duplicate = True
        elif save == 2 and (self.board[self.cube_1.x][self.cube_1.y] == 4 or
                            self.board[self.cube_1.x][self.cube_1.y] == 6 or
                            self.board[self.cube_1.x][self.cube_1.y] == 7 or
                            self.board[self.cube_1.x][self.cube_1.y] == 11):
            X = self.cube_1.x
            Y = self.cube_1.y
            two_button = True
            if self.board[self.cube_1.x][self.cube_1.y] == 7:
                duplicate = True
            
        if two_button:
            if duplicate:
                for i in items:
                    if i[0] == X and i[1] == Y:
                        if i[2] == -1: 
                            return
                        self.board[i[2]][i[3]] = 0
                        if i[4] != -1:
                            self.board[i[4]][i[5]] = 0
                        if len(i) > 6:
                            self.board[i[6]][i[7]] = 0
                            if i[8] != -1:
                                self.board[i[8]][i[9]] = 0
                        if len(i) > 10:
                            self.board[i[10]][i[11]] = 0
                            if i[12] != -1:
                                self.board[i[12]][i[13]] = 0
                        if len(i) > 14:
                            self.board[i[14]][i[15]] = 0
                            if i[16] != -1:
                                self.board[i[16]][i[17]] = 0
                        return
            else:
                self.button4(items)
                self.button6(items)
                self.button11(items)
                return
        
            
    # BUTTON 8: Teleport and Split gate
    def button8(self, items: list):  
        if self.split or self.board[self.cube_1.x][self.cube_1.y] != 8 or self.board[self.cube_2.x][self.cube_2.y] != 8:
            return
        
        self.split = True
        
        X, Y = -1, -1
        if self.board[self.cube_1.x][self.cube_1.y] == 8:
            X = self.cube_1.x
            Y = self.cube_1.y
        else:
            X = self.cube_2.x
            Y = self.cube_2.y
            
        for i in items:
            if i[0] == X and i[1] == Y:
                self.cube_1.x = i[2]
                self.cube_1.y = i[3]
                self.cube_2.x = i[4]
                self.cube_2.y = i[5]
                return
            
    # BUTTON 9: X - Only OFF (heavy)
    def button9(self, items: list):
        if self.board[self.cube_1.x][self.cube_1.y] != 9 or self.board[self.cube_2.x][self.cube_2.y] != 9:
            return

        X, Y = -1, -1
        if self.board[self.cube_1.x][self.cube_1.y] == 9:
            X = self.cube_1.x
            Y = self.cube_1.y
        else:
            X = self.cube_2.x
            Y = self.cube_2.y
            
        for i in items:
            if i[0] == X and i[1] == Y:
                if i[2] == -1: 
                    return
                self.board[i[2]][i[3]] = 0
                if i[4] != -1:
                    self.board[i[4]][i[5]] = 0
                if len(i) > 6:
                    self.board[i[6]][i[7]] = 0
                    if i[8] != -1:
                        self.board[i[8]][i[9]] = 0
                return
            
    # BUTTON 10: X - Only ON (heavy)
    def button10(self, items: list):
        if self.board[self.cube_1.x][self.cube_1.y] != 10 or self.board[self.cube_2.x][self.cube_2.y] != 10:
            return

        X, Y = -1, -1
        if self.board[self.cube_1.x][self.cube_1.y] == 10:
            X = self.cube_1.x
            Y = self.cube_1.y
        else:
            X = self.cube_2.x
            Y = self.cube_2.y
            
        for i in items:
            if i[0] == X and i[1] == Y:
                if i[2] == -1: 
                    return
                self.board[i[2]][i[3]] = 1
                if i[4] != -1:
                    self.board[i[4]][i[5]] = 1
                if len(i) > 6:
                    self.board[i[6]][i[7]] = 1
                    if i[8] != -1:
                        self.board[i[8]][i[9]] = 1
                return
            
    # BUTTON 11: O - ON a bridge and OFF a bridge (soft)
    def button11(self, items: list):
        if self.board[self.cube_1.x][self.cube_1.y] != 11 and self.board[self.cube_2.x][self.cube_2.y] != 11:
            return

        X, Y = -1, -1
        if self.board[self.cube_1.x][self.cube_1.y] == 11:
            X = self.cube_1.x
            Y = self.cube_1.y
            save = 1
        else:
            X = self.cube_2.x
            Y = self.cube_2.y
            save = 2
            
        for i in items:
            if i[0] == X and i[1] == Y:
                if i[2] == -1: 
                    return
                self.board[i[2]][i[3]] = 1
                if i[4] != -1:
                    self.board[i[4]][i[5]] = 1
                self.board[i[6]][i[7]] = 0
                if i[8] != -1:
                    self.board[i[8]][i[9]] = 0
                if len(i) > 10:
                    self.board[i[10]][i[11]] = 0
                    if i[12] != -1:
                        self.board[i[12]][i[13]] = 0
                if len(i) > 14:
                    self.board[i[14]][i[15]] = 0
                    if i[16] != -1:
                        self.board[i[16]][i[17]] = 0
                break
            
        two_button = False
        duplicate = False
        
        if save == 1 and (self.board[self.cube_2.x][self.cube_2.y] == 4 or 
                          self.board[self.cube_2.x][self.cube_2.y] == 6 or 
                          self.board[self.cube_2.x][self.cube_2.y] == 7 or
                          self.board[self.cube_2.x][self.cube_2.y] == 11):
            X = self.cube_2.x
            Y = self.cube_2.y
            two_button = True
            if self.board[self.cube_2.x][self.cube_2.y] == 11:
                duplicate = True
        elif save == 2 and (self.board[self.cube_1.x][self.cube_1.y] == 4 or
                            self.board[self.cube_1.x][self.cube_1.y] == 6 or
                            self.board[self.cube_1.x][self.cube_1.y] == 7 or
                            self.board[self.cube_1.x][self.cube_1.y] == 11):
            X = self.cube_1.x
            Y = self.cube_1.y
            two_button = True
            if self.board[self.cube_1.x][self.cube_1.y] == 11:
                duplicate = True
            
        if two_button:
            if duplicate:
                for i in items:
                    if i[0] == X and i[1] == Y:
                        if i[2] == -1: 
                            return
                        self.board[i[2]][i[3]] = 0
                        if i[4] != -1:
                            self.board[i[4]][i[5]] = 0
                        if len(i) > 6:
                            self.board[i[6]][i[7]] = 0
                            if i[8] != -1:
                                self.board[i[8]][i[9]] = 0
                        if len(i) > 10:
                            self.board[i[10]][i[11]] = 0
                            if i[12] != -1:
                                self.board[i[12]][i[13]] = 0
                        if len(i) > 14:
                            self.board[i[14]][i[15]] = 0
                            if i[16] != -1:
                                self.board[i[16]][i[17]] = 0
                        return
            else:
                self.button4(items)
                self.button6(items)
                self.button7(items)
                return
    
    # BUTTON 12: X - ON a bridge and OFF a bridge (heavy)
    def button12(self, items: list):
        if self.board[self.cube_1.x][self.cube_1.y] != 12 or self.board[self.cube_2.x][self.cube_2.y] != 12:
            return

        X, Y = -1, -1
        if self.board[self.cube_1.x][self.cube_1.y] == 12:
            X = self.cube_1.x
            Y = self.cube_1.y
        else:
            X = self.cube_2.x
            Y = self.cube_2.y
            
        for i in items:
            if i[0] == X and i[1] == Y:
                if i[2] == -1: 
                    return
                self.board[i[2]][i[3]] = 1
                if i[4] != -1:
                    self.board[i[4]][i[5]] = 1
                self.board[i[6]][i[7]] = 0
                if i[8] != -1:
                    self.board[i[8]][i[9]] = 0
                if len(i) > 10:
                    self.board[i[10]][i[11]] = 0
                    if i[12] != -1:
                        self.board[i[12]][i[13]] = 0
                if len(i) > 14:
                    self.board[i[14]][i[15]] = 0
                    if i[16] != -1:
                        self.board[i[16]][i[17]] = 0
                return
    
    # Combine 2 cubes into 1 block
    def Fusion(self):
        if (abs(self.cube_1.x - self.cube_2.x) == 1 and abs(self.cube_1.y - self.cube_2.y) == 0) or (abs(self.cube_1.x - self.cube_2.x) == 0 and abs(self.cube_1.y - self.cube_2.y) == 1):
            self.split = False
        return
                    
    def isDead(self):
        if self.board[self.cube_1.x][self.cube_1.y] * self.board[self.cube_2.x][self.cube_2.y] == 0:
            return True
        if self.isStanding() and self.board[self.cube_1.x][self.cube_1.y] == 5:
            return True
        return False
    
    def isGoal(self):
        if self.split:
            return False
        if self.board[self.cube_1.x][self.cube_1.y] == 2 and self.board[self.cube_2.x][self.cube_2.y] == 2:
            return True
        return False
    
def bfs_cube(init: Cube, board: list):
    P = []
    Q = []
    Q.append(init)
    P.append(init)
    while len(Q) > 0:
        current = Q.pop(0)
        
        if current.Goal(board):
            return current
        
        x_up, y_up = current.up()
        cube_1 = Cube(x_up, y_up, current)
        if not cube_1.Dead(board):
            if not cube_1.visited(P):
                Q.append(cube_1)
                P.append(cube_1)
        
        x_down, y_down = current.down()
        cube_2 = Cube(x_down, y_down, current)
        if not cube_2.Dead(board):
            if not cube_2.visited(P):
                Q.append(cube_2)
                P.append(cube_2)
                
        x_right, y_right = current.right()
        cube_3 = Cube(x_right, y_right, current)
        if not cube_3.Dead(board):
            if not cube_3.visited(P):
                Q.append(cube_3)
                P.append(cube_3)
        
        x_left, y_left = current.left()
        cube_4 = Cube(x_left, y_left, current)
        if not cube_4.Dead(board):
            if not cube_4.visited(P):
                Q.append(cube_4)
                P.append(cube_4)
    return None

def dist(cube: Cube, board):
    init = copy.deepcopy(cube)
    init.prev = None
    current = bfs_cube(init, board)
    if current == None:
        return -1
    result = 0
    while current != None:
        result += 1
        current = current.prev
    return result
    
def equal_cube(cub_1: Cube, cub_2: Cube):
    if cub_1.x == cub_2.x and cub_1.y == cub_2.y:
        return True
    return False
    
def equal_block(block_1: Block, block_2: Block):
    if (equal_cube(block_1.cube_1, block_2.cube_1) and equal_cube(block_1.cube_2, block_2.cube_2)) or (equal_cube(block_1.cube_1, block_2.cube_2) and equal_cube(block_1.cube_2, block_2.cube_1)):
        return True
    return False

def getGoal(board: list):
    row, col = np.shape(board)
    for i in range(row):
        for j in range(col):
            if board[i][j] == 2:
                return i, j
    return -1, -1
        
class BFS:
    def __init__(self, 
                 items: list,
    ):
        self.items = items # list of items (X, O button,...) in the board
        self.passed = [] # list of passed states
        
    def visited(self, block: Block):
        for i in self.passed:
            if equal_block(i, block) and i.board == block.board:
                return True
        return False
    
    def button(self, block: Block):
        block.button3(self.items)
        block.button4(self.items)
        block.button6(self.items)
        block.button7(self.items)
        block.button8(self.items)
        block.button9(self.items)
        block.button10(self.items)
        block.button11(self.items)
        block.button12(self.items)
    
    def path(self, block: Block):
        temp = block
        result = []
        b = []
        while block.parent_step != "- START":
            result.insert(0, block.parent_step)
            b.insert(0, block)
            block = block.parent
        result.insert(0, block.parent_step)
        b.insert(0, block)
        for i in range(len(result)):
            f.write(result[i] + ': (' + str(b[i].cube_1.x) + ', ' + str(b[i].cube_1.y) + '), (' + str(b[i].cube_2.x) + ', ' + str(b[i].cube_2.y) + ')\n')
        f.write('--> GOAL: (' + str(temp.cube_1.x) + ', ' + str(temp.cube_1.y) + '), (' + str(temp.cube_2.x) + ', ' + str(temp.cube_2.y) + ')\n')
       
    def process(self, queue: list, block: Block, split: bool,):
        if not block.isDead():
            self.button(block)
            if split:
                block.Fusion()
            if not self.visited(block):
                queue.append(block)
                self.passed.append(block)
        return
        
    def bfs(self, init_block: Block):
        self.passed = []
        queue = []
        queue.append(init_block)
        self.passed.append(init_block)
        while len(queue) > 0:
            current = queue.pop(0)
            
            if current.isGoal():
                print("\nSUCCESS!!!")
                self.path(current)
                return True
            
            if not current.split:
                # Move up
                up_1, up_2 = current.up()
                temp_up = Block(up_1, up_2, current, "- UP", current.board)
                self.process(queue, temp_up, False)
                
                # Move down
                down_1, down_2 = current.down()
                temp_down = Block(down_1, down_2, current, "- DOWN", current.board)
                self.process(queue, temp_down, False)
                
                # Move right
                right_1, right_2 = current.right()
                temp_right = Block(right_1, right_2, current, "- RIGHT", current.board)
                self.process(queue, temp_right, False)
                
                # Move left
                left_1, left_2 = current.left()
                temp_left = Block(left_1, left_2, current, "- LEFT", current.board)
                self.process(queue, temp_left, False)
                
            else:
                # Cube 1 move up
                c1_up1, c1_up2 = current.cube_1_up()
                temp1_up = Block(c1_up1, c1_up2, current, "- CUBE 1 UP", current.board, True)
                self.process(queue, temp1_up, True)
                
                # Cube 1 move down
                c1_down1, c1_down2 = current.cube_1_down()
                temp1_down = Block(c1_down1, c1_down2, current, "- CUBE 1 DOWN", current.board, True)
                self.process(queue, temp1_down, True)
                        
                # Cube 1 move right
                c1_right1, c1_right2 = current.cube_1_right()
                temp1_right = Block(c1_right1, c1_right2, current, "- CUBE 1 RIGHT", current.board, True)
                self.process(queue, temp1_right, True)
                        
                # Cube 1 move left
                c1_left1, c1_left2 = current.cube_1_left()
                temp1_left = Block(c1_left1, c1_left2, current, "- CUBE 1 LEFT", current.board, True)
                self.process(queue, temp1_left, True)
                
                # Cube 2 move up
                c2_up1, c2_up2 = current.cube_2_up()
                temp2_up = Block(c2_up1, c2_up2, current, "- CUBE 2 UP", current.board, True)
                self.process(queue, temp2_up, True)
                
                # Cube 2 move down
                c2_down1, c2_down2 = current.cube_2_down()
                temp2_down = Block(c2_down1, c2_down2, current, "- CUBE 2 DOWN", current.board, True)
                self.process(queue, temp2_down, True)
                        
                # Cube 2 move right
                c2_right1, c2_right2 = current.cube_2_right()
                temp2_right = Block(c2_right1, c2_right2, current, "- CUBE 2 RIGHT", current.board, True)
                self.process(queue, temp2_right, True)
                        
                # Cube 2 move left
                c2_left1, c2_left2 = current.cube_2_left()
                temp2_left = Block(c2_left1, c2_left2, current, "- CUBE 2 LEFT", current.board, True)
                self.process(queue, temp2_left, True)
                        
        print("\nUNSUCCESS!!!")
        return False
    
class GENETIC:
    def __init__(self,
                 items: list,
                 board: list,
                 lenADN: int = 50,
                 numADN: int = 200,
    ):
        self.items, self.board = items, board
        self.lenADN, self.numADN = lenADN, numADN
        self.goal_x, self.goal_y = getGoal(self.board)
        self.ADNs = []
        
    def button(self, block: Block):
        block.button3(self.items)
        block.button4(self.items)
        block.button6(self.items)
        block.button7(self.items)
        block.button8(self.items)
        block.button9(self.items)
        block.button10(self.items)
        block.button11(self.items)
        block.button12(self.items)
        
    def process(self, block: Block):
        self.button(block)
        if block.split:
            block.Fusion()
        return
        
    def random_move(self, block: Block):
        rand = random.randint(0, 4)
        if rand == 0:
            cube_1, cube_2 = block.up()
            return Block(cube_1, cube_2, block, "- UP", block.board, block.split)
        elif rand == 1:
            cube_1, cube_2 = block.down()
            return Block(cube_1, cube_2, block, "- DOWN", block.board, block.split)
        elif rand == 2:
            cube_1, cube_2 = block.right()
            return Block(cube_1, cube_2, block, "- RIGHT", block.board, block.split)
        elif rand == 3:
            cube_1, cube_2 = block.left()
            return Block(cube_1, cube_2, block, "- LEFT", block.board, block.split)
        else:
            cube_1, cube_2 = block.cube_1, block.cube_2
            return Block(cube_1, cube_2, block, "- NONE", block.board, block.split)
        
    def random_move_split(self, block: Block):
        rand = random.randint(0, 8)
        if rand == 0:
            cube_1, cube_2 = block.cube_1_up()
            return Block(cube_1, cube_2, block, "- CUBE 1 UP", block.board, block.split)
        elif rand == 1:
            cube_1, cube_2 = block.cube_1_down()
            return Block(cube_1, cube_2, block, "- CUBE 1 DOWN", block.board, block.split)
        elif rand == 2:
            cube_1, cube_2 = block.cube_1_right()
            return Block(cube_1, cube_2, block, "- CUBE 1 RIGHT", block.board, block.split)
        elif rand == 3:
            cube_1, cube_2 = block.cube_1_left()
            return Block(cube_1, cube_2, block, "- CUBE 1 LEFT", block.board, block.split)
        elif rand == 4:
            cube_1, cube_2 = block.cube_2_up()
            return Block(cube_1, cube_2, block, "- CUBE 2 UP", block.board, block.split)
        elif rand == 5:
            cube_1, cube_2 = block.cube_2_down()
            return Block(cube_1, cube_2, block, "- CUBE 2 DOWN", block.board, block.split)
        elif rand == 6:
            cube_1, cube_2 = block.cube_2_right()
            return Block(cube_1, cube_2, block, "- CUBE 2 RIGHT", block.board, block.split)
        elif rand == 7:
            cube_1, cube_2 = block.cube_2_left()
            return Block(cube_1, cube_2, block, "- CUBE 2 LEFT", block.board, block.split)
        else:
            cube_1, cube_2 = block.cube_1, block.cube_2
            return Block(cube_1, cube_2, block, "- NONE", block.board, block.split)
        
    def InitGen(self, init_block: Block, size: int):
        ADN = []
        ADN.append(init_block)
        for i in range(size - 1):
            current = ADN[len(ADN) - 1]
            if not current.split:
                while True:
                    block = self.random_move(current)
                    if not block.isDead():
                        self.process(block)
                        ADN.append(block)
                        break
            else:
                while True:
                    block = self.random_move_split(current)
                    if not block.isDead():
                        self.process(block)
                        ADN.append(block)
                        break
        return ADN
        
    def InitialPopulation(self, init_block: Block):
        for idx in range(self.numADN):
            ADN = self.InitGen(init_block, self.lenADN)
            self.ADNs.append(ADN)
        return
    
    def FitnessFunction(self, ADN: list):
        result = 5000
        
        # Bonus score
        for block in ADN:
            # Check if the block is in orange tiles
            if not block.isStanding():
                if self.board[block.cube_1.x][block.cube_1.y] == 5:
                    result += 30
                    self.board[block.cube_1.x][block.cube_1.y] = 9
                if self.board[block.cube_2.x][block.cube_2.y] == 5:
                    result += 30
                    self.board[block.cube_2.x][block.cube_2.y] = 9
            
            # Check if the block is in X button
            if block.isStanding():
                if self.board[block.cube_1.x][block.cube_1.y] == 3:
                    result += 100
                    self.board[block.cube_1.x][block.cube_1.y] = 9
                    
            # Check if the block is in O button
            if (
                self.board[block.cube_1.x][block.cube_1.y] == 4 or self.board[block.cube_2.x][block.cube_2.y] == 4 or
                self.board[block.cube_1.x][block.cube_1.y] == 6 or self.board[block.cube_2.x][block.cube_2.y] == 6 or
                self.board[block.cube_1.x][block.cube_1.y] == 7 or self.board[block.cube_2.x][block.cube_2.y] == 7
            ):
                result += 100
                if self.board[block.cube_1.x][block.cube_1.y] == 4 or self.board[block.cube_1.x][block.cube_1.y] == 6 or self.board[block.cube_1.x][block.cube_1.y] == 7:
                    self.board[block.cube_1.x][block.cube_1.y] = 9
                else:
                    self.board[block.cube_2.x][block.cube_2.y] = 9
                    
            # Check if the block is in Teleport gates
            if block.isStanding():
                if self.board[block.cube_1.x][block.cube_1.y] == 8:
                    result += 100
                    self.board[block.cube_1.x][block.cube_1.y] = 9
                    
            # Check if the tile is among orange tiles
            if block.isStanding():
                if (
                    self.board[block.cube_1.x][block.cube_1.y] == 1 and
                    self.board[block.cube_1.x - 1][block.cube_1.y] == 5 and
                    self.board[block.cube_1.x + 1][block.cube_1.y] == 5 and
                    self.board[block.cube_1.x][block.cube_1.y - 1] == 5 and
                    self.board[block.cube_1.x][block.cube_1.y + 1] == 5
                ):
                    result += 100
                    self.board[block.cube_1.x][block.cube_1.y] = 9
            
        # Main score
        second_last = ADN[self.lenADN - 2]
        
        # Check if the block is really near the goal
        if not second_last.isStanding():
            if (
                (second_last.cube_1.x == self.goal_x - 1 and second_last.cube_2.x == self.goal_x - 2 and second_last.cube_1.y == self.goal_y and second_last.cube_2.y == self.goal_y) or
                (second_last.cube_1.x == self.goal_x - 2 and second_last.cube_2.x == self.goal_x - 1 and second_last.cube_1.y == self.goal_y and second_last.cube_2.y == self.goal_y) or 
                (second_last.cube_1.x == self.goal_x + 1 and second_last.cube_2.x == self.goal_x + 2 and second_last.cube_1.y == self.goal_y and second_last.cube_2.y == self.goal_y) or
                (second_last.cube_1.x == self.goal_x + 2 and second_last.cube_2.x == self.goal_x + 1 and second_last.cube_1.y == self.goal_y and second_last.cube_2.y == self.goal_y) or
                (second_last.cube_1.y == self.goal_y - 1 and second_last.cube_2.y == self.goal_y - 2 and second_last.cube_1.x == self.goal_x and second_last.cube_2.x == self.goal_x) or
                (second_last.cube_1.y == self.goal_y - 2 and second_last.cube_2.y == self.goal_y - 1 and second_last.cube_1.x == self.goal_x and second_last.cube_2.x == self.goal_x) or  
                (second_last.cube_1.y == self.goal_y + 1 and second_last.cube_2.y == self.goal_y + 2 and second_last.cube_1.x == self.goal_x and second_last.cube_2.x == self.goal_x) or
                (second_last.cube_1.y == self.goal_y + 2 and second_last.cube_2.y == self.goal_y + 1 and second_last.cube_1.x == self.goal_x and second_last.cube_2.x == self.goal_x)
            ): 
                result += 200
        
        last_block = ADN[self.lenADN - 1]
        if last_block.isStanding():
            if self.board[last_block.cube_1.x][last_block.cube_1.y] == 2:
                result += 100000
        
        distance = dist(last_block.cube_1, self.board) + dist(last_block.cube_2, self.board) # !!!
        result -= distance
        return result
            
    def sorted(self):
        self.ADNs.sort(key = self.FitnessFunction, reverse = True)
        
    def Crossover(self):
        self.sorted()
        count = int(self.numADN / 4)
        for i in range(count):
            ADN_1 = random.randint(0, self.numADN / 2)
            ADN_2 = random.randint(0, self.numADN / 2)
            while ADN_2 == ADN_1:
                ADN_2 = random.randint(0, self.numADN / 2)
            for i in range(self.lenADN):
                if equal_block(self.ADNs[ADN_1][i], self.ADNs[ADN_2][i]):
                    child1, child2 = copy.deepcopy(self.ADNs[ADN_1]), copy.deepcopy(self.ADNs[ADN_2])
                    child1[i:] = copy.deepcopy(self.ADNs[ADN_2][i:])
                    child2[i:] = copy.deepcopy(self.ADNs[ADN_1][i:])
                    self.ADNs.append(child1)
                    self.ADNs.append(child2)
                    break
        self.sorted()
        self.ADNs = self.ADNs[0:self.numADN]
    
    def Mutation(self):
        self.sorted()
        count = int(self.numADN / 2)
        for i in range(count):
            index_ADN = random.randint(0, self.numADN - 1)
            index_Gen = random.randint(int(self.lenADN / 2), self.lenADN - 1)
            self.ADNs[index_ADN][index_Gen:] = self.InitGen(self.ADNs[index_ADN][index_Gen], self.lenADN - index_Gen)
    
    def path(self, ADN: list):
        last = ADN[0]
        for i in ADN:
            f.write(i.parent_step + ': (' + str(i.cube_1.x) + ', ' + str(i.cube_1.y) + '), (' + str(i.cube_2.x) + ', ' + str(i.cube_2.y) + ')\n')
            last = i
            if i.isGoal():
                break
        f.write('--> GOAL: (' + str(last.cube_1.x) + ', ' + str(last.cube_1.y) + '), (' + str(last.cube_2.x) + ', ' + str(last.cube_2.y) + ')\n')
        
    def Genetic(self, init_block: Block):
        count = 0
        self.InitialPopulation(init_block)
        while True:
            count += 1
            for i in self.ADNs:
                if i[len(i) - 1].isGoal():
                    print("\nSUCCESS!!!")
                    self.path(i)
                    return
                
            # self.sorted()
            # b = self.ADNs[0][len(self.ADNs[0]) - 1]
            # print("Loop " + str(count) + ": " + str(self.FitnessFunction(self.ADNs[0])) + " --> "
                  # + '(' + str(b.cube_1.x) + ', ' + str(b.cube_1.y) + '), (' + str(b.cube_2.x) + ', ' + str(b.cube_2.y) + ')')
            
            self.Crossover()
            self.Mutation()

start = timeit.default_timer()

if sys.argv[1:][1] == 'BFS'  or sys.argv[1:][1] == 'bfs':
    file = 'Output\BFS_Stage_' + str(sys.argv[1:][0]) + '.txt'
    
elif sys.argv[1:][1] == 'Genetic' or sys.argv[1:][1] == 'genetic':
    file = 'Output\Genetic_Stage_' + str(sys.argv[1:][0]) + '.txt'

with open(file, 'w') as f:

    board, items, init_x, init_y = readBoard('Stage\Stage_' + str(sys.argv[1:][0]) + '.txt')
    printBoard(board)

    cube = Cube(init_x, init_y)
    init_block = Block(cube_1 = cube, cube_2 = cube, board = board)

    if sys.argv[1:][1] == 'BFS'  or sys.argv[1:][1] == 'bfs':
        solver = BFS(items)
        solver.bfs(init_block)
        
    elif sys.argv[1:][1] == 'Genetic' or sys.argv[1:][1] == 'genetic':
        full = fullBoard(board, items)
        solver = GENETIC(items, full)
        solver.Genetic(init_block)
    
    stop = timeit.default_timer()
    f.write('Time: ' + str(round(stop - start, 4))  + ' s\n')

    process = psutil.Process(os.getpid())
    f.write('Memory: ' + str(round(process.memory_info().rss / (1024 * 1024), 2)) + " MB")  # in bytes 