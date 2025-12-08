import os
import sys

sys.path.append(os.path.abspath("."))


def input():
    lst = list(open(sys.argv[1] + "/input", "r"))
    return [x for x in lst]


day = __import__(sys.argv[1] + ".solve")
if sys.argv[2] == "p1":
    print(day.solve.solve1(input()))
else:
    print(day.solve.solve2(input()))
