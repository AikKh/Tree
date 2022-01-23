import random
from typing import overload


class Tree:
    
    _leaves_num = None#list(random.sample(range(1000), random.randint(10, 50)))
    
    two_square = [2**i for i in range(10)]
    level_list = []
    objects = {}
    index_list = {0:[0]}
    
    
    class _Node:
        def __init__(self, lvl: int, value: int):
            self._value = value
            self._level = lvl
                        
            self._left = None
            self._right = None
        
        def nodes(self, x, y):
            self._left = x
            self._right = y
                    
        def __repr__(self):
            return str(self._value)
        
        def __int__(self):
            return self._value


    def __init__(self, leaves: list):
        
        self._leaves_num = list(leaves)
        self._leaves_num.sort()
        
        self._lenght = len(self._leaves_num)
        
        for i in range(1, 20):
            self.index_list[i] = list(range(2**i - 1, 2**(i+1) - 1))
        
        for i in range(self.getLength() + 1):
            self.objects[str(i)] = []
        
        for i in range(10):
            for _ in range(2**i):
                self.level_list.append(i)
                
        for leaf in self._leaves_num:
            level = self.level_list[self._leaves_num.index(leaf)]
            self.objects[str(level)].append(self._Node(lvl=level, value=leaf))
            
        self.determinator()
        
        self._root = self[0]
        self._end = self._leaves_num[-1]
        self.current_index = -1
        
    def __len__(self):
        return self._lenght
            
    def __getitem__(self, index):
        if index >= self._lenght:
            raise StopIteration('out of tree')
        
        ind_list = dict(self.index_list)
        self._root = self.objects['0'][0]
        
        if index == 0:
            return self._root
        
        for lvl in self.index_list:
            for leaf in self.index_list[lvl]:
                if leaf == index:
                    return self.getDir(index, lvl, ind_list)
    
    def getDir(self, index: int, lvl: int, ind_list: dict):
        if lvl > 0:
            curren_lvl = ind_list[lvl]
            middle = len(curren_lvl)//2
            left = curren_lvl[:middle]
            right = curren_lvl[middle:]
            if index in left:
                self._root = self._root._left
                ind_list[lvl-1] = left
            elif index in right:
                self._root = self._root._right
                ind_list[lvl-1] = right
            return self.getDir(index, lvl-1, ind_list)
        else:
            return self._root
            
        
    def __next__(self):
        self.current_index += 1
        try:
            res = self[self.current_index]
        except StopIteration:
            return
        else:
            return res
        
    def __repr__(self) -> str:
        self.recursionPrint()
        return str()
    
    def index(self, value: int):
        index = 0
        for lvl in self.objects:
            for leaf in self.objects[lvl]:
                if int(leaf) == value:
                    return index
                index += 1
        
    def append(self, value):
        #print('You added {}'.format(value))
        self.indexCheck(0)
        
        try:
            value = int(value)
            if value < 0:
                print('Only positive values')
                return
            
            check = self.find(value)
            if check[1]:
                print('Already in level {}'.format(check[0][-1]))
                return
        except ValueError as error:
            print('ValueError:', error)
        else:
            self.indexCheck(0)
            if value > self._end:
                self._end = value
            self.findPlace(value)
            
    def remove(self, value):
        try:
            value = int(value)
            if value < 0:
                print('Only positive values')
                return
            
            check = self.find(value)
            if not check[1]:
                print(check[0])
                return
        except ValueError as error:
            print('ValueError:', error)
        else:
            self.indexCheck(0)
            self._lenght -= 1
            self.removeNode(value)
            
        
        
    def findPlace(self, value: int):
            node = next(self)
            if node:
                if node._value > value:
                    old = int(node._value)
                    node._value = value
                    value = old
                    
                return self.findPlace(value)    
            else:
                self._lenght += 1
                self.indexCheck(0)
                self.addNode()
            
        
    def addNode(self):
        node = next(self)
        
        if node._left == None:
            node._left = self._Node(node._level + 1, self._end)
            return
        
        elif node._right == None:
            node._right = self._Node(node._level + 1, self._end)
            return 
        
        return self.addNode()
    
    def removeNode(self, value):
        node = next(self)
        if node:
            if node._value == value:
                node._value = self[self.current_index + 1]._value
                self[self.current_index + 1]._value = None
            elif node._value == None:
                try:
                    node._value = int(self[self.current_index + 1]._value)
                    self[self.current_index + 1]._value = None
                except StopIteration:
                    node._value = self._end
                    return
        else:
            return
        return self.removeNode(value)
            
    def indexCheck(self, index):
        if index == 0:
            self.current_index = -1
        
        
    def find(self, value: int, index=0):
        self.indexCheck(index)
        node = next(self)
        int_node = int(node._value)
        if int_node == value:
            return ('The {} in level N-{}'.format(value, node._level), True)
        elif index < len(self) - 1:
            return self.find(value, index + 1)
        else:
            return('There is no {}'.format(value), False)
        
    def replace(self, the_value, to_value):
        try:
            the_value = int(the_value)
            to_value = int(to_value)
            if the_value < 0 or to_value < 0:
                print('Only positive values')
                return
            
            check = self.find(the_value)
            if not check[1]:
                print(check[0])
                return
        except ValueError as error:
            print('ValueError:', error)
        else:
            self.indexCheck(0)
            self.replaceValue(the_value, to_value)
        
    def replaceValue(self, the_value, to_value):
        node = next(self)
        try:
            if node._value == the_value:
                node._value = to_value
            else:
                return self.replaceValue(the_value, to_value)
        except StopIteration:
            print('There is no {}'.format(the_value))
            return
        
    def getLength(self):
        list_len = len(self._leaves_num)
        for i in range(10):
            if list_len - 2**i < 0:
                return i
            
    def getNode(self, lvl: str, place, dir=0):
        plusLvl = int(lvl) + 1
        
        for node in self.objects[str(plusLvl)]:
            if self.objects[str(node._level)].index(node) + dir == place:
                return node
            
    def determinator(self):
        for i in self.objects:
            for node in self.objects[i]:
                place = (self._leaves_num.index(node._value) - 2**node._level + 1)*2
                node.nodes(self.getNode(i, place), self.getNode(i, place+1))
                
            
    def recursionPrint(self, index=0, space_count=50):
        self.indexCheck(index)
        node = next(self)
        if node:
            for n in self.two_square:
                if index + 1 == n:
                    print('\n')
                    print(space_count * ' ', end=' ')
                    space_count -= 2 * n
            print('{}'.format(node._value), end=' ')
            if index < len(self) - 1:
                self.recursionPrint(index + 1, space_count)
            else:
                print('\n')
                



