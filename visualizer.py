import pygame

NODE_RADIUS = 4
EDGE_WIDTH = 3
EDGE_COLOR = 0, 0, 0
START_NODE_COLOR = 0, 155, 155
END_NODE_COLOR = 155, 0, 0
GOAL_COLOR = 0, 200, 0, 50
PATH_COLOR = 155, 0, 0
PATH_NODE_RADIUS = 10
PATH_WIDTH = 5

def draw_node(screen, node):
    pygame.draw.circle(screen, node.color, node.pos, NODE_RADIUS)

def draw_edge(screen, start, end):
    pygame.draw.line(screen, EDGE_COLOR, start.pos, end.pos, EDGE_WIDTH)

def draw_path(screen, start, end):
    pygame.draw.line(screen, PATH_COLOR, start.pos, end.pos, PATH_WIDTH)

def draw_goal(screen, goal):
    draw_circle(GOAL_COLOR, (goal[0], goal[1]), goal[2])

def draw_circle(screen, color, pnt, radius):
    pygame.draw.circle(screen, color, pnt, radius)

def plot_node(screen, node):
    for child in node.children:
        draw_edge(screen, node, child)
        plot_node(screen, child)

    draw_node(screen, node)

def plot_graph(screen, graph):
    screen.blit(background_image, [0, 0])
    
    draw_goal(graph.goal)
    plot_node(graph.root)
    
    pygame.display.flip()

def plot_path(screen, graph):
    if graph.end_node is None:
        return

    inactive_path = [graph.end_node]
    active_path = []

    node = graph.end_node.prev_node
    while True:
        inactive_path.insert(0, node)
        if node.prev_node is None:
            break
        node = node.prev_node
    
    screen.blit(background_image, [0, 0])
    draw_goal(graph.goal)
    plot_node(graph.root)
    start_pos = node.pos
    draw_circle(START_NODE_COLOR, start_pos, PATH_NODE_RADIUS)
    pygame.display.flip()

    while inactive_path:
        screen.blit(background_image, [0, 0])
        draw_goal(graph.goal)
        plot_node(graph.root)
        draw_circle(START_NODE_COLOR, start_pos, PATH_NODE_RADIUS)
        
        active_path.append(inactive_path.pop(0))

        for node in active_path:
            if node.prev_node is not None:
                draw_path(node.prev_node, node)

        pygame.display.flip()
        time.sleep(0.5)

