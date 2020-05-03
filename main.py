import rrt, sys, pygame, time, math
from PIL import Image

COLOR_NODES = True

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

file_name = sys.argv[1]
PIL_image = Image.open(file_name)

screen = pygame.display.set_mode(PIL_image.size)
background_image = pygame.image.load(file_name).convert()

def plot_node(graph):
    if graph.last_parent_node is not None: 
        draw_edge(graph.last_parent_node, graph.last_child_node)
    if COLOR_NODES:
        draw_node(graph.last_child_node)
    pygame.display.update()

def plot_path(graph):
    if graph.last_child_node is None:
        return

    path = [graph.last_child_node]

    node = path[0].prev_node
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
            x_diff = node.pos[0] - node.prev_node.pos[0]
            y_diff = node.pos[1] - node.prev_node.pos[1]
            last_x = node.prev_node.pos[0]
            last_y = node.prev_node.pos[1]
            angle = math.atan2(y_diff, x_diff)
            distance = int(math.sqrt(math.pow(x_diff,2) + math.pow(y_diff,2)))
            step = distance / 3
            for i in range(3):
                x = last_x + int(step * math.cos(angle))
                y = last_y + int(step * math.sin(angle))
                draw_path((last_x, last_y), (x, y))
                last_x = x
                last_y = y
                pygame.display.flip()
                time.sleep(0.03)
            draw_path((last_x, last_y), node.pos)
            pygame.display.update()

def draw_node(node):
    pygame.draw.circle(screen, node.color, node.pos, NODE_RADIUS)

def draw_edge(start, end):
    pygame.draw.line(screen, EDGE_COLOR, start.pos, end.pos, EDGE_WIDTH)

def draw_path(start, end):
    pygame.draw.line(screen, PATH_COLOR, start, end, PATH_WIDTH)

def draw_goal(goal):
    draw_circle(GOAL_COLOR, (goal[0], goal[1]), goal[2])

def draw_circle(color, pnt, radius):
    pygame.draw.circle(screen, color, pnt, radius)

root = rrt.Node(300,150)
graph = rrt.Graph(root, 50, PIL_image.load(), PIL_image.size[0], PIL_image.size[1])

screen.blit(background_image, [0, 0])
draw_goal(graph.goal)
pygame.display.update()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    while not graph.reached_goal(graph.last_child_node.pos):
        graph.add_node() 
        plot_node(graph)
        time.sleep(0.005)

        if graph.reached_goal(graph.last_child_node.pos):
            graph.find_path() 
            plot_path(graph)
