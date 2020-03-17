import sys, pygame
pygame.init()

# Constants
node_radius = 5
edge_width = 3
node_color = 1, 84, 143
edge_color = 0, 0, 0

size = width, height = 1024, 576
white = 255, 255, 255

screen = pygame.display.set_mode(size)

def draw_node(node):
    pygame.draw.circle(screen, node_color, node.pos, node_radius)

def draw_edge(start, end):
    pygame.draw.line(screen, edge_color, start.pos, end.pos, edge_width)

def plot_node(node):
    for child in node.children:
        draw_edge(node, child)
        plot_node(child)

    draw_node(node)

def plot_graph(root):
    screen.fill(white)
    
    plot_node(root)
    
    pygame.display.flip()
