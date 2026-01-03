import os
import sys
import time

sys.path.append(os.path.abspath("."))


def input():
    lst = list(open(sys.argv[1] + "/input", "r"))
    return [x for x in lst]


day = __import__(sys.argv[1] + ".solve")
start = time.time()
if sys.argv[2] == "p1":
    sol = day.solve.solve1(input())
else:
    sol = day.solve.solve2(input())

now = time.time()
print(f"{sol: >20} (took {now - start})")
