import networkx as nx
import matplotlib.pyplot as plt
from Core.network import G, volumes

# Draw the graph
pos = nx.get_node_attributes(G, 'pos')
# plt.figure(figsize=(20, 10))

# Nodes
station_nodes = [f"{node}" for node in G.nodes if "Station" in node]
platform_nodes = [f"{node}" for node in G.nodes if "Platform" in node]
# nx.draw_networkx_nodes(G, pos, nodelist=station_nodes, node_size=100, node_color='blue', alpha=0.8)
# nx.draw_networkx_nodes(G, pos, nodelist=platform_nodes, node_size=100, node_color='orange', alpha=0.8)

# Edges
# Update edges with volume information
for (u, v, data) in G.edges(data=True):
    data['volume'] = volumes[u][v] / 20
edge_colors = [color for _, _, color in G.edges.data('color')]
edge_widths = [data['volume'] for _, _, data in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, alpha=0.5, edge_cmap=plt.cm.Blues)

# Labels
labels = {node: node.split("(")[0] if "Station" in node else "" for node in G.nodes}
label_pos = {k: (v[0], v[1] + 0.008) for k, v in pos.items()}  # Adjust y-position for labels
nx.draw_networkx_labels(G, label_pos, labels=labels, font_size=10, font_color='black', font_weight='bold', verticalalignment='center')

# Title and Grid
plt.title("Melbourne Public Transportation Network", fontsize=16, fontweight='bold')
plt.grid(False)

# Display the graph
plt.axis('equal')  # Ensure equal aspect ratio
plt.show()