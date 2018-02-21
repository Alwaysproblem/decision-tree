#!usr/bin/python3
# this is a practice for decision tree in machine learning.
# written by Prophet Young at 18:44 23/12/2017.
# test environment:
# Python 3.6.3 (v3.6.3:2c5fed86e0, Oct  3 2017, 00:32:08) 
# [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin

from Tree import *
from math import log2
from copy import deepcopy

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
            # tmp.sort()
            AttrDic[self.attribute[idx]] = tmp

        tmp = list(set(self.col[-1]))
        tmp.sort(reverse = True)
        AttrDic[self.target] = tmp
        return AttrDic


class ID3(Tree):
    def __init__(self, file_name, value = None, leaf_len = 2):
        super(ID3, self).__init__(value, leaf_len)
        self.tdata = TRData(file_name)

    def Entropy(self, bool_example, total = None):
        """
        calculate the Entropy of bool example like [9+ , 5-].
        """
        if total == None :
            total = sum(bool_example)

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
        # Set_class = deepcopy(S_train)
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
        gain_list = [self.info_gain(S_train, attr) for attr in attr_list]
        max_gain = max(gain_list)
        max_idx = gain_list.index(max_gain)
        # print(gain_list)
        return attr_list[max_idx]


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
    print(t.select_attr(t.tdata.trdata, ['Outlook', 'Temperature', 'Humidity', 'Wind']))

if __name__ == '__main__':
    main()