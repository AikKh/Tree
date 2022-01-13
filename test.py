from Tree import Tree

tree = Tree([0])
for i in range(2, 510, 2):
    tree.append(i)
print(tree)