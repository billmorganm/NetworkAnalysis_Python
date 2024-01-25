import networkx as nx
import matplotlib.pyplot as plt
import volumes
import pandas as pd
import numpy as np
import networkx as nx
from scipy.spatial.distance import euclidean
import pandas as pd
from pandas import DataFrame

def get_suburbs():
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
    return suburbs

def create_graph(suburbs):
    # Create a graph
    G = nx.Graph()

    # Define lines as dictionaries containing their name, list of suburbs, and color
    line_1 = {"name": "Glen Waverley Line", "suburbs": ["Melbourne CBD", "Richmond", "Tooronga", "Syndal", "Glen Waverley"],
              "color": "blue"}
    line_2 = {"name": "Werribee Line", "suburbs": ["Melbourne CBD", "Footscray", "Spotswood", "Laverton", "Werribee"],
              "color": "red"}
    line_3 = {"name": "Pakenham Line",
              "suburbs": ["Melbourne CBD", "Richmond", "Caulfield", "Clayton", "Dandenong", "Pakenham"], "color": "green"}
    line_4 = {"name": "Broadmeadows Line",
              "suburbs": ["Melbourne CBD", "North Melbourne", "Essendon", "Pascoe Vale", "Broadmeadows"], "color": "yellow"}

    lines = [line_1, line_2, line_3, line_4]

    # Step 1: Create station nodes
    for suburb in suburbs:
        station_name = f"{suburb} Station"
        G.add_node(station_name, pos=suburbs[suburb])

    # Step 2: Create platform nodes and link together nodes in the same line
    def add_line_to_graph(graph, line):
        for i in range(len(line["suburbs"]) - 1):
            platform_node_1 = f"{line['suburbs'][i]} Platform ({line['name']})"
            platform_node_2 = f"{line['suburbs'][i + 1]} Platform ({line['name']})"

            graph.add_node(platform_node_1, pos=suburbs[line['suburbs'][i]])
            graph.add_node(platform_node_2, pos=suburbs[line['suburbs'][i + 1]])

            graph.add_edge(platform_node_1, platform_node_2, line=line['name'], color=line['color'], train_position=0)

    # Add lines to the graph
    add_line_to_graph(G, line_1)
    add_line_to_graph(G, line_2)
    add_line_to_graph(G, line_3)
    add_line_to_graph(G, line_4)


    # Step 3: Connect platform nodes to their corresponding station node
    def connect_platforms_to_station(graph, line):
        for suburb in line["suburbs"]:
            station_node = f"{suburb} Station"
            platform_node = f"{suburb} Platform ({line['name']})"

            graph.add_edge(station_node, platform_node, line=line['name'], color='gray', train_position=0.1)


    # Connect platforms to station for each line
    connect_platforms_to_station(G, line_1)
    connect_platforms_to_station(G, line_2)
    connect_platforms_to_station(G, line_3)
    connect_platforms_to_station(G, line_4)

    return G

def get_volumes(G, suburbs):
    # Melbourne CBD coordinates
    cbd_coordinates = suburbs["Melbourne CBD"]

    # Function to calculate population based on inverse distance
    def calculate_population(distance):
        return max(int(np.random.normal(5000 * (1 / (distance + 1)), 1000)), 100)


    # Generate population dictionary
    population_dict = {suburb: calculate_population(euclidean(cbd_coordinates, np.array(coords))) for suburb, coords in
                       suburbs.items()}

    print("Population Dictionary inversely proportional to Distance to Melbourne CBD:")
    print(population_dict)

    # Convert dictionary to Pandas DataFrame
    df_population = DataFrame(list(population_dict.items()), columns=['Suburb', 'Population'])

    # Display the DataFrame
    df_population

    # Assuming df_population is the DataFrame containing suburbs and populations

    # Extract populations and suburbs from the DataFrame
    populations = df_population['Population'].values
    suburbs = df_population['Suburb'].values

    # Normalize populations to create probability distribution
    probabilities = populations / np.sum(populations)

    # Set the seed
    np.random.seed(42)
    movement_simulation_o = np.random.choice(suburbs, size=1000, p=probabilities)

    np.random.seed(100)
    movement_simulation_d = np.random.choice(suburbs, size=1000, p=probabilities)

    # Create a new DataFrame for the simulation results
    df_simulation = DataFrame(
        {'Person': range(1, 1001), 'Moving From': movement_simulation_o, 'Moving To': movement_simulation_d})

    # Display the simulation results
    (df_simulation)

    import pandas as pd

    # Assuming you have the DataFrame df_simulation from the previous steps
    # ...

    # Group by (Origin, Destination) and count occurrences
    grouped_df = df_simulation.groupby(['Moving From', 'Moving To']).size().reset_index(name='Count').sort_values(
        by="Count", ascending=False)

    # Display the grouped DataFrame
    print(grouped_df)

    # Group by (Origin, Destination) and count occurrences
    grouped_df = df_simulation.groupby(['Moving From', 'Moving To']).size().reset_index(name='Count').sort_values(
        by="Count", ascending=False)

    # Display the grouped DataFrame
    print(grouped_df)

    a = grouped_df.apply(
        lambda row: " > ".join(nx.shortest_path(G, f'{row["Moving From"]} Station', f'{row["Moving To"]} Station')), axis=1)

    paths = grouped_df.copy()
    paths['Path'] = a
    paths.head()


    def get_traffic_dict(paths_df):
        result = dict()
        for index, row in paths_df.iterrows():
            stops = row['Path'].split(" > ")
            if len(stops) == 1:
                pass
            else:
                for i in range(len(stops) - 1):
                    if stops[i] in result:
                        if stops[i + 1] in result[stops[i]]:
                            result[stops[i]][stops[i + 1]] += row['Count']
                        else:
                            result[stops[i]][stops[i + 1]] = row['Count']
                    else:
                        result[stops[i]] = {}
                        result[stops[i]][stops[i + 1]] = row['Count']
        return result


    volumes = get_traffic_dict(paths_df=paths)
    return volumes