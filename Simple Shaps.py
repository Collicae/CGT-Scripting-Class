from tkinter import *
import turtle
import time


my_turtle = turtle.Turtle()
my_turtle.setpos(0, 0)

def draw_triangle():
    for i in range(3):
        my_turtle.forward(100)
        my_turtle.left(120)

def draw_octo():
    for i in range(8):
        my_turtle.forward(45)
        my_turtle.left(45)

def draw_hexa():
    for i in range(6):
        my_turtle.forward(45)
        my_turtle.left(60)


draw_triangle()

my_turtle.penup()
my_turtle.forward(150)  # move right
my_turtle.pendown()

draw_octo()

my_turtle.penup()
my_turtle.forward(150)  # move right
my_turtle.pendown()

draw_hexa()


time.sleep(1)
