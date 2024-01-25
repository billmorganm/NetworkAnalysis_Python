import networkx as nx
import network as nw
from scipy.spatial.distance import euclidean
import random

class NetworkAnalysis:
    def __init__(self, network, agents=[]):
        self.network: nx.Graph = network
        self.agents: [Agent] = []
        self.vehicles: [Vehicle] = []
        self.current_agent_id_counter = 1

    def reroute_idle_agents(self):
        pass

    def assign_path(self, agent, destination):
        pass

    def add_agents(self, n=1, mode='population-weighted'):
        if mode != 'population-weighted':
            raise NotImplementedError("Mode not supported")

        suburbs = nw.get_suburbs()
        df_od_pairs = nw.generate_agent_od_pairs(suburbs, n)

        for _, row in df_od_pairs.iterrows():
            agent_id = self.current_agent_id_counter
            self.current_agent_id_counter += 1

            origin = f'{row["Moving From"]} Station'
            destination = f'{row["Moving To"]} Station'
            path = nx.shortest_path(self.network, origin, destination)

            agent = Agent(agent_id, current_node=origin, path=path)
            self.agents.append(agent)

    def add_test_vehicle(self):
        # path = nx.shortest_path(self.network,"Melbourne CBD Platform (Glen Waverley Line)", "Glen Waverley Station")
        vehicle1 = Vehicle(id=1,
                          network=self.network,
                          current_node="Melbourne CBD Platform (Glen Waverley Line)" ,# path[0],
                          # path=path[1:],
                          assigned_line="Glen Waverley Line",
                          current_edge_traversed=0.0)

        vehicle2 = Vehicle(id=2,
                          network=self.network,
                          current_node="Glen Waverley Platform (Glen Waverley Line)",  # path[0],
                          # path=path[1:],
                          assigned_line="Glen Waverley Line",
                          current_edge_traversed=0.0)

        vehicle3 = Vehicle(id=3,
                           network=self.network,
                           current_node="Melbourne CBD Platform (Werribee Line)",  # path[0],
                           # path=path[1:],
                           assigned_line="Werribee Line",
                           current_edge_traversed=0.0)

        vehicle4 = Vehicle(id=4,
                           network=self.network,
                           current_node="Melbourne CBD Platform (Pakenham Line)",  # path[0],
                           # path=path[1:],
                           assigned_line="Pakenham Line",
                           current_edge_traversed=0.0)

        self.vehicles.extend([vehicle1, vehicle2, vehicle3, vehicle4])



class Agent:
    def __init__(self, id, start_time=0, current_node=None, path=[]):
        self.id = id
        self.start_time = start_time
        self.points_of_interest = {}  # TODO: dictionary to implement {"home": "Glen Waverley"}
        self.current_node = current_node
        self.parent = None
        self.path = path
    def move(self):
        pass
    def log_event(self, log):
        # write key events and times to a log buffer. e.g. spawn, board, deboard, etc
        pass

    def __repr__(self):
        if len(self.path) > 1:
            return f'Agent {self.id} | {self.current_node} > {self.path[-1]}'
        else:
            return f'Agent {self.id}'

class Vehicle:
    def __init__(self, id, network, capacity=50, current_node=None, assigned_line="", path=[], current_edge_traversed=0.0):
        self.id = id
        self.capacity = capacity
        self.speed = 0.1
        self.max_speed = 10
        self.max_acceleration = 2
        self.current_node = current_node
        self.current_edge_traversed = current_edge_traversed
        self.path = path
        self.passengers = []
        self.assigned_line = assigned_line
        self.manifest = None  # TODO
        self.network = network

    def repopulate_path(self, last_known_node):
        lines = nw.get_lines()
        last_known_suburb = last_known_node.split("Platform")[0].strip().split("Station")[0].strip()

        for line in lines:
            line_name = line["line_name"]
            if line_name == self.assigned_line:

                first = f"{line['suburbs'][0]} Platform ({line_name})"
                last = f"{line['suburbs'][-1]} Platform ({line_name})"

                if last_known_suburb == line["suburbs"][-1]:
                    self.path = nx.shortest_path(self.network, last, first)[1:]

                else:
                    self.path = nx.shortest_path(self.network, first, last)[1:]

                print(self.path)

    def move(self):
        last_known_node = self.current_node
        self.current_edge_traversed += 0.05 #random.uniform(0.2,0.3)

        if self.current_edge_traversed > 1.0:
            self.current_edge_traversed = 0.0
            if len(self.path) > 0:
                self.current_node = self.path[0]
                self.path = self.path[1:]
            else:
                self.repopulate_path(last_known_node)


    def calculate_vehicle_position(self, network):
        current_node_pos = network.nodes[self.current_node]['pos']
        try:
            next_node_pos = network.nodes[self.path[0]]['pos']
        except:
            return current_node_pos


        edge_length = euclidean(current_node_pos, next_node_pos)

        edge_direction = (next_node_pos[0] - current_node_pos[0], next_node_pos[1] - current_node_pos[1])

        vehicle_position = (current_node_pos[0] + edge_direction[0] * self.current_edge_traversed,
                            current_node_pos[1] + edge_direction[1] * self.current_edge_traversed)

        return vehicle_position


    def log_event(self, log):
        # write key events and times to a log buffer. e.g. spawn, arrive, depart, load, unload
        pass

