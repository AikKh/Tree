from Tree import Tree

tree = Tree([0])

for i in range(4, 51, 2):
    tree.append(i)
print(tree)

for i in range(12, 41, 2):
    tree.remove(i)
print(tree)