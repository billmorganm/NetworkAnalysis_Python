import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import volumes

import networkx as nx
import matplotlib.pyplot as plt
import volumes
import pandas as pd

# Create a graph
G = nx.Graph()

# Define suburbs and their coordinates
suburbs = {
    "Melbourne CBD": (144.9631, -37.8136),
    "Richmond": (145.0000, -37.8183),
    "Tooronga": (145.0441, -37.8483),
    "Syndal": (145.1234, -37.8760),
    "Glen Waverley": (145.1616, -37.8779),
    "Footscray": (144.8992, -37.8000),
    "Spotswood": (144.8838, -37.8333),
    "Laverton": (144.7757, -37.8595),
    "Werribee": (144.6630, -37.9026),
    "Caulfield": (145.0220, -37.8776),
    "Clayton": (145.1195, -37.9245),
    "Dandenong": (145.2149, -37.9875),
    "Pakenham": (145.4900, -38.0703),
    "North Melbourne": (144.9447, -37.8070),
    "Essendon": (144.9175, -37.7515),
    "Pascoe Vale": (144.9471, -37.7268),
    "Broadmeadows": (144.9190, -37.6841),
}

# Define lines as dictionaries containing their node_name, list of suburbs, and color
line_1 = {"node_name": "Glen Waverley Line", "suburbs": ["Melbourne CBD", "Richmond", "Tooronga", "Syndal", "Glen Waverley"],
          "color": "blue"}
line_2 = {"node_name": "Werribee Line", "suburbs": ["Melbourne CBD", "Footscray", "Spotswood", "Laverton", "Werribee"],
          "color": "red"}
line_3 = {"node_name": "Pakenham Line",
          "suburbs": ["Melbourne CBD", "Richmond", "Caulfield", "Clayton", "Dandenong", "Pakenham"], "color": "green"}
line_4 = {"node_name": "Broadmeadows Line",
          "suburbs": ["Melbourne CBD", "North Melbourne", "Essendon", "Pascoe Vale", "Broadmeadows"], "color": "yellow"}

lines = [line_1, line_2, line_3, line_4]

# Step 1: Create station nodes
for suburb in suburbs:
    station_name = f"{suburb} Station"
    G.add_node(station_name, pos=suburbs[suburb])


# Step 2: Create platform nodes and link together nodes in the same line
def add_line_to_graph(graph, line):
    for i in range(len(line["suburbs"]) - 1):
        platform_node_1 = f"{line['suburbs'][i]} Platform ({line['node_name']})"
        platform_node_2 = f"{line['suburbs'][i + 1]} Platform ({line['node_name']})"

        graph.add_node(platform_node_1, pos=suburbs[line['suburbs'][i]])
        graph.add_node(platform_node_2, pos=suburbs[line['suburbs'][i + 1]])

        graph.add_edge(platform_node_1, platform_node_2, line=line['node_name'], color=line['color'], train_position=0)


# Add lines to the graph
add_line_to_graph(G, line_1)
add_line_to_graph(G, line_2)
add_line_to_graph(G, line_3)
add_line_to_graph(G, line_4)


# Step 3: Connect platform nodes to their corresponding station node
def connect_platforms_to_station(graph, line):
    for suburb in line["suburbs"]:
        station_node = f"{suburb} Station"
        platform_node = f"{suburb} Platform ({line['node_name']})"

        graph.add_edge(station_node, platform_node, line=line['node_name'], color='gray', train_position=0.1)


# Connect platforms to station for each line
connect_platforms_to_station(G, line_1)
connect_platforms_to_station(G, line_2)
connect_platforms_to_station(G, line_3)
connect_platforms_to_station(G, line_4)

volumes = volumes.get_traffic(G, suburbs)

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
# nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, alpha=0.5, edge_cmap=plt.cm.Blues)

# Labels
labels = {node: node.split("(")[0] if "Station" in node else "" for node in G.nodes}
label_pos = {k: (v[0], v[1] + 0.008) for k, v in pos.items()}  # Adjust y-position for labels
# nx.draw_networkx_labels(G, label_pos, labels=labels, font_size=10, font_color='black', font_weight='bold', verticalalignment='center')

# Title and Grid
# plt.title("Melbourne Public Transportation Network", fontsize=16, fontweight='bold')
# plt.grid(False)

# Step 4: Extract nodes and edges information for DataFrame creation
nodes_data = {'Node': [], 'Latitude': [], 'Longitude': []}
edges_data = {'Source': [], 'Target': [], 'Line': [], 'Color': [], 'Train_Position': [], 'Volume': []}

for node, pos in nx.get_node_attributes(G, 'pos').items():
    nodes_data['Node'].append(node)
    nodes_data['Latitude'].append(pos[1])
    nodes_data['Longitude'].append(pos[0])

for u, v, data in G.edges(data=True):
    edges_data['Source'].append(u)
    edges_data['Target'].append(v)
    edges_data['Line'].append(data['line'])
    edges_data['Color'].append(data['color'])
    edges_data['Train_Position'].append(data['train_position'])
    edges_data['Volume'].append(data['volume'])

# Step 5: Create DataFrames
nodes_df = pd.DataFrame(nodes_data)
edges_df = pd.DataFrame(edges_data)

# Step 6: Save DataFrames to CSV files
nodes_df.to_csv('nodes.csv', index=False)
edges_df.to_csv('edges.csv', index=False)

# Step 7: Display the DataFrames
print("Nodes DataFrame:")
print(nodes_df)
print("\nEdges DataFrame:")
print(edges_df)
