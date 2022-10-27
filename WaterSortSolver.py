from queue import Queue,PriorityQueue
from collections import deque
from copy import copy
import numpy as np
import time
import random
import heapq

class CusQueue:
    def __init__(self):
        self.data = []
        self.index = 0
        self.count = 0
    def push(self, item, priority):
        heapq.heappush(self.data, (-priority, self.index, item))
        self.index += 1
        self.count += 1
    def pop(self):
        if self.count != 0:
            self.count -= 1
            return heapq.heappop(self.data)[-1]
    def empty(self):
        return self.count == 0

class State:
    def __init__(self, lst: np.array , child = [], parent = None):
        self.lst = copy(lst)
        self.child = child
        self.parent = parent
        
    def __ne__(self, other) -> bool:
        if other is None: 
            return self is not None
        else:
            return self.lst == other.lst
    
    def __lt__(self, other)->bool:
        return random.randint(0,1)
    
    def __eq__(self, other) -> bool:
        return np.array_equal(self.lst, other.lst)
    
    def __key(self):
        s = 0
        for x in range(0,len(self.lst)):
            if len(self.lst[x][0]) != 0:
                s += ord(self.lst[x][0][0])*(10**x)
        return s
    
    def __hash__(self) -> int:
        return self.__key()
    
    def is_solved(self) -> bool:
        for x in self.lst:
            if x[0]:
                if not np.all(x == x[0]):
                    return False
        return True
    
def move(s:State, pos1:int, pos2: int) -> State:
    temp = copy(s.lst)
    if temp[pos1][0] == '':
        return State(np.array([]))
    elif temp[pos2][0] == '':
        pos = 0
        for i in range(0,4):
            if temp[pos1][i] != '':
                pos = i
        a = temp[pos1][pos]
        index = 0
        while temp[pos1].size != 0 and temp[pos1][pos] == a:
            temp[pos2][index] = a
            temp[pos1][pos] = ''
            if pos == 0:
                break
            index += 1
            pos -= 1
    else:
        index1 = 0
        index2 = 0
        for i in range(0,4):
            if temp[pos1][i] != '':
                index1 = i
            if temp[pos2][i] != '':
                index2 = i
        while index1 >= 0 and index2 <= 2 and temp[pos1][index1] == temp[pos2][index2]:
            temp[pos2][index2 + 1] = temp[pos1][index1]
            index2 += 1
            temp[pos1][index1] = ''
            index1 -= 1
    return State(temp)

def bfs(s:State)->np.array:
    q = Queue()
    q.put(s)
    mp = dict()
    mp[s] = 1
    while not q.empty():
        temp = copy(q.get())
        for i in range (0, temp.lst.shape[0]):
            for j in range (i+1, temp.lst.shape[0]):
                move1 = move(temp, i, j)
                if move1.lst.size != 0 and move1 not in mp:
                    q.put(move1)
                    move1.parent = temp
                    mp[move1] = 1
                    if move1.is_solved():
                        res = list([move1.lst.tolist()])
                        while move1.parent != None:
                            res.append(move1.parent.lst.tolist())
                            move1 = move1.parent
                        res.reverse()
                        return res
                move2 = move(temp, j, i)
                if move2.lst.size != 0 and move2 not in mp:
                    q.put(move2)
                    move2.parent = temp
                    mp[move2] = 1
                    if move2.is_solved():
                        res = list([move2.lst.tolist()])
                        while move2.parent != None:
                            res.append(move2.parent.lst.tolist())
                            move2 = move2.parent
                        res.reverse()
                        return res
    return []

def dfs(s:State) ->list:
    st = deque()
    st.append(s)
    mp = dict()
    mp[s] = 1
    while len(st) != 0:
        temp = copy(st.pop())
        for i in range (0, temp.lst.shape[0]):
            for j in range (i+1, temp.lst.shape[0]):
                move1 = move(temp, i, j)
                if move1.lst.size != 0 and move1 not in mp:
                    st.append(move1)
                    move1.parent = temp
                    mp[move1] = 1
                    if move1.is_solved():
                        res = list([move1.lst.tolist()])
                        while move1.parent != None:
                            res.append(move1.parent.lst.tolist())
                            move1 = move1.parent
                        res.reverse()
                        return res
                move2 = move(temp, j, i)
                if move2.lst.size != 0 and move2 not in mp:
                    st.append(move2)
                    move2.parent = temp
                    mp[move2] = 1
                    if move2.is_solved():
                        res = list([move2.lst.tolist()])
                        while move2.parent != None:
                            res.append(move2.parent.lst.tolist())
                            move2 = move2.parent
                        res.reverse()
                        return res
    return []

def readmap(filename) -> np.array:
    f = open(filename, 'r')
    line = f.read()
    temp = line.split("\n")
    lst = []
    for x in temp:
        lst.append(x.split())
    lst = [x + ['']*(4-len(x)) for x in lst]
    arr = np.array(lst)
    return arr

def f(s:State)->int:
    res = 0
    for x in s.lst:
        for i in range(0, len(x) - 1):
            if x[i] != '':
                if x[i] == x[i+1]:
                    res += 1
                else:
                    if x[i +1] != '':
                        res -= 1
    return res
    
def aStar(s: State)->list:
    q = CusQueue()
    cost = 0 # g(x)
    q.push(s, f(s))
    mp = dict()
    mp[s] = 1
    while not q.empty():
        temp = copy(q.pop())
        a = 0
        for i in range (0, temp.lst.shape[0]):
            for j in range (i+1, temp.lst.shape[0]):
                move1 = move(temp, i, j)
                if move1.lst.size != 0 and move1 not in mp:
                    q.push(move1, f(move1))
                    move1.parent = temp
                    mp[move1] = 1
                    if move1.is_solved():
                        res = list([move1.lst.tolist()])
                        while move1.parent != None:
                            res.append(move1.parent.lst.tolist())
                            move1 = move1.parent
                        res.reverse()
                        return res
                a += 0.1
                move2 = move(temp, j, i)
                if move2.lst.size != 0 and move2 not in mp:
                    q.push(move2, f(move2))
                    move2.parent = temp
                    mp[move2] = 1
                    if move2.is_solved():
                        res = [move2.lst]
                        while move2.parent != None:
                            res.append(move2.parent.lst)
                            move2= move2.parent
                        res.reverse()
                        return res
                a += 0.1
        cost += 1
    return []

def calctime(typ :str) ->list:
    filename = ""
    lst_time = []
    res = []
    if typ == 'aStar':
        for i in range(1, 11):
            filename = 'map/lv' + str(i) + '.txt'
            arr = readmap(filename)
            start = time.time()
            res = aStar(State(arr))
            lst_time.append(time.time() - start)
            print("done " + str(i))
    elif typ == 'dfs':
        for i in range(1, 11):
            filename = 'map\lv' + str(i) + '.txt'
            arr = readmap(filename)
            start = time.time()
            res = dfs(State(arr))
            lst_time.append(time.time() - start)
            print("done " + str(i))
    elif typ =='bfs':
        for i in range(1, 11):
            filename = 'map\lv' + str(i) + '.txt'
            arr = readmap(filename)
            start = time.time()
            res = bfs(State(arr))
            lst_time.append(time.time() - start)
            print("done " + str(i))
    return lst_time

def help(lst1: list, lst2: list):
    index = 0
    index2 = 0
    for i in range(0, len(lst1)):
        for j in range(0, len(lst1[i])):
            if lst1[i][j] == '' and lst2[i][j] != '':
                index = i
            elif lst1[i][j] != '' and lst2[i][j] == '':
                index2 = i
    return index2,index

def instruction(lst: list)->list:
    res = []
    for i in range(0, len(lst)-1):
        index, index2 = help(lst[i], lst[i + 1])
        res.append((index, index2))
    return res

def getInstuc():
    for i in range(1,11):
        filename = 'map/lv' + str(i) + '.txt'
        out = 'output/lv' + str(i) + '.txt'
        outf = open(out, 'w+')
        arr = readmap(filename)
        res = aStar(State(arr))
        instruct = instruction(res)
        for i in range(0, len(instruct)):
            outf.write("Step " + str(i + 1) + ":" + str(instruct[i][0] + 1) + "->" + str(instruct[i][1] + 1) + '\n')

getInstuc()



       