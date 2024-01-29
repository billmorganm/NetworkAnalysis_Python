import networkx as nx
import network as nw
from scipy.spatial.distance import euclidean
import random

class NetworkAnalysis:
    def __init__(self, network):
        self.network: nx.Graph = network

        # initialize engine objects
        self.stations: [Station] = [Station(name=node) for node in self.network.nodes if "Station" in node]
        for station in self.stations:
            platforms = [node for node in self.network.nodes if (f"{station.name.split(' Station')[0]} Platform" in node)]
            for platform in platforms:
                line_name = platform.split("(")[1].split(" Line")[0]
                station.add_platform(Platform(station, line_name))


        self.agents: [Agent] = []
        self.vehicles: [Vehicle] = []
        self.current_agent_id_counter = 1

    def reroute_idle_agents(self):
        pass

    def assign_path(self, agent, destination):
        pass

    def get_station_from_name(self, name):
        for station in self.stations:
            if station.name == name:
                return station

        # if exit without match
        raise ValueError("Station not found")

    def get_platform_from_name(self, name):
        for station in self.stations:
            for platform in station.platforms:
                if platform.name == name:
                    return platform

        # if exit without match
        raise ValueError("Platform not found")

    def add_agents(self, n=1, mode='population-weighted'):
        if mode != 'population-weighted':
            raise NotImplementedError("Mode not supported")

        suburbs = nw.get_suburbs()
        df_od_pairs = nw.generate_agent_od_pairs(suburbs, n)

        for _, row in df_od_pairs.iterrows():
            agent_id = self.current_agent_id_counter
            self.current_agent_id_counter += 1

            origin = f'{row["Moving From"]} Station'
            origin_station: Station = self.get_station_from_name(origin)
            destination = f'{row["Moving To"]} Station'

            path = nx.shortest_path(self.network, origin, destination)[1:]

            agent = Agent(agent_id, current_node=origin_station, path=path)
            self.agents.append(agent)
            origin_station.add_to_waiting_list(agent)

        for station in self.stations:
            station.process_waitlist()

    def add_test_vehicles(self):
        # path = nx.shortest_path(self.network,"Melbourne CBD Platform (Glen Waverley Line)", "Glen Waverley Station")
        vehicle1 = Vehicle(id=1,
                          engine=self,
                          current_node="Melbourne CBD Platform (Glen Waverley Line)" ,# path[0],
                          # path=path[1:],
                          assigned_line="Glen Waverley Line",
                          current_edge_traversed=0.0)

        vehicle2 = Vehicle(id=2,
                          engine=self,
                          current_node="Glen Waverley Platform (Glen Waverley Line)",  # path[0],
                          # path=path[1:],
                          assigned_line="Glen Waverley Line",
                          current_edge_traversed=0.0)

        vehicle3 = Vehicle(id=3,
                           engine=self,
                           current_node="Melbourne CBD Platform (Werribee Line)",  # path[0],
                           # path=path[1:],
                           assigned_line="Werribee Line",
                           current_edge_traversed=0.0)

        vehicle4 = Vehicle(id=4,
                           engine=self,
                           current_node="Melbourne CBD Platform (Pakenham Line)",  # path[0],
                           # path=path[1:],
                           assigned_line="Pakenham Line",
                           current_edge_traversed=0.0)

        vehicle5 = Vehicle(id=5,
                           engine=self,
                           current_node="Broadmeadows Platform (Broadmeadows Line)",
                           assigned_line="Broadmeadows Line",
                           current_edge_traversed=0.0)

        self.vehicles.extend([vehicle1, vehicle2, vehicle3, vehicle4, vehicle5])


class Agent:
    printing_logs = True

    def __init__(self, id, start_time=0, current_node=None, path=[]):
        self.id = id
        self.start_time = start_time
        self.points_of_interest = {}  # TODO: dictionary to implement {"home": "Glen Waverley"}
        self.current_node = current_node
        self.parent = None
        self.path = path
    def move(self):
        pass
    def log_event(self, message):
        if Agent.printing_logs:
            # write key events and times to a log buffer. e.g. spawn, board, deboard, etc
            print(f"A{self.id}: {message}")

    def __repr__(self):
        if len(self.path) > 1:
            if self.current_node is None:
                return f'Agent {self.id} > D: {self.path[-1]}'
            else:
                return f'Agent {self.id} | {self.current_node.name} > {self.path[-1]}'
        else:
            return f'Agent {self.id}'

class Vehicle:
    printing_logs = True

    def __init__(self, id, engine, capacity=50, current_node=None, assigned_line="", current_edge_traversed=0.0):
        self.id = id
        self.capacity = capacity
        self.speed = 0.1
        self.max_speed = 10
        self.max_acceleration = 2
        self.current_node = current_node
        self.current_edge_traversed = current_edge_traversed
        self.passengers = []
        self.assigned_line = assigned_line
        self.engine: NetworkAnalysis = engine
        self.path = []
        self.repopulate_path(current_node, trim_path=False)
        print(self.path)

    def repopulate_path(self, last_known_node, trim_path=True):
        lines = nw.get_lines()
        last_known_suburb = last_known_node.split("Platform")[0].strip().split("Station")[0].strip()

        for line in lines:
            line_name = line["line_name"]
            if line_name == self.assigned_line:

                first = f"{line['suburbs'][0]} Platform ({line_name})"
                last = f"{line['suburbs'][-1]} Platform ({line_name})"

                if last_known_suburb == line["suburbs"][-1]:
                    self.path = nx.shortest_path(self.engine.network, last, first)

                else:
                    self.path = nx.shortest_path(self.engine.network, first, last)

                if trim_path:
                    self.path = self.path[1:]

    def __repr__(self):
        return f"V{self.id}: {len(self.passengers)}/{self.capacity}"

    def move(self):

        self.current_edge_traversed += 0.008 #random.uniform(0.2,0.3)

        if self.current_edge_traversed > 1.0:

            self.current_edge_traversed = 0.0

            if len(self.path) > 0:
                self.current_node = self.path[0]
                self.path = self.path[1:]

                last_known_node = self.current_node

                # repopulate so that passengers on platform can board
                if self.path == []:
                    self.repopulate_path(self.current_node)

                # handle arrival
                platform = self.engine.get_platform_from_name(last_known_node)
                platform.process_vehicle_arrival(self)



    def add_passenger(self, passenger):
        self.passengers.append(passenger)

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


    def log_event(self, message):
        if Vehicle.printing_logs:
            # write key events and times to a log buffer. e.g. spawn, arrive, depart, load, unload
            print(f"V{self.id}: {message}")



class Platform:
    def __init__(self, station, line):
        self.station: Station = station
        self.line = line
        self.name: str = f"{station.name.split(' Station')[0]} Platform ({line} Line)"
        self.waitlist: [Agent] = []

    def __repr__(self):
        return self.name

    def add_to_waiting_list(self, passenger):

        self.waitlist.append(passenger)

    def remove_from_waiting_list(self, agents):
        pass

    def process_vehicle_arrival(self, vehicle: Vehicle):

        to_remove_from_vehicle = []

        # At an arrival event,
        for passenger in vehicle.passengers:
            if len(passenger.path) == 1:
                raise ValueError(f"Something wrong with {passenger}'s path, length 1")
            if passenger.path[0] != self.name:
                raise ValueError("This passenger is on the wrong station")

            if passenger.path[1] == self.station.name:
                # deboard passenger and put to station
                passenger.current_node = None # TODO
                passenger.parent = self.station
                passenger.path = passenger.path[2:] # move directly to station waitlist
                self.station.add_to_waiting_list(passenger)
                passenger.log_event(f"arrived at {self.station.name}")
                to_remove_from_vehicle.append(passenger)

            else:
                # passenger proceeds on their journey
                passenger.current_node = None  # TODO
                passenger.path = passenger.path[1:]

        # remove passengers from vehicle
        vehicle.passengers = [passenger for passenger in vehicle.passengers if passenger not in to_remove_from_vehicle]
        self.station.process_waitlist()

        remaining_capacity_on_vehicle = vehicle.capacity - len(vehicle.passengers)

        to_remove_from_waitlist = []
        for passenger in self.waitlist[:remaining_capacity_on_vehicle]:
            # check heading to the same nod
            if len(vehicle.path) == 0:
                return
            if passenger.path[0] == vehicle.path[0]:
                passenger.parent = vehicle
                vehicle.add_passenger(passenger)
                passenger.log_event(f"boarded V{vehicle.id}")
                to_remove_from_waitlist.append(passenger)

        self.waitlist = [passenger for passenger in self.waitlist if passenger not in to_remove_from_waitlist]

class Station:

    def __init__(self, name):
        self.name = name
        self.lines = []
        self.platforms: [Platform] = []
        self.waitlist: [Agent] = []

    def __repr__(self):
        return f'{self.name} <{len(self.platforms)} Platforms>'

    def add_platform(self, platform):
        self.platforms.append(platform)

    def add_to_waiting_list(self, passenger):
        passenger.parent = self
        self.waitlist.append(passenger)

    def integrate_line(self, line):
        pass

    def process_waitlist(self):
        to_remove = []

        for passenger in self.waitlist:
            if passenger.path == []:
                if passenger.id == 125:
                    print("DEBUG")
                passenger.log_event(f"{passenger} finished trip")
                passenger.parent = None
                to_remove.append(passenger)
            else:
                flag_successfully_processed = False
                # move to platform in their next node
                for platform in self.platforms:
                    if platform.name == passenger.path[0]:
                        passenger.parent = platform
                        passenger.path = passenger.path[1:]
                        platform.add_to_waiting_list(passenger)
                        to_remove.append(passenger)

                        flag_successfully_processed = True

                if not flag_successfully_processed:
                    raise ValueError(f"{repr(passenger)} in the wrong station")

        # remove passengers from to_remove
        self.waitlist = [passenger for passenger in self.waitlist if passenger not in to_remove]






