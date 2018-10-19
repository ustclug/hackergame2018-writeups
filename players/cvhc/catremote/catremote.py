import sys
from turtle import *

seq_file = sys.argv[1]
with open(seq_file) as fin:
    log = fin.read().strip()

color('red', 'yellow')
begin_fill()
for c in log:
    if c == 'U':
        setheading(90)
    elif c == 'D':
        setheading(270)
    elif c == 'L':
        setheading(180)
    elif c == 'R':
        setheading(0)
    forward(1)
end_fill()
done()
