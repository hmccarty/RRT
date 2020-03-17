import sys, pygame, time
import random as rdm
pygame.init()

# Constants
node_radius = 4
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
    shape = obstacle[0].copy()
    shape.inflate_ip(-15, -15)
    if obstacle[1] == "ellipse":
        pygame.draw.ellipse(screen, obstacle_color, shape)
    elif obstacle[1] == "rect":
        pygame.draw.rect(screen, obstacle_color, shape) 

def draw_root(node):
    pygame.draw.circle(screen, (200, 0, 20), node.pos, 15)

def draw_goal(pos):
    pygame.draw.circle(screen, (200, 0, 20), pos, 15)

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

def plot_path(graph):
    path_length = 0
    curr_node = graph.path
    while curr_node is not None:
        path_length += 1
        curr_node = curr_node.prev_node

    for i in range(path_length):
        screen.fill(white)
    
        plot_tree(graph.root)
        for obstacle in graph.obstacles:
            draw_obstacle(obstacle)

        draw_root(graph.root)
        draw_goal(graph.goal)

        curr_node = graph.path
        for j in range(i):
            pygame.draw.line(screen, (200, 0, 20), curr_node.pos, curr_node.prev_node.pos, 5)
            curr_node = curr_node.prev_node
    
        pygame.display.flip()
        
        time.sleep(0.075)
