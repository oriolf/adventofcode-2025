import os
import sys

sys.path.append(os.path.abspath("."))


day = __import__(sys.argv[1] + ".solve")
if sys.argv[2] == "p1":
    day.solve.solve1()
else:
    day.solve.solve2()
