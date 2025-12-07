import sys


def input():
    lst = list(open(sys.argv[1] + "/" + sys.argv[3], "r"))
    return [x.strip() for x in lst]
