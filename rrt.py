import random as rdm
import pygame, time, math

class Node:
    def __init__(self, x, y):
        self.pos = x, y

        # Assigns a random color to each Node
        self.color = rdm.randint(0, 255), rdm.randint(0, 255), rdm.randint(0, 255)
        
        self.children = []

        # Values for A*
        self.prev_node = None
        self.g_score = math.inf
        self.heuristic = math.inf
    
    def add_child(self, child):
        self.children.append(child)
    
class Graph:
    def __init__(self, root, step_size, obstacle_map, width, height, goal=None):
        self.root = root

        # Max distance between any two nodes
        self.step_size = step_size

        self.map = obstacle_map
        self.width = width
        self.height = height
       
        # Stores the last nodes added
        self.last_child_node = root
        self.last_parent_node = None
        
        self.goal = goal

        # If no goal is set, create a one at a random point
        if self.goal is None:
            dest_x = rdm.randint(0, self.width)
            dest_y = rdm.randint(0, self.height)
            dest_radius = 25
            self.goal = (dest_x, dest_y, dest_radius)

    def distance(self, start, end):
        """ Finds the euclidean distance between two points """

        x_comp = end[0] - start[0]
        y_comp = end[1] - start[1]

        return math.sqrt(math.pow(x_comp, 2) + math.pow(y_comp, 2))
    
    def check_distance(self, node, pnt):
        """ Checks the distance between each child and the given point """
        for child in node.children:
            distance = self.distance(child.pos, pnt)
            if distance < self.min_distance:
                self.min_distance = distance
                self.closest_node = child
            # Runs the same check on each of the child's children
            self.check_distance(child, pnt)

    def find_closest_node(self, pnt):
        """ 
        Finds the node on the graph closest to the chosen point, then 
        sets closest_node
        """
        self.min_distance = self.distance(self.root.pos, pnt)
        self.closest_node = self.root
        
        self.check_distance(self.root, pnt)

    def reached_goal(self, pnt):
        x_comp = math.pow(pnt[0] - self.goal[0], 2)
        y_comp = math.pow(pnt[1] - self.goal[1], 2)

        return math.sqrt(x_comp + y_comp) <= self.goal[2]

    def add_node(self):
        """ Uses RRT to define another point within the map """

        # Creates a random point on the graph
        target_x = rdm.randint(0, self.width)
        target_y = rdm.randint(0, self.height)
        target = (target_x, target_y)

        # Gets the node we'll be adding a child too
        self.find_closest_node((target_x, target_y))
        parent_node = self.closest_node
        init_x = parent_node.pos[0]
        init_y = parent_node.pos[1]
        x_diff = target_x - init_x 
        y_diff = target_y - init_y 

        angle = math.atan2(y_diff, x_diff)
        mag = self.step_size
        if self.distance(target, parent_node.pos) < mag:
            mag = int(self.distance(target, parent_node.pos))

        x = init_x + int(mag * math.cos(angle))
        y = init_y + int(mag * math.sin(angle))

        collision = False
        for i in range(mag + 1):
            inner_x = init_x + int(i * math.cos(angle))
            inner_y = init_y + int(i * math.sin(angle))
            if (inner_x >= self.width) or (inner_x < 0):
                return
            elif (inner_y >= self.height) or (inner_y < 0):
                return
            elif self.map[inner_x, inner_y] == (0, 0, 0):
                return
            elif self.reached_goal((inner_x, inner_y)):
                child_node = Node(inner_x, inner_y)
                parent_node.add_child(child_node)

                self.last_child_node = child_node
                self.last_parent_node = parent_node
                return
        
        child_node = Node(x, y)   
        parent_node.add_child(child_node)

        self.last_child_node = child_node
        self.last_parent_node = parent_node

    def find_path(self):
        """ Searches the graph to find the shortest path to the goal """
        
        open_set = [self.root]
        closed_set = []
        prev_node = None

        while open_set:
            current = min(open_set, key=lambda node: node.g_score + node.heuristic) 

            # If last node added did not reach the goal
            if not self.reached_goal(self.last_child_node.pos): 
                if self.distance(current.pos, self.goal) < 20:
                    self.last_child_node = current
                    break
            elif self.last_child_node == current:
                break

            open_set.remove(current)
            closed_set.append(current)
            
            for child in current.children:
                if child in closed_set:
                    continue

                if child in open_set:
                    tmp_score = current.g_score + self.distance(current.pos, child.pos)
                    if tmp_score < child.g_score:
                        child.g_score = tmp_score
                        child.prev_node = current
                    continue
                
                child.g_score = current.g_score + self.distance(current.pos, child.pos)
                child.heuristic = self.distance(child.pos, self.goal)
                child.prev_node = current
                open_set.append(child)


