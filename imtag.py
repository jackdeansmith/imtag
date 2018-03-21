#!/usr/bin/env python3
from sys import argv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg

# Simple function for error printing
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Check to make sure the user supplied the right number of args to the tagging
# script.
if(len(argv) != 3):
    #TODO make a nice error message here
    exit(1)

# the first positional arg is the name of the file we are trying to tag
image_filename = argv[1]

# second positional arg is the name of the output tag file
tag_filename = argv[2]

# Try to open the image, ensure failure if we can't
try:
    img=mpimg.imread(image_filename)
except(FileNotFoundError):
    #TODO nice error message here
    exit(1)

# List of the x and y positions selected, ordered in the order of their
# selection
x_points = [];
y_points = [];

# Draws the image with the points on top, marked by a small x
def draw():
    plt.clf()
    plt.imshow(img)
    plt.scatter(x_points,y_points, marker='x'); #inform matplotlib of the new data
    plt.draw() #redraw

# Handler for clicks
def onclick(event):
    if event.button == 1:
         x_points.append(event.xdata)
         y_points.append(event.ydata)
    draw()

# Keypress handler, space closes the plot window, escape clears the points
def onkey(event):
    if(event.key == ' '):
        plt.close()
    elif(event.key == 'escape'):
        print("Escaped")
        x_points = []
        y_points = []
        draw()

# Create the figure and set up the handlers
fig,ax=plt.subplots()
draw()
fig.canvas.mpl_connect('button_press_event',onclick)
fig.canvas.mpl_connect('key_press_event', onkey)
plt.show()

# Once the matplotlib window closes, write the output as a CSV
with open(tag_filename, 'w') as tagfile:
    tagfile.write("X, Y\n")
    for (x, y) in zip(x_points, y_points):
        tagfile.write("{}, {}\n".format(x, y))
