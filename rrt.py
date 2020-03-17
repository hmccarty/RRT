import visualizer as vis 
import random as rdm

class Node:
    def __init__(self, x, y):
        self.pos = x, y
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)

class RRT:
    def __init__(self, root, step_size, screen_x, screen_y):
        self.root = root
        self.step_size = step_size
        self.screen_x = screen_x
        self.screen_y = screen_y

root = Node(150, 150)
root.add_child(Node(0, 0))


while 1:
    vis.plot_graph(root)

