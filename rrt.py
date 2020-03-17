import visualizer as vis 
import random as rdm
import pygame, time, math

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
        self.prev_node = None
        self.g_score = math.inf
        self.heuristic = math.inf
    
    def add_child(self, child):
        self.children.append(child)

class RRT:
    def __init__(self, root, step_size):
        self.root = root
        self.step_size = step_size
        self.obstacles = []
        self.path = None
        self.goal = None

    def find_closest_node(self, node, pnt):
        for child in node.children:
            dist_val = dist(child.pos, pnt)
            if dist_val < self.min_val:
                self.min_val = dist_val
                self.min_node = child
            self.find_closest_node(child, pnt)

    def add_obstacle(self, obstacle, style):
        self.obstacles.append((obstacle, style))

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
            if x_diff < 0:
                if y_diff < 0:
                    angle += 180
                else:
                    angle += 90
            else:
                if y_diff < 0:
                    angle += 270
        mag = self.step_size
        if self.min_val < mag:
            mag = self.min_val

        new_x = parent_node.pos[0] + int(mag * math.cos(angle))
        new_y = parent_node.pos[1] + int(mag * math.sin(angle))

        collision = False

        if (new_x > width) or (new_x < 0):
            collision = True
        
        if (new_y > height) or (new_y < 0):
            collision = True

        for obstacle in self.obstacles:
            if obstacle[0].collidepoint(new_x, new_y):
                collision = True
                break

        if not collision:
            parent_node.add_child(Node(new_x, new_y))

    def find_path(self):
        dest_x = rdm.randint(0, width)
        dest_y = rdm.randint(0, height)
        dest = (dest_x, dest_y)
        self.goal = dest
        
        open_set = [self.root]
        closed_set = []
        prev_node = None

        while open_set:
            current = min(open_set, key=lambda node: node.g_score + node.heuristic) 
            if dist(current.pos, dest) < 20:
                self.path = current
                break

            open_set.remove(current)
            closed_set.append(current)
            
            for child in current.children:
                if child in closed_set:
                    continue

                if child in open_set:
                    tmp_score = current.g_score + dist(current.pos, child.pos)
                    if tmp_score < child.g_score:
                        child.g_score = tmp_score
                        child.prev_node = current
                    continue
                
                child.g_score = current.g_score + dist(current.pos, child.pos)
                child.heuristic = dist(child.pos, dest)
                child.prev_node = current
                open_set.append(child)

root = Node(150,150)
rrt = RRT(root, 30)
rrt.add_obstacle(pygame.Rect(600, 100, 200, 100), "ellipse")
rrt.add_obstacle(pygame.Rect(200, 400, 500, 50), "rect")
for x in range(1750):    
    vis.plot_graph(rrt)
    rrt.step()
    time.sleep(0.005)

rrt.find_path()
vis.plot_path(rrt)
