import random


class Tree:
    
    _leaves_num = list(random.sample(range(1000), random.randint(10, 50)))
    _leaves_num.sort()
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
            return str(self._value)#'<Lvl: {}, Value: {}>'.format(self._level, self._value)
        
        def __int__(self):
            return self._value


    def __init__(self):
        
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
        
        self._root = self.objects['0'][0]
        self._end = self._leaves_num[-1]
        print(self._end)
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
    
    def index(self, value: int):
        index = 0
        for lvl in self.objects:
            for leaf in self.objects[lvl]:
                if int(leaf) == value:
                    return index
                index += 1
        
    def append(self, value):
        print('You added {}'.format(value))
        self.indexCheck(0)
        try:
            value = int(value)
            if value < 0:
                print('Only positive values')
                return
            
            check = self.find(value)
            if check[4] == 'r':
                print('Already in level {}'.format(check[-1]))
                return
        except ValueError as error:
            print('ValueError:', error)
        else:
            self.indexCheck(0)
            self.findPlace(value)
        
        
    def findPlace(self, value: int):
        try:
            node = next(self)
            if node:
                if node._value > value:
                    old = int(node._value)
                    node._value = value
                    value = old

            else:
                self._lenght += 1
                self.indexCheck(0)
                while True:
                    node = next(self)
                    
                    if node._left == None:
                        node = next(self)
                        print('None is', node, node._left, node._right)
                        print('==============', node._left)
                        node._left = Tree._Node(node._lvl + 1, self._end._value)
                        print('None is', node, node._left, node._right)
                        return
                    
                    elif node._right == None:
                        node = next(self)
                        print('None is', node, node._left, node._right)
                        print('==============', node._right)
                        node._right = Tree._Node(node._lvl + 1, self._end._value)
                        print('None is', node, node._left, node._right)
                        return
                
        except AttributeError or StopIteration:
            return None
        else:
            return self.findPlace(value)
        
        
    def indexCheck(self, index):
        if index == 0:
            self.current_index = -1
        
        
    def find(self, value: int, index=0):
        self.indexCheck(index)
        node = next(self)
        int_node = int(node._value)
        if int_node == value:
            return 'The {} in level N-{}'.format(value, node._level)
        elif index < len(self) - 1:
            return self.find(value, index + 1)
        else:
            return 'There is no {}'.format(value)
            
        
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
                
    def printLeaves(self):
        print('----------------------------------')
        for i in self.objects:
            for node in self.objects[i]: 
                #if node._right is not None or node._right is not None:
                    print('<<{}>>'.format(node._value), node._left, node._right)
                    
    def iterationPrint(self):
        space_count = 50
        
        for l in self.objects:
            print(space_count*' ')
            for obj in self.objects[l]:
                if self.objects[l].index(obj) == 0:
                    print(space_count*' ', obj, end='  ')
                    continue
                print(obj, end='  ')
            print('\n')
            space_count -= 3*(int(l)+1)
            
            
    def recursionPrint(self, index=0, space_count=50):
        self.indexCheck(index)
        node = next(self)
        if node != None:
            for n in self.two_square:
                if index + 1 == n:
                    print('\n')
                    print(space_count * ' ', end=' ')
                    space_count -= 2 * n
            print('{}'.format(node._value), end=' ')
            if index < len(self) - 1:
                self.recursionPrint(index + 1, space_count)
                
def test1():
    while True:
        try:
            num = input('Nuber:')
            if num == 'break':
                break
            print(tree.find(int(num)))
        except ValueError:
            print('Invalid, try again')
            
def test2():
    i = 0
    while True:
        try:
            print(tree[i])
            i += 1
        except StopIteration:
            print('Stop', 'Len:', i) 
            break
        
def test3():
    tree.indexCheck(0)
    while True:
        try:
            print(next(tree))
        except StopIteration:
            print('Stop')
            break
        
        
tree = Tree()
#tree.printLeaves()
#tree.iterationPrint()
tree.recursionPrint()
print('\n')

# tree.indexCheck(0)
x = 111
print(tree.find(x))
test2()
tree.append(x)
test2()
print('\n')

tree.recursionPrint()
print('\n')
print(tree.find(x))

