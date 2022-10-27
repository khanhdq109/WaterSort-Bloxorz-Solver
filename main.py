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
# 8: X - ON and OFF (heavy) but only creat 1 tiles

import copy

def printBoard(board):
    print("======================================================")
    for i in board:
        print(i)
    print("======================================================")

class Cube:
    def __init__(self, X, Y):
        self.x = copy.deepcopy(X)
        self.y = copy.deepcopy(Y)
        
class Block:
    def __init__(self, 
                 cube_1: Cube,
                 cube_2: Cube,
                 parent: 'Block' = None,
                 parent_step: str = "START",
                 board: list = None,
    ):
        self.cube_1 = cube_1
        self.cube_2 = cube_2
        self.parent = parent
        self.parent_step = parent_step
        self.board = copy.deepcopy(board)
        
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
                    
    def isDead(self):
        if self.board[self.cube_1.x][self.cube_1.y] * self.board[self.cube_2.x][self.cube_2.y] == 0:
            return True
        if self.isStanding() and self.board[self.cube_1.x][self.cube_1.y] == 5:
            return True
        return False
    
    def isGoal(self):
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
        
class State:
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
            
    # BUTTON 6: Only ON (soft)
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
    
    # BUTTON 7: Only OFF (soft)
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
            # printBoard(b[i].board)
        print('\nGOAL: (' + str(temp.cube_1.x) + ', ' + str(temp.cube_1.y) + '), (' + str(temp.cube_2.x) + ', ' + str(temp.cube_2.y) + ')\n')
        
    def BFS(self, init_block: Block):
        self.passed = []
        queue = []
        queue.append(init_block)
        while len(queue) > 0:
            current = queue.pop(0)
            
            if (current.isGoal()):
                print("\nSUCCESS, FOLLOW THiS INSTRUCTION:")
                self.path(current)
                return True
            
            # Move up
            up_1, up_2 = current.up()
            temp_up = Block(up_1, up_2, current, "UP", current.board)
            if not temp_up.isDead():
                self.button3(temp_up)
                self.button4(temp_up)
                self.button6(temp_up)
                self.button7(temp_up)
                if not self.visited(temp_up):
                    queue.append(temp_up)
                    self.passed.append(current)
            
            # Move down
            down_1, down_2 = current.down()
            temp_down = Block(down_1, down_2, current, "DOWN", current.board)
            if not temp_down.isDead():
                self.button3(temp_down)
                self.button4(temp_down)
                self.button6(temp_down)
                self.button7(temp_down)
                if not self.visited(temp_down):
                    queue.append(temp_down)
                    self.passed.append(current)
            
            # Move right
            right_1, right_2 = current.right()
            temp_right = Block(right_1, right_2, current, "RIGHT", current.board)
            if not temp_right.isDead():
                self.button3(temp_right)
                self.button4(temp_right)
                self.button6(temp_right)
                self.button7(temp_right)
                if not self.visited(temp_right):
                    queue.append(temp_right)
                    self.passed.append(current)
            
            # Move left
            left_1, left_2 = current.left()
            temp_left = Block(left_1, left_2, current, "LEFT", current.board)
            if not temp_left.isDead():
                self.button3(temp_left)
                self.button4(temp_left)
                self.button6(temp_left)
                self.button7(temp_left)
                if not self.visited(temp_left):
                    queue.append(temp_left)
                    self.passed.append(current)
                    
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

board, items, init_x, init_y = readBoard("Stage_7.txt")
printBoard(board)
cube = Cube(init_x, init_y)
init_block = Block(cube_1 = cube, cube_2 = cube, board = board)
state = State(items)
state.BFS(init_block)