# iterative Loop
import turtle
import time

myturtle = turtle.Turtle()
myturtle.setpos(0, 0)

#start from 10 to 95
line_range = 10

def loopFunction():
    global line_range
    for i in range(9):
        for k in range(2):
            myturtle.forward(line_range)
            myturtle.right(90)
        line_range += 5.5

loopFunction()
time.sleep(1)