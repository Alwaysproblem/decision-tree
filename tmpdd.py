from math import log2

def Entropy(bool_example):
    total = sum(bool_example)
    pure_list = [ i/total for i in bool_example]
    def log2_Entr(p):
        return -1 * p * log2(p)
    etp_list = list(map(log2_Entr, pure_list))

    return sum(etp_list)

def Gain(value_list):
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
    EnS = Entropy(S)
    gain = EnS
    for v in value_list:
        gain -= sum(v)/total * Entropy(v)

    return gain

def main():
    print(Gain([[6, 2], [3, 3], [9, 5]]))

if __name__ == '__main__':
    main()