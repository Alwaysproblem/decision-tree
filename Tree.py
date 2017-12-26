#!usr/bin/python3
# this is a tree module.
# written by Prophet Young at 18:44 23/12/2017.
# test environment:
# Python 3.6.3 (v3.6.3:2c5fed86e0, Oct  3 2017, 00:32:08) 
# [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin

from queue import Queue

class Tree:
    def __init__(self, value = None, leaf_len = 2):
        self.value = value
        self.domain = {}
        self.leafs = []
        if self.value is None:
            self.leafs = None
        else:
            self.leafs = [ Tree(None, leaf_len = leaf_len) for _ in range(leaf_len)]

    def is_full(self, Parent):
        """check if the child of Parent is full."""
        return len(\
                [leaf for leaf in Parent.leafs if leaf.value is not None]\
                ) == len(Parent.leafs)

    def _leaf_join(self, NewTree, index):
        """
        assign a new sub-tree into the parent tree.
        """
        if index > len(self.leafs) - 1:
            return 'error'

        if isinstance(NewTree, Tree) is True:
            self.leafs[index] = NewTree
        else:
            self.leafs[index] = Tree(NewTree)

    def add_subtree(self, Parent, Subtree):
        """add the subtree into the empty space of Parent leaf list."""
        if Parent is None or Subtree is None:
            return 'error'
        if Parent.value is None or Subtree.value is None:
            return 'error'
        elif self.is_full(Parent) is True:
            return 'full'
        else:
            for index in range(len(Parent.leafs)):
                if Parent.leafs[index].value is None:
                    Parent._leaf_join(Subtree, index)
                    return 'True'
            return "False"

    def delete_leaf(self, Parent, index):
        if Parent is None:
            return 'error'
        elif Parent.value is None :
            return 'error'
        elif Parent.leafs[index].value is None:
            pass
        else:
            Parent.leafs[index] = Tree()


    def size(self):
        '''Returns the number of nodes. using the BFS traversal'''
        if self.value is None:
            return 0
        else:
            Size = 0
            q = Queue()
            cur_tree = self
            q.put_nowait(cur_tree)
            while q.empty() is not True:
                cur_tree = q.get_nowait()
                if cur_tree.leafs is not None:
                    for leaf in cur_tree.leafs:
                        if leaf.value is not None:
                            q.put_nowait(leaf)
                else:
                    pass
                Size += 1
        return Size

    def height(self):
        """ return the hight of tree. using the BFS traversal"""
        if self.value is None:
            return 0
        else:
            q = Queue()
            cur_tree = self
            all_leaves = 1
            next_level_count = 0
            cur_level_count = 0
            level_list = list()
            q.put_nowait(cur_tree)
            while q.empty() is not True:
                if cur_level_count >= all_leaves - 1:
                    cur_tree = q.get_nowait()
                    for leaf in cur_tree.leafs:
                        if leaf.value is not None:
                            next_level_count += 1
                            q.put_nowait(leaf)

                    level_list.append(all_leaves)
                    all_leaves = next_level_count
                    cur_level_count = 0
                    next_level_count = 0
                else:
                    cur_level_count += 1
                    cur_tree = q.get_nowait()
                    for leaf in cur_tree.leafs:
                        if leaf.value is not None:
                            next_level_count += 1
                            q.put_nowait(leaf)
        # print(level_list)
        return len(level_list) - 1


    def occur_in_tree(self, value):
        """
        return the truth if the value is in the tree, 
        and time complexity is O(number of node) 
        using the BFS traversal.
        """
        if self.value is None:
            return False
        else:
            q = Queue()
            cur_tree = self
            q.put_nowait(cur_tree)
            while q.empty() is not True:
                cur_tree = q.get_nowait()
                if cur_tree.value == value:
                    return True
                for leaf in cur_tree.leafs:
                    if leaf.value is not None:
                        q.put_nowait(leaf)
                else:
                    pass
            return False

    def showTree(self, mode = 'hide'):
        """
        show the tree. 
        mode = 'hide' is showing all of node which value is not None.
        default: mode = 'hide'
        """
        if self.value is None:
            return
        else:
            Stack = list()
            level = 0
            Stack.append(('', self, level))

            while len(Stack) != 0:
                symbol, cur_tree, level = Stack.pop()

                if level == 0:
                    print(cur_tree.value)
                    print('│')
                else:
                    print(symbol + str(cur_tree.value))

                if symbol == '':
                    base_str = symbol
                elif "└────" in symbol:
                    base_str = symbol[:-len("└────")] + '     '
                else:
                    base_str = symbol[:-len("├────")] + '|    '

                level += 1
                if mode == 'hide':
                    leafs = [ f for f in cur_tree.leafs if f.value is not None]
                    leafs.reverse()
                    for leaf_index in range(len(leafs)):
                        if leaf_index == 0:
                            Stack.append((base_str + "└────", leafs[leaf_index], level))
                        else:
                            Stack.append((base_str + "├────", leafs[leaf_index], level))
                else:
                    pass


if __name__ == '__main__':
    t = Tree(1, leaf_len = 3)
    for i in range(3):
        t._leaf_join(Tree(i+2, leaf_len = 3),i)

    t.add_subtree(t.leafs[2], Tree(42))
    t.add_subtree(t.leafs[2], Tree(43))
    t.leafs[1]._leaf_join(Tree(6, leaf_len = 3), 2)
    t.leafs[1]._leaf_join(Tree(11, leaf_len = 3), 0)
    t.leafs[0]._leaf_join(Tree(7, leaf_len = 3), 0)
    t.leafs[1].leafs[2]._leaf_join(Tree(8, leaf_len = 3), 2)
    t.leafs[0].leafs[0]._leaf_join(Tree(10), 0)
    # print(t.size())
    t.add_subtree(t.leafs[1].leafs[2], Tree(9))
    t.add_subtree(t.leafs[1].leafs[2], Tree(22))

    t.add_subtree(t.leafs[1].leafs[2].leafs[0], Tree(91))
    t.add_subtree(t.leafs[1].leafs[2].leafs[0], Tree(92))
    # print(t.size())
    # t.delete_leaf(t.leafs[1].leafs[2], 0)
    # print(t.size())

    t.showTree()
    # t.leafs[1].leafs[2].leafs[2].leafs[0].value == 9
    # print(t.occur_in_tree(9))
    # print(t.height())
    # print(t.size())
    # import doctest
    # doctest.testmod()