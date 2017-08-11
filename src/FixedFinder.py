#! /usr/bin/env python

'''
Actually finds optimal path unlike previous implementation
'''

from heapq import heappop, heappush
import math
import time

from Finder import PathFinder, cost_guess, EXPLORED


SQRT2 = math.sqrt(2) #for easy access

class FixedFinder(PathFinder):
    
    def findpath(self, start_xy, stop_xy, show=False):
        '''
        Finds optimal path using real A* algorithm
        :return: returns two lists: path list, explored list
        '''
        parents = {start_xy : "done"} #dictionary of elements to their parents
        raw_costs = {start_xy : 0} #dictionary of elements to their raw costs (excluding heuristic)
        frontier = [(cost_guess(start_xy, stop_xy), start_xy)] #list will be used as heap to get closest in priority queue (cost, index)
        start_time = time.time()
        loop_num = 0

        while True:   
            ### HAHA, seemingly infinite loop
            if len(frontier) <= 0:
                print("Warning: No path found in time %s" % (time.time() - start_time))
                return [], parents.keys()
            best = heappop(frontier)[1]
            
            if best == stop_xy:
                #it's done
                print("Info: Path from %s to %s found in %s s" % (start_xy, stop_xy, time.time() - start_time))
                return path_list(parents, stop_xy), list(parents.keys())
            
            best_cost = raw_costs[best] #should exist
            
            for neighbor in self.neighbors(best):
                #all direct neighbors
                if parents.get(neighbor) is None:
                    #It has no parent so it's like it never existed
                    parents[neighbor] = best
                    raw_cost = best_cost + 1 #add one to cost
                    raw_costs[neighbor] = raw_cost
                    heappush(frontier, (raw_cost + diagonal_cost_guess(neighbor, stop_xy), neighbor))

                    if show or self.save:
                        self.put_point(neighbor, color=230, update=False)

                        if show:
                            self.update_display()
                        if self.save:
                            self.save_map("%s.png" % loop_num)
                    
            for neighbor in self.diagonal_neighors(best):
                #all diagonal neighbors
                if parents.get(neighbor) is None:
                    #It has no parent so it's like it never existed
                    parents[neighbor] = best
                    raw_cost = best_cost + SQRT2 #add one to cost
                    raw_costs[neighbor] = raw_cost
                    heappush(frontier, (raw_cost + diagonal_cost_guess(neighbor, stop_xy), neighbor))

                    if show or self.save:
                        self.put_point(neighbor, color=230, update=False)

                        if show:
                            self.update_display()
                        if self.save:
                            self.save_map("%s.png" % loop_num)

            loop_num += 1

    def neighbors(self, loc):
        '''
        Finds all valid direct neighbors of loc (not diagonal)
        :param loc: integer 2-tuple
        :return: returns integer 2-tuples beside loc that are contained in image
        '''
        valid = []
        
        right = (loc[0]+1, loc[1])
        if self.valid_loc(right): valid.append(right)
        
        left = (loc[0]-1, loc[1])
        if self.valid_loc(left): valid.append(left)
        
        up = (loc[0], loc[1]+1)
        if self.valid_loc(up): valid.append(up)
        
        down = (loc[0], loc[1]-1)
        if self.valid_loc(down): valid.append(down)
        
        return valid
    
    def diagonal_neighors(self, loc):
        '''
        Finds all valid diagonal neighbors of loc
        :param loc: integer 2-tuple
        :return: returns integer 2-tuples beside loc that are contained in image
        '''
        valid = []
        
        ne = (loc[0]+1, loc[1]+1) #northeast
        if self.valid_loc(ne): valid.append(ne)
        
        nw = (loc[0]-1, loc[1]+1) #northwest
        if self.valid_loc(nw): valid.append(nw)
        
        se = (loc[0]+1, loc[1]-1) #southeast
        if self.valid_loc(se): valid.append(se)
        
        sw = (loc[0]-1, loc[1]-1) #southwest
        if self.valid_loc(sw): valid.append(sw)
        
        return valid
    
    def valid_loc(self, loc):
        '''
        Determines if the location is valid (i.e. within constraints of image) and UNEXPLORED
        :param loc: integer 2-tuple location
        :return: returns True if location can be used as index else false
        '''
        valid_x = 0 < loc[0] <= self.im.size[0]
        valid_y = 0 < loc[1] <= self.im.size[1]
        unexplored = self.im.getpixel(loc) == EXPLORED #in domain of map
        return valid_x and valid_y and unexplored
    
def path_list(parents, end_xy):
    '''
    Creates a list representing the ideal path based on the dictionary of parents
    :param parents: dictionary of integer 2-tuple to integer 2-tuple representing node -> parent
    :param end_xy: integer 2-tuple representing end node
    :return: returns path list starting from start node
    '''
    parent = parents[end_xy]
    path = [end_xy]
    while parent is not "done":
        new_node = parents[path[0]]
        path.insert(0, new_node)
        parent = parents[new_node]
    return path

def diagonal_cost_guess(point_xy, stop_xy):
    '''
    Distance cost guess for using diagonals
    :param point_xy: integer 2-tuple current point
    :param stop_xy: integer 2-tuple for end point
    :return: returns distance including diagonals multiplied by SQRT2 plus other linear distance
    '''
    dx = abs(point_xy[0] - stop_xy[0])
    dy = abs(point_xy[1] - stop_xy[1])
    return min(dx, dy) * SQRT2 + abs(dx - dy)

if __name__ == "__main__":
    FixedFinder()
