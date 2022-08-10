import numpy as np

# TODO:
#  enum LineDirection {
#     case Northbound
#     case Southbound
#     case Clockwise
#     case CounterClockwise
#     case Downtown
#     case Uptown
# }

class Line:
    count = 0

    def __init__(self, name):
        self.id = Line.count + 1;
        Line.count += 1

        self.name = name
        self.stops = []
        self.vehicles = []
        pass

    def add_vehicle(self):
        pass

    def get_stops(self):
        return self.stops

    def get_vehicles(self):
        return self.vehicles

    def remove_stop(self, stop):
        pass

    def add_stop(self, station, index=None):
        """Add the station to the list at the index specified as 'index'. If None, add to the end of the line"""
        stop = TransitStop(station, line=self)
        if index is None:
            self.stops.append(stop)
        else:
            self.stops.insert(index, stop)

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle):
        self.vehicles.remove(vehicle)

    def __repr__(self):
        return f'<Line {self.id}> {self.name}'

class TransitStop:
    def __init__(self, station, line):
        self.station = station
        self.line = line
        self.waiting_list = [] # TODO

    def move_to_waiting_list(self, agents):
        pass

    def remove_from_waiting_list(self, agents):
        pass

    def process_arrivals(self, agents):
        pass

class Station:
    count = 0

    def __init__(self, name, x, y):
        self.id = Station.count + 1
        Station.count += 1
        self.name = name
        self.location = (float(x), float(y))
        self.lines = []
        self.stops = []  # TODO

    def __repr__(self):
        return f'<Station {self.id}> {self.name} at {self.location}'

    def process_arrivals(self, agents):
        pass

    def integrate_line(self, line):
        pass

class Vehicle:
    count = 0

    def __init__(self, capacity, assigned_line):
        self.id = Vehicle.count + 1
        Vehicle.count += 1
        self.capacity = capacity
        self.max_speed = 10
        self.max_acceleration = 2
        self.passengers = []
        self.path = []
        self.assigned_line = assigned_line
        self.manifest = None # TODO
        pass

    def __repr__(self):
        return f'<Vehicle {self.id}>'

    def move(self):
        pass

    def load_passengers(self, agents):
        pass

    def unload_passengers(self, agents):
        pass

    def update_manifest(self):
        pass

class Agent:
    count = 0

    def __init__(self, origin, destination):
        self.id = Agent.count + 1
        Agent.count += 1
        self.origin = origin
        self.destination = destination
        self.path = [] # TODO
        pass

    def set_new_path(self, path):
        pass

    def get_next_transit_stop(self):
        pass

    def get_disembarkation_point(self):
        pass

    def update_path(self, pop_first_element=True):
        pass

    def __repr__(self):
        return f'<Agent {self.id}>'