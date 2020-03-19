import rrt, sys, pygame, time
from PIL import Image

COLOR_NODES = False

NODE_RADIUS = 4
EDGE_WIDTH = 3
EDGE_COLOR = 0, 0, 0
START_NODE_COLOR = 0, 155, 155
END_NODE_COLOR = 155, 0, 0
GOAL_COLOR = 0, 200, 0, 50
PATH_COLOR = 155, 0, 0
PATH_NODE_RADIUS = 10
PATH_WIDTH = 5

pygame.init()

file_name = "test_map.png"

PIL_image = Image.open(file_name)

screen = pygame.display.set_mode(PIL_image.size)
background_image = pygame.image.load(file_name).convert()

def plot_graph(graph):
    plot_node(graph.root)
    pygame.display.update()

def plot_path(graph):
    if graph.end_node is None:
        return

    path = [graph.end_node]

    node = graph.end_node.prev_node
    while True:
        path.insert(0, node)
        if node.prev_node is None:
            break
        node = node.prev_node
    
    start_pos = node.pos
    draw_circle(START_NODE_COLOR, start_pos, PATH_NODE_RADIUS)
    pygame.display.update()

    for node in path:
        if node.prev_node is not None:
            draw_path(node.prev_node, node)

        pygame.display.update()
        time.sleep(0.5)

def plot_node(node):
    for child in node.children:
        draw_edge(node, child)
        plot_node(child)

    draw_node(node)

def draw_node(node):
    pygame.draw.circle(screen, node.color, node.pos, NODE_RADIUS)

def draw_edge(start, end):
    pygame.draw.line(screen, EDGE_COLOR, start.pos, end.pos, EDGE_WIDTH)

def draw_path(start, end):
    pygame.draw.line(screen, PATH_COLOR, start.pos, end.pos, PATH_WIDTH)

def draw_goal(goal):
    draw_circle(GOAL_COLOR, (goal[0], goal[1]), goal[2])

def draw_circle(color, pnt, radius):
    pygame.draw.circle(screen, color, pnt, radius)

root = rrt.Node(300,150)
graph = rrt.Graph(root, 50, PIL_image.load(), PIL_image.size[0], PIL_image.size[1])

screen.blit(background_image, [0, 0])
draw_goal(graph.goal)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    while graph.end_node is None:
        graph.add_node() 
        plot_graph(graph)

        if graph.end_node is not None:
            graph.find_path() 
            plot_path(graph) 
