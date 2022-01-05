import random


class Tree:
    
    _leaves_num = random.sample(range(1000), random.randint(10, 500))
    two_square = [2**i for i in range(10)]
    level_list = []
    objects = {}
    
    
    class _Node:
        def __init__(self, lvl: int, value: int):
            self._value = value
            self._level = lvl
                        
            self._left = None
            self._right = None
        
        def nodes(self, x, y):
            try:
                if x._value > y._value:
                    self._left = y
                    self._right = x
            except AttributeError:
                self._left = y
                self._right = x
                    
        def __repr__(self):
            return str(self._value)#'<Lvl: {}, Value: {}>'.format(self._level, self._value)
        
        def __int__(self):
            return self._value


    def __init__(self):
        
        self._lenght = len(self._leaves_num)
        
        for i in range(self.getLength() + 1):
            self.objects[str(i)] = []
        
        for i in range(10):
            for _ in range(2**i):
                self.level_list.append(i)
                
        for leaf in self._leaves_num:
            level = self.level_list[self._leaves_num.index(leaf)]
            self.objects[str(level)].append(self._Node(lvl=level, value=leaf))
            
        self.determinator()
        
        self.current_node = None
        self.cur_lvl = None
        self.cur_leaf = None
        
    def __len__(self):
        return self._lenght
            
    def __getitem__(self, index):
        try:
            return self.objects[str(index)]
        except KeyError:
            pass
        
    def __next__(self):
        if self.current_node == None:
            self.cur_leaf = 0
            self.cur_lvl = 0
            self.current_node = self.objects[str(self.cur_lvl)][self.cur_leaf]
            return self.current_node
        
        elif self.current_node != None:
            try:
                self.cur_leaf += 1
                self.current_node = self.objects[str(self.cur_lvl)][self.cur_leaf]
            except IndexError:
                try:
                    self.cur_leaf = 0
                    self.cur_lvl += 1
                    self.current_node = self.objects[str(self.cur_lvl)][self.cur_leaf]
                except KeyError:
                    return
                
            return self.current_node
        
    def indexCheak(self, index):
        if index == 0:
            self.current_node = None
            self.cur_lvl = None
            self.cur_leaf = None
        
    def find(self, value: int, index=0):
        self.indexCheak(index)
        node = next(self)
        int_node = int(node)
        if int_node == value:
            return 'In {} level'.format(node._level)
        elif index < len(self) - 1:
            return self.find(value, index + 1)
        else:
            return 'There is no such number'
            
        
    def getLength(self):
        list_len = len(self._leaves_num)
        for i in range(10):
            if list_len - 2**i < 0:
                return i
            
    def maxNode(self, nodes: list[_Node]):
        int_nodes = [int(i) for i in nodes]
        return max(int_nodes)
    
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
        self.indexCheak(index)
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
                           
tree = Tree()
tree.iterationPrint()
tree.recursionPrint()
print('\n')

def main():
    while True:
        try:
            num = input('Nuber:')
            if num == 'break':
                break
            print(tree.find(int(num)))
        except ValueError:
            print('Invalid, try again')
            
if __name__ == '__main__':
    main()
        
    
    