import networkx as nx
import matplotlib.pyplot as plt
import random


def generate_grid_graph(rows, cols):
    G = nx.grid_2d_graph(rows, cols)

    # Add random roads
    for edge in G.edges():
        if random.random() < 0.5:
            G[edge[0]][edge[1]]['road'] = 1

    return G


def draw_grid_graph(G):
    pos = {(x, y): (y, -x) for x, y in G.nodes()}

    node_colors = ['red' if 'road' in G.nodes[node] else 'white' for node in G.nodes()]

    nx.draw(G, pos, with_labels=True, node_size=100, node_color=node_colors)
    plt.show()


def main():
    rows, cols = 5, 5  # Adjust the grid size as needed
    G = generate_grid_graph(rows, cols)
    draw_grid_graph(G)


if __name__ == "__main__":
    main()
