# x-axis is vertical, point down
# y-axis is horizontal, point right

# 0: DEAD
# 1: NORMAL
# 2: GOAL
# 3: X - ON and OFF (heavy)
# 4: O - ON and OFF (soft)

def printBoard(board):
    print("Board: ")
    print("======================================================")
    for i in board:
        print(i)
    print("======================================================")

class Cube:
    def __init__(self, X, Y):
        self.x = X
        self.y = Y
        
class Block:
    def __init__(self, 
                 cube_1: Cube,
                 cube_2: Cube,
                 parent: 'Block' = None,
                 parent_step: str = "START",
    ):
        self.cube_1 = cube_1
        self.cube_2 = cube_2
        self.parent = parent
        self.parent_step = parent_step
        
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
                    
    def isDead(self, board):
        if board[self.cube_1.x][self.cube_1.y] * board[self.cube_2.x][self.cube_2.y] == 0:
            return True
        return False
    
    def isGoal(self, board):
        if board[self.cube_1.x][self.cube_1.y] == 2 and board[self.cube_2.x][self.cube_2.y] == 2:
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
    def __init__(self, 
                 board: list,
                 items: list,):
        self.board = board
        self.items = items
        self.passed = []
        self.passed_board = []
        
    def visited(self, block: Block):
        count = 0
        for i in self.passed:
            if equal_block(i, block) and self.passed_board[count] == self.board:
                return True
            count += 1
        return False
    
    # BUTTON 3: X - ON and OFF (heavy)
    def button3(self, block: Block):
        if block.isStanding():
            if self.board[block.cube_1.x][block.cube_1.y] != 3:
                return
            
            line = 0
            for i in range(len(self.items)):
                if self.items[i][0] == block.cube_1.x and self.items[i][1] == block.cube_1.y:
                    line = i
                    break
                
            if self.board[self.items[line][2]][self.items[line][3]] == 1:
                self.board[self.items[line][2]][self.items[line][3]] = 0
                self.board[self.items[line][4]][self.items[line][5]] = 0
            else:
                self.board[self.items[line][2]][self.items[line][3]] = 1
                self.board[self.items[line][4]][self.items[line][5]] = 1
        return
    
    # BUTTON 4: O - ON and OFF (soft)
    def button4(self, block: Block):
        if self.board[block.cube_1.x][block.cube_1.y] != 4 and self.board[block.cube_2.x][block.cube_2.y] != 4:
            return
        
        X, Y = -1, -1
        if self.board[block.cube_1.x][block.cube_1.y] == 4:
            X = block.cube_1.x
            Y = block.cube_1.y
        else:
            X = block.cube_2.x
            Y = block.cube_2.y
            
        line = 0
        for i in range(len(self.items)):
            if self.items[i][0] == X and self.items[i][1] == Y:
                line = i
                break
        
        if self.board[self.items[line][2]][self.items[line][3]] == 1:
            self.board[self.items[line][2]][self.items[line][3]] = 0
            self.board[self.items[line][4]][self.items[line][5]] = 0
        else:
            self.board[self.items[line][2]][self.items[line][3]] = 1
            self.board[self.items[line][4]][self.items[line][5]] = 1
    
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
            print(result[i] + ': (' + str(b[i].cube_1.x) + ', ' + str(b[i].cube_1.y) + '), (' + str(b[i].cube_2.x) + ', ' + str(b[i].cube_2.y) + ')')
        print('GOAL: (' + str(temp.cube_1.x) + ', ' + str(temp.cube_1.y) + '), (' + str(temp.cube_2.x) + ', ' + str(temp.cube_2.y) + ')')
        
    def BFS(self, init_block: Block):
        self.passed = []
        queue = []
        queue.append(init_block)
        while len(queue) > 0:
            current = queue.pop(0)
            self.passed.append(current)
            self.passed_board.append(self.board)
            
            # print('(' + str(current.cube_1.x) + ', ' + str(current.cube_1.y) + '), (' + str(current.cube_2.x) + ', ' + str(current.cube_2.y) + ')')
            # printBoard(self.board)
            
            if (current.isGoal(self.board)):
                print("SUCCESS, FOLLOW THiS INSTRUCTION:")
                self.path(current)
                return True
            
            self.button3(current)
            self.button4(current)
            
            # Move up
            up_1, up_2 = current.up()
            temp_up = Block(up_1, up_2, current, "UP")
            if not temp_up.isDead(self.board):
                if not self.visited(temp_up):
                    queue.append(temp_up)
            
            # Move down
            down_1, down_2 = current.down()
            temp_down = Block(down_1, down_2, current, "DOWN")
            if not temp_down.isDead(self.board):
                if not self.visited(temp_down):
                    queue.append(temp_down)
            
            # Move right
            right_1, right_2 = current.right()
            temp_right = Block(right_1, right_2, current, "RIGHT")
            if not temp_right.isDead(self.board):
                if not self.visited(temp_right):
                    queue.append(temp_right)
            
            # Move left
            left_1, left_2 = current.left()
            temp_left = Block(left_1, left_2, current, "LEFT")
            if not temp_left.isDead(self.board):
                if not self.visited(temp_left):
                    queue.append(temp_left)
                    
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

board, items, init_x, init_y = readBoard("Stage_2.txt")
printBoard(board)
cube = Cube(init_x, init_y)
init_block = Block(cube, cube)
state = State(board, items)
print(state.BFS(init_block))