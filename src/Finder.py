#! /usr/bin/env python

'''
Loads map image file then uses A* to find shortest path
'''

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

import math
from heapq import *
import threading
import sys


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
        self.threads = []

        self.im = Image.open("maps/map.png").convert("I")
        self.display_im = self.im.copy()
        self.drawer = ImageDraw.Draw(self.display_im)

        self.display = plt.imshow(self.display_im)
        plt.title("Path Finding A* Algorithm In a Map\n(Click 2 Points and Wait)")
        self.display.figure.canvas.mpl_connect('button_press_event', self.onclick)
        plt.show()

    def update_display(self):
        self.display.set_data(self.display_im)
        plt.draw()

    def put_point(self, xy, color=0, width=4):
        '''
        Changes the pixel at a point
        '''
        #print("point %s" % (xy,)) #TODO remove
        r = int(width/2)
        x,y = xy
        self.drawer.ellipse((x-r, y-r, x+r, y+r), fill=color)
        self.update_display()

    def put_points(self, xy_points, color=0, width=4):
        r = int(width/2)
        for x,y in xy_points:
            self.drawer.ellipse((x-r, y-r, x+r, y+r), fill=color)
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

                thread = threading.Thread(target=self.drawpath, args=(("early_show" in sys.argv),))
                thread.setDaemon(True)
                thread.start()
                self.threads.append(thread)

                self.start_xy = None
                self.stop_xy = None

    def drawpath(self, early_show=False):
        '''
        Calculates path based on and draws it on the map
        '''
        if self.start_xy is None or self.stop_xy is None:
            #if either is not ready, just stop
            return
        #TODO call finding algorithm to do the stuff with the data
        path, explored = self.findpath(self.start_xy, self.stop_xy, early_show)

        #display explored locations in grey and path in black
        if not early_show:
            self.put_points(explored, color=230)
        self.put_points(path)
        self.update_display()

    def findpath(self, start_xy, stop_xy, show=False):
        '''
        Finds optimal path from start_xy to stop_xy
        '''
        frontier = [] #TODO may need to be heapified
        explored = set()
        start = PathNode(start_xy, stop_xy)
        neighbors = start.neighbors(self.im.size)
        for neighbor_path in neighbors:
            if neighbor_path is not None:
                heappush(frontier, neighbor_path)

        path = None
        while path is None:
            #loop until the ideal path is found -> path will become the Path object with shortest route
            best = heappop(frontier)

            if best.frontier() == stop_xy:
                path = best
            else:
                for neighbor_path in best.neighbors(self.im.size):
                    if neighbor_path is not None and self.im.getpixel(neighbor_path.frontier()) == EXPLORED and neighbor_path.frontier() not in map(lambda node: node.frontier(), frontier):
                        explored.add(neighbor_path.frontier())
                        heappush(frontier, neighbor_path)
                        if show:
                            self.put_point(neighbor_path.frontier(), color=230)

        return path_list(path), list(set(explored))

def path_list(path):
    '''
    Converts Path object to list of tuple xy points
    '''
    node = path
    nodes = []
    while node is not None:
        nodes.append(node.frontier())
        node = node.get_prev()
    return nodes

def cost_guess(point_xy, stop_xy):
    '''
    Makes a guess about how far the points are from each other (possibly using Manhattan distance)
    '''
    return abs(point_xy[0] - stop_xy[0]) + abs(point_xy[1] - stop_xy[1])

def cmp(a, b):
    '''
    Compares two objects (resurrected from Python 2)
    '''
    return (a>b)-(a<b)

class PathNode():
    def __init__(self, location, endpoint, prev=None):
        self.prev = prev
        self.xy = location
        self.endpoint = endpoint
        self.length = (1 + prev.prev_dist()) if prev is not None else 1

    def __cmp__(self, other):
        return cmp(self.cost(), other.cost())

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def get_prev(self):
        return self.prev

    def prev_dist(self):
        return self.length

    def future_guess(self):
        return cost_guess(self.xy, self.endpoint)

    def cost(self):
        return self.prev_dist() + self.future_guess()

    def frontier(self):
        return self.xy

    def self_test(self):
        cmp = self.__cmp__(self)
        prev = self.prev_dist()
        future = self.future_guess()
        cost = self.cost()
        last = self.frontier()
        return "%s %s %s %s %s" % (cmp, prev, future, cost, last)

    def neighbors(self, shape):
        '''
        Gets a Path for all valid neighbors
        '''
        len_x, len_y = shape
        x, y = self.frontier()
        ret = [] #list of index xy tuples beside the xy input

        up_x = PathNode((x+1, y), self.endpoint, prev=self)
        if x+1 < len_x: ret.append(up_x)
        if x-1 >= 0: ret.append(PathNode((x-1, y), self.endpoint, prev=self))
        if x+1 < len_x: ret.append(PathNode((x, y+1), self.endpoint, prev=self))
        if x-1 >= 0: ret.append(PathNode((x, y-1), self.endpoint, prev=self))

        return ret

class Path(list):
    def __init__(self, start):
        self.extend(start)

    def __cmp__(self, other):
        return cmp(len(self), len(other))

    def prev_dist(self):
        return len(self)

    def future_guess(self, endpoint):
        return cost_guess(self[-1], endpoint)

    def cost(self, endpoint):
        return self.prev_dist() + self.future_guess(endpoint)

    def frontier(self):
        return self[-1]

    def self_test(self, endpoint):
        cmp = self.__cmp__(self)
        prev = self.prev_dist()
        future = self.future_guess(endpoint)
        cost = self.cost(endpoint)
        last = self.frontier()
        return "%s %s %s %s %s" % (cmp, prev, future, cost, last)

    def neighbors(self, shape):
        '''
        Gets a Path for all valid neighbors
        '''
        len_x, len_y = shape
        x, y = self.frontier()
        ret = [] #list of index xy tuples beside the xy input

        if x+1 < len_x: ret.append(Path(self + [(x+1, y)]))
        if x-1 >= 0: ret.append(Path(self + [(x-1, y)]))
        if x+1 < len_x: ret.append(Path(self + [(x, y+1)]))
        if x-1 >= 0: ret.append(Path(self + [(x, y-1)]))

        return ret

if __name__ == "__main__":
    PathFinder()
