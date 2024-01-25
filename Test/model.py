

class NetworkAnalysis:
    def __init__(self):
        self.network = None
        self.agents = []

    def reroute_idle_agents(self):
        pass
    def assign_path(self, agent, destination):
        pass

class Agent:
    def __init__(self):
        self.id = None
        self.start_time = 0
        self.home_base = None
        self.current_node = None
        self.current_edge = None
        self.current_edge_percent = 0.0
        self.path = []
    def move(self):
        pass
    def log_event(self):
        # write key events and times to a log buffer. e.g. spawn, board, deboard, etc
        pass
