import visualizer as vis 
import random as rdm
import pygame
import time
import math

width = 1024
height = 576

def dist(start, end):
    x_comp = end[0] - start[0]
    y_comp = end[1] - start[1]

    return math.sqrt(math.pow(x_comp, 2) + math.pow(y_comp, 2))

class Node:
    def __init__(self, x, y):
        self.pos = x, y
        self.color = rdm.randint(0, 255), rdm.randint(0, 255), rdm.randint(0, 255)
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)

class RRT:
    def __init__(self, root, step_size):
        self.root = root
        self.step_size = step_size
        self.obstacles = []

    def find_closest_node(self, node, pnt):
        for child in node.children:
            dist_val = dist(child.pos, pnt)
            if dist_val < self.min_val:
                self.min_val = dist_val
                self.min_node = child
            self.find_closest_node(child, pnt)

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def find_closest(self, pnt):
        self.min_val = dist(self.root.pos, pnt)
        self.min_node = self.root
        
        self.find_closest_node(self.root, pnt)

    def step(self):
        x = rdm.randint(0, width)
        y = rdm.randint(0, height)

        self.find_closest((x,y))
        parent_node = self.min_node

        y_diff = y - parent_node.pos[1]
        x_diff = x - parent_node.pos[0]
        
        if x_diff == 0:
            if y_diff > 0:
                angle = math.pi / 2
            else:
                angle = 3 * math.pi / 2
        elif y_diff == 0:
            if x_diff > 0:
                angle = 0
            else:
                angle = math.pi
        else:
            angle = math.atan(y_diff / x_diff)
       
        mag = self.step_size
        if self.min_val < self.step_size:
            mag = self.min_val

        new_x = parent_node.pos[0] + int(mag * math.cos(angle))
        new_y = parent_node.pos[1] + int(mag * math.sin(angle))

        collision = False
        for obstacle in self.obstacles:
            if obstacle.collidepoint(new_x, new_y):
                collision = True
                break

        if not collision:
            parent_node.add_child(Node(new_x, new_y))

root = Node(150,150)
rrt = RRT(root, 25)
rrt.add_obstacle(pygame.Rect(600, 100, 200, 100))
rrt.add_obstacle(pygame.Rect(0, 400, 700, 50))
while 1:
    vis.plot_graph(rrt)
    rrt.step()
