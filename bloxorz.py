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

import sys
import copy
import numpy as np

def printBoard(board):
    row, col = np.shape(board)
    print('=' * col * 3)
    for i in board:
        print(i)
    print('=' * col * 3)

class Cube:
    def __init__(self, 
                 X: int, 
                 Y: int,):
        self.x = copy.deepcopy(X)
        self.y = copy.deepcopy(Y) 
           
class Block:
    def __init__(self, 
                 cube_1: Cube,
                 cube_2: Cube,
                 parent: 'Block' = None,
                 parent_step: str = "START",
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
    
def equal_cube(cub_1: Cube, cub_2: Cube):
    if cub_1.x == cub_2.x and cub_1.y == cub_2.y:
        return True
    return False
    
def equal_block(block_1: Block, block_2: Block):
    if (equal_cube(block_1.cube_1, block_2.cube_1) and equal_cube(block_1.cube_2, block_2.cube_2)) or (equal_cube(block_1.cube_1, block_2.cube_2) and equal_cube(block_1.cube_2, block_2.cube_1)):
        return True
    return False
        
class Solver:
    def __init__(self, items: list):
        self.items = items # list of items (X, O button,...) in the board
        self.passed = [] # list of passed states
        
    def visited(self, block: Block):
        for i in self.passed:
            if equal_block(i, block) and i.board == block.board:
                return True
        return False
    
    # BUTTON 3: X - ON and OFF (heavy)
    def button3(self, block: Block):
        if block.board[block.cube_1.x][block.cube_1.y] != 3 or block.board[block.cube_2.x][block.cube_2.y] != 3:
            return
        
        for i in self.items:
            if i[0] == block.cube_1.x and i[1] == block.cube_1.y:
                if i[2] == -1: 
                    return # X button but no bridge is created
                if block.board[i[2]][i[3]] == 0:
                    block.board[i[2]][i[3]] = 1
                    if i[4] != -1: # Sometimes we just creat one tile
                        block.board[i[4]][i[5]] = 1
                else:
                    block.board[i[2]][i[3]] = 0
                    if i[4] != -1: # Sometimes we just erase one tile
                        block.board[i[4]][i[5]] = 0
                if len(i) == 10: # Creat 2 bridge
                    if block.board[i[6]][i[7]] == 0:
                        block.board[i[6]][i[7]] = 1
                        if i[8] != -1: # Sometimes we just erase one tile
                            block.board[i[8]][i[9]] = 1
                    else:
                        block.board[i[6]][i[7]] = 0
                        if i[8] != -1: # Sometimes we just erase one tile
                            block.board[i[8]][i[9]] = 0
                return
    
    # BUTTON 4: O - ON and OFF (soft)
    def button4(self, block: Block):
        if block.board[block.cube_1.x][block.cube_1.y] != 4 and block.board[block.cube_2.x][block.cube_2.y] != 4:
            return
        
        X, Y = -1, -1
        if block.board[block.cube_1.x][block.cube_1.y] == 4:
            X = block.cube_1.x
            Y = block.cube_1.y
        else:
            X = block.cube_2.x
            Y = block.cube_2.y
            
        for i in self.items:
            if i[0] == X and i[1] == Y:
                if block.board[i[2]][i[3]] == 0:
                    block.board[i[2]][i[3]] = 1
                    block.board[i[4]][i[5]] = 1
                else:
                    block.board[i[2]][i[3]] = 0
                    block.board[i[4]][i[5]] = 0
                return
            
    # BUTTON 6: O - Only ON (soft)
    def button6(self, block: Block):
        if block.board[block.cube_1.x][block.cube_1.y] != 6 and block.board[block.cube_2.x][block.cube_2.y] != 6:
            return

        X, Y = -1, -1
        if block.board[block.cube_1.x][block.cube_1.y] == 6:
            X = block.cube_1.x
            Y = block.cube_1.y
        else:
            X = block.cube_2.x
            Y = block.cube_2.y
            
        for i in self.items:
            if i[0] == X and i[1] == Y:
                block.board[i[2]][i[3]] = 1
                block.board[i[4]][i[5]] = 1
                return
    
    # BUTTON 7: O - Only OFF (soft)
    def button7(self, block: Block):
        if block.board[block.cube_1.x][block.cube_1.y] != 7 and block.board[block.cube_2.x][block.cube_2.y] != 7:
            return

        X, Y = -1, -1
        if block.board[block.cube_1.x][block.cube_1.y] == 7:
            X = block.cube_1.x
            Y = block.cube_1.y
        else:
            X = block.cube_2.x
            Y = block.cube_2.y
            
        for i in self.items:
            if i[0] == X and i[1] == Y:
                block.board[i[2]][i[3]] = 0
                block.board[i[4]][i[5]] = 0
                return
            
    # BUTTON 8: Teleport and Split gate
    def button8(self, block: Block):  
        if block.split or block.board[block.cube_1.x][block.cube_1.y] != 8 or block.board[block.cube_2.x][block.cube_2.y] != 8:
            return
        
        block.split = True
        
        X, Y = -1, -1
        if block.board[block.cube_1.x][block.cube_1.y] == 8:
            X = block.cube_1.x
            Y = block.cube_1.y
        else:
            X = block.cube_2.x
            Y = block.cube_2.y
            
        for i in self.items:
            if i[0] == X and i[1] == Y:
                block.cube_1.x = i[2]
                block.cube_1.y = i[3]
                block.cube_2.x = i[4]
                block.cube_2.y = i[5]
                return
            
    # Combine 2 cubes into 1 block
    def Fusion(self, block: Block):
        if (abs(block.cube_1.x - block.cube_2.x) == 1 and abs(block.cube_1.y - block.cube_2.y) == 0) or (abs(block.cube_1.x - block.cube_2.x) == 0 and abs(block.cube_1.y - block.cube_2.y) == 1):
            block.split = False
        return
    
    def button(self, block: Block):
        self.button3(block)
        self.button4(block)
        self.button6(block)
        self.button7(block)
        self.button8(block)
    
    def path(self, block: Block):
        temp = block
        result = []
        b = []
        while block.parent_step != "START":
            result.insert(0, block.parent_step)
            b.insert(0, block)
            block = block.parent
        result.insert(0, block.parent_step)
        b.insert(0, block)
        for i in range(len(result)):
            print('\n'+ result[i] + ': (' + str(b[i].cube_1.x) + ', ' + str(b[i].cube_1.y) + '), (' + str(b[i].cube_2.x) + ', ' + str(b[i].cube_2.y) + ')')
        print('\nGOAL: (' + str(temp.cube_1.x) + ', ' + str(temp.cube_1.y) + '), (' + str(temp.cube_2.x) + ', ' + str(temp.cube_2.y) + ')\n')
       
    def process(self, queue: list, block: Block, split: bool,):
        if not block.isDead():
            self.button(block)
            if split:
                self.Fusion(block)
            if not self.visited(block):
                queue.append(block)
                self.passed.append(block)
        return
        
    def BFS(self, init_block: Block):
        self.passed = []
        queue = []
        queue.append(init_block)
        self.passed.append(init_block)
        while len(queue) > 0:
            current = queue.pop(0)
            
            if (current.isGoal()):
                print("\nSUCCESS, FOLLOW THiS INSTRUCTION:")
                self.path(current)
                return True
            
            if not current.split:
                # Move up
                up_1, up_2 = current.up()
                temp_up = Block(up_1, up_2, current, "UP", current.board)
                self.process(queue, temp_up, False)
                
                # Move down
                down_1, down_2 = current.down()
                temp_down = Block(down_1, down_2, current, "DOWN", current.board)
                self.process(queue, temp_down, False)
                
                # Move right
                right_1, right_2 = current.right()
                temp_right = Block(right_1, right_2, current, "RIGHT", current.board)
                self.process(queue, temp_right, False)
                
                # Move left
                left_1, left_2 = current.left()
                temp_left = Block(left_1, left_2, current, "LEFT", current.board)
                self.process(queue, temp_left, False)
                
            else:
                # Cube 1 move up
                c1_up1, c1_up2 = current.cube_1_up()
                temp1_up = Block(c1_up1, c1_up2, current, "CUBE 1 UP", current.board, True)
                self.process(queue, temp1_up, True)
                
                # Cube 1 move down
                c1_down1, c1_down2 = current.cube_1_down()
                temp1_down = Block(c1_down1, c1_down2, current, "CUBE 1 DOWN", current.board, True)
                self.process(queue, temp1_down, True)
                        
                # Cube 1 move right
                c1_right1, c1_right2 = current.cube_1_right()
                temp1_right = Block(c1_right1, c1_right2, current, "CUBE 1 RIGHT", current.board, True)
                self.process(queue, temp1_right, True)
                        
                # Cube 1 move left
                c1_left1, c1_left2 = current.cube_1_left()
                temp1_left = Block(c1_left1, c1_left2, current, "CUBE 1 LEFT", current.board, True)
                self.process(queue, temp1_left, True)
                
                # Cube 2 move up
                c2_up1, c2_up2 = current.cube_2_up()
                temp2_up = Block(c2_up1, c2_up2, current, "CUBE 2 UP", current.board, True)
                self.process(queue, temp2_up, True)
                
                # Cube 2 move down
                c2_down1, c2_down2 = current.cube_2_down()
                temp2_down = Block(c2_down1, c2_down2, current, "CUBE 2 DOWN", current.board, True)
                self.process(queue, temp2_down, True)
                        
                # Cube 2 move right
                c2_right1, c2_right2 = current.cube_2_right()
                temp2_right = Block(c2_right1, c2_right2, current, "CUBE 2 RIGHT", current.board, True)
                self.process(queue, temp2_right, True)
                        
                # Cube 2 move left
                c2_left1, c2_left2 = current.cube_2_left()
                temp2_left = Block(c2_left1, c2_left2, current, "CUBE 2 LEFT", current.board, True)
                self.process(queue, temp2_left, True)
                        
        print("UNSUCCESS!!!")
        return False
    
def readBoard(file):
    with open(file) as f:
        # Read the first line to get shape of board, initialize coordinate of block
        row, init_x, init_y = [int(x) for x in next(f).split()]
        
        # Read the board
        board = []
        count = 0
        for line in f:
            board.append([int(x) for x in line.split()])
            count += 1
            if count == row: 
                break
            
        # Read the items
        items = []
        for line in f:
            items.append([int(x) for x in line.split()])
            
    return board, items, init_x, init_y

board, items, init_x, init_y = readBoard('Stage\Stage_' + str(sys.argv[1:][0]) + '.txt')
printBoard(board)
cube = Cube(init_x, init_y)
init_block = Block(cube_1 = cube, cube_2 = cube, board = board)
state = Solver(items)
state.BFS(init_block)