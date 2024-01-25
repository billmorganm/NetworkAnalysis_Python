import networkx as nx

import network as nw

class NetworkAnalysis:
    def __init__(self, network, agents=[]):
        self.network: nx.Graph = network
        self.agents = []
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




class Agent:
    def __init__(self, id, start_time=0, current_node=None, path=[]):
        self.id = id
        self.start_time = start_time
        self.points_of_interest = {}  # TODO: dictionary to implement {"home": "Glen Waverley"}
        self.current_node = current_node
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
    def __init__(self):
        self.id = None
        self.start_time = 0
        self.home_base = None
        self.current_node = None
        self.current_edge = None
        self.current_edge_traversed = 0.0
        self.path = []
    def move(self):
        pass
    def log_event(self, log):
        # write key events and times to a log buffer. e.g. spawn, board, deboard, etc
        pass

