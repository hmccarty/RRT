import sys, pygame
import random as rdm
pygame.init()

# Constants
node_radius = 5
edge_width = 3
edge_color = 0, 0, 0
obstacle_color = 0, 0, 0

bg_color = 255, 255, 255
size = width, height = 1024, 576
white = 255, 255, 255

screen = pygame.display.set_mode(size)

def draw_node(node):
    pygame.draw.circle(screen, node.color, node.pos, node_radius)

def draw_edge(start, end):
    pygame.draw.line(screen, edge_color, start.pos, end.pos, edge_width)

def draw_obstacle(obstacle):
    shape = obstacle.copy()
    shape.inflate_ip(-15, -15)
    pygame.draw.rect(screen, obstacle_color, shape) 

def plot_tree(node):
    for child in node.children:
        draw_edge(node, child)
        plot_tree(child)

    draw_node(node)

def plot_graph(graph):
    screen.fill(white)
    
    plot_tree(graph.root)
    for obstacle in graph.obstacles:
        draw_obstacle(obstacle)
    
    pygame.display.flip()
