import turtle
import time

my_turtle = turtle.Turtle()

my_turtle.penup()
my_turtle.backward(200)
my_turtle.left(90)
my_turtle.backward(200)
my_turtle.right(90)
my_turtle.pendown()

#Draws the square base of the house
def draw_square():
    for i in range(4):
        my_turtle.forward(300)
        my_turtle.left(90)

#Draws the door in the square landing on the top left hand corner for the triangle roof
def draw_door():
    my_turtle.forward(90)
    my_turtle.left(90)
    for i in range(3):
        if i == 1:
            my_turtle.forward(50)
            my_turtle.right(90)
        my_turtle.forward(90)
        my_turtle.right(90)
        if i == 2:
            my_turtle.pendown()
            my_turtle.left(90)
            my_turtle.forward(50)
            my_turtle.right(90)
            my_turtle.forward(300)
            my_turtle.pendown()

#Picks up from the doors markers last position to draw the roof
def draw_triangle():
    for i in range(2):
        my_turtle.right(60)
        my_turtle.forward(176)

def draw_chimney():
    my_turtle.backward(30)
    my_turtle.left(120)

  #Creates the Chimney
    my_turtle.forward(100)
    my_turtle.left(90)
    my_turtle.forward(50)
    my_turtle.left(90)
    my_turtle.forward(70)









draw_square()
draw_door()
draw_triangle()
draw_chimney()
time.sleep(3)