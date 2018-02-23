#!usr/bin/python3
# this is a practice for decision tree in machine learning.
# written by Prophet Young at 18:44 23/12/2017.
# test environment:
# Python 3.6.3 (v3.6.3:2c5fed86e0, Oct  3 2017, 00:32:08) 
# [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin

from Tree import Tree
from math import log2
# from copy import deepcopy
from queue import Queue as q

class TRData():
    def __init__(self, Datafile):
        self.attribute, self.target, self.trdata = self.getdata(Datafile)
        self.col = list(zip(*self.trdata))
        self.dic = self.dicgen()

    def getdata(self, Datafile):
        try:
            with open(Datafile, 'r+') as f:
                attribute = f.readline()
                target = f.readline()
                trdata = f.readlines()

        except FileNotFoundError :
            print("I can not find the input file, Sir.")
            return 'err', 'err', 'err'
        else:
            print("will do Sir!")
            return attribute.strip().split(), target.strip(), [d.strip().split() for d in trdata]

    def dicgen(self):
        AttrDic = {}
        for idx in range(len(self.attribute)):
            tmp = list(set(self.col[idx]))
            tmp.sort(reverse = True)
            AttrDic[self.attribute[idx]] = tmp

        tmp = list(set(self.col[-1]))
        tmp.sort(reverse = True)
        AttrDic[self.target] = tmp
        return AttrDic


class DTree(Tree):
    def __init__(self, value = None, leaf_len = 2):
        super(DTree, self).__init__(value, leaf_len)

    def find_in_tree(self):
        pass


class ID3(object):
    def __init__(self, file_name):
        self.tdata = TRData(file_name)

    def Entropy(self, bool_example, total = None):
        """
        calculate the Entropy of bool example like [9+ , 5-].
        """
        if total == None :
            total = sum(bool_example)
        if total == 0:
            return 0

        pure_list = [ i/total for i in bool_example]
        def log2_Entr(p):
            if p == 0:
                return 0
            return -1 * p * log2(p)
        etp_list = list(map(log2_Entr, pure_list))

        return sum(etp_list)

    def Gain(self, value_list):
        """
        the fomular for calculating the infomation gain.
        value list is like:
            if S <- [9+, 5-], Sweak <- [6+, 2-], Sstrong <- [3+, 3-]
            then [[6, 2], [3, 3], [9, 5]].
        """
        if value_list == None:
            return

        S = value_list.pop()
        total = sum(S)
        EnS = self.Entropy(S)
        gain = EnS
        for v in value_list:
            gain -= sum(v)/total * self.Entropy(v)

        return gain

    def Set_Stastistic(self, S_train, atrDic, target, cond_atr = None):
        """
        S_train means that the whole subset of training set that is changed by upper-layer attribute.
        atrDic is attribute dictionary,
        cond_atr means that the attribute value need to be classified.
        """
        bool_expl = list()
        for v in atrDic[target]:
            classify_list = [ t for t in S_train if t[-1] == v ]
            if cond_atr == None:
                count = len(classify_list)
            else:
                count = len([ t for t in classify_list if cond_atr in t])
            bool_expl.append(count)
        return bool_expl

    def info_gain(self, S_train, cond_atr):
        atrDic = self.tdata.dic
        target = self.tdata.target
        S = self.Set_Stastistic(S_train, atrDic, target)
        gain_list = list()
        for v in atrDic[cond_atr]:
            tmp = self.Set_Stastistic(S_train, atrDic, target, v)
            gain_list.append(tmp)

        gain_list.append(S)
        return self.Gain(gain_list)

    def select_attr(self, S_train, attr_list):
        # gain_list = [self.info_gain(S_train, attr) for attr in attr_list]
        gain_list = list()

        for attr in attr_list:
            ddebug = self.info_gain(S_train, attr)
            gain_list.append(ddebug)

        max_gain = max(gain_list)
        max_idx = gain_list.index(max_gain)
        # print(gain_list)
        return attr_list[max_idx]

    def _subtree_gen(self, root, attrdic, attr, same = False):
        addr_list = list()
        root.value = attr
        if same == True:
            root.add_subtree(root, DTree())
            root.add_subtree(root, DTree())
        else:
            for Value in attrdic[attr]:
                leaf = DTree(value = Value)
                leaf.add_subtree(leaf, DTree('None'))
                root.add_subtree(root, leaf)
                addr_list.append(leaf.leafs[0])
        return addr_list

    def subtree_gen(self, root, attr, same = False):
        addr_list = self._subtree_gen(root, self.tdata.dic, attr, same)
        return addr_list

    def _S_list_gen(self, S, attr, attrdic):
        S_list = list()
        for Value in attrdic[attr]:
            S_list.append([ t for t in S if Value in t])
        return S_list

    def S_list_gen(self, S, attr):
        S_list = self._S_list_gen(S, attr, self.tdata.dic)
        return S_list

    def S_all_same(self, S):
        S_stat = self.Set_Stastistic(S, self.tdata.dic, self.tdata.target)
        S_tmp = [ i for i in S_stat if i != 0]
        if S is None or len(S) == 0:
            return False, 'err'
        elif len(S_tmp) == 1:
            return True, S_stat.index(S_tmp[0])
        return False, 'err'

    def _ID3_Dtree(self, S_train, target_attr, Attr, AttrDic):
        attr_set = set(Attr)
        attr_name = self.select_attr(S_train, list(attr_set))
        # root = self.subtree_gen(AttrDic, Attr)
        root = DTree(value = 'None', leaf_len = len(AttrDic[attr_name]))
        que_node = q()
        que_S_train = q()

        que_node.put_nowait(root)
        que_S_train.put_nowait(S_train)

        while len(attr_set) != 0 and que_node.empty() is False:
            cur_tree = que_node.get_nowait()
            S = que_S_train.get_nowait()
            bool_same, same_value = self.S_all_same(S)

            if bool_same is True:
                self.subtree_gen(cur_tree, AttrDic[target_attr][same_value], True)
            else:
                attr_name = self.select_attr(S, list(attr_set))
                addr_list = self.subtree_gen(cur_tree, attr_name, False)
                S_list = self.S_list_gen(S, attr_name)

                for addr in addr_list:
                    que_node.put_nowait(addr)

                for S_v in S_list:
                    que_S_train.put_nowait(S_v)

            attr_set.difference_update({attr_name})
        return root

    def ID3_Tree(self):
        res = self._ID3_Dtree(self.tdata.trdata, self.tdata.target, self.tdata.attribute, self.tdata.dic)
        res.showTree()





def main():
    filename = input("the train file name, please:\n")
    # t = TRData(filename)
    t = ID3(filename)
    # print("the content is:")
    # print(t.tdata.attribute)
    # print(t.tdata.target)
    # print(t.tdata.trdata)
    # print(t.tdata.dic)
    # print(t.Set_Stastistic(t.tdata.trdata, t.tdata.dic, t.tdata.target, 'Strong'))
    # print(t.info_gain(t.tdata.trdata, 'Temperature'))
    # print(t.select_attr(t.tdata.trdata, ['Outlook', 'Temperature', 'Humidity', 'Wind']))
    t.ID3_Tree()
    # S = [['Rain', 'Mild', 'High', 'Weak', 'Yes'], ['Rain', 'Cool', 'Normal', 'Weak', 'Yes'], ['Rain', 'Cool', 'Normal', 'Strong', 'No'], ['Rain', 'Mild', 'Normal', 'Weak', 'Yes'], ['Rain', 'Mild', 'High', 'Strong', 'No']]
    # print(t.info_gain(S,'Wind'))
if __name__ == '__main__':
    main()