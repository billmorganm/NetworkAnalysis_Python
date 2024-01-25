######
import pygame
from pygame.locals import QUIT
import networkx as nx
from sim import G


# Create Pygame window
pygame.init()
window_size = (1600, 1200)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Train Simulation")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Main simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the graph
    pos = nx.get_node_attributes(G, 'pos')
    station_nodes = [f"{node}" for node in G.nodes if "Station" in node]
    edge_colors = [color for _, _, color in G.edges.data('color')]
    edge_widths = [data['volume'] for _, _, data in G.edges(data=True)]
    train_positions = [data['train_position'] for _, _, data in G.edges(data=True)]

    # nx.draw_networkx_nodes(G, pos, nodelist=station_nodes, node_size=100, node_color='blue', alpha=0.8)
    # nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, alpha=0.5, edge_cmap=plt.cm.Blues)

    # Update train positions
    for (u, v, data) in G.edges(data=True):
        data['train_position'] += 10  # Adjust the increment as needed
        if data['train_position'] > 1000:
            data['train_position'] = 0  # Reset train position when it reaches the next station

    # Draw trains
    for (u, v, data) in G.edges(data=True):
        train_pos_x = pos[u][0] + (pos[v][0] - pos[u][0]) * data['train_position']
        train_pos_y = pos[u][1] + (pos[v][1] - pos[u][1]) * data['train_position']
        pygame.draw.circle(screen, (255, 0, 0), (int(train_pos_x+100)*3, int(train_pos_y+100)*3), 10)

    # Refreshes the window
    pygame.display.update()
    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
