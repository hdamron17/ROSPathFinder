#! /usr/bin/env python

'''
Loads map image file then uses A* to find shortest path
'''

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

import math
import queue


EXPLORED = 254 #explored location
UNEXPLORED = 205 #unexplored location
BOUNDARY = 0 #boundary location

class PathFinder():
    def __init__(self):
        '''
        Creates PathFinder object, loads and displays map
        '''
        self.start_xy = None #point to start on
        self.stop_xy = None #point to end on

        self.im = Image.open("maps/map.png").convert("I")
        self.display_im = self.im.copy()
        self.drawer = ImageDraw.Draw(self.display_im)

        self.display = plt.imshow(self.display_im)
        self.display.figure.canvas.mpl_connect('button_press_event', self.onclick)
        plt.show()

    def update_display(self):
        self.display.set_data(self.display_im)
        plt.draw()

    def put_point(self, xy, color=0):
        '''
        Changes the pixel at a point
        '''
        #print("point %s" % (xy,)) #TODO remove
        self.drawer.point(xy, color)
        self.update_display()

    def put_line(self, start_xy, stop_xy, color=0):
        '''
        Draws a straight line on the map from one point to another
        '''
        #print("line from %s to %s" % (start_xy, stop_xy)) #TODO remove
        self.drawer.line([start_xy, stop_xy], width=10)
        self.update_display()

    def onclick(self, event):
        '''
        When the user clicks a location on the map, it sets that point as endpoint
        '''
        x = int(round(event.xdata))
        y = int(round(event.ydata))
        if x != None and y != None and self.im.getpixel((x,y)) == EXPLORED:
            #print("Clicked (%s,%s) -> %s, start: %s, stop: %s" % (x,y, self.im.getpixel((x,y)), self.start_xy, self.stop_xy)) #TODO remove
            if self.start_xy == None:
                self.start_xy = (x, y)
                self.put_point(self.start_xy)

            elif self.stop_xy == None:
                self.stop_xy = (x, y)
                #TODO call finding algorithm to do the stuff with the data
                print(self.findpath(self.start_xy, self.stop_xy))
                self.put_line(self.start_xy, self.stop_xy) #TODO remove
                # print("Resetting") #TODO remove

                self.start_xy = None
                self.stop_xy = None

    def cost_guess(self, point_xy, stop_xy):
        '''
        Makes a guess about how far the points are from each other (possibly using Manhattan distance)
        '''
        return abs(point_xy[0] - stop_xy[0]) + abs(point_xy[1] - stop_xy[1])

    def findpath(self, start_xy, stop_xy):
        '''
        Finds optimal path from start_xy to stop_xy
        '''
        frontier = queue.PriorityQueue()

    def Path(list):
        def __init__(self, start):
            super.__init__()
            self.append(start)

        def __cmp__(self, other):
            return cmp(len(self), len(other))

        def prev_dist(self):
            return len(self)

        def future_guess(self):
            return self.cost_guess(self[-1])

if __name__ == "__main__":
    PathFinder()
