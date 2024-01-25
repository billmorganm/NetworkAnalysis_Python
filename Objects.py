import numpy as np
import Helper as h

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

    def __init__(self, name, stops=[]):
        self.id = Line.count + 1;
        Line.count += 1

        self.name = name
        self.stops = stops
        self.vehicles = []
        pass

    def add_vehicle(self, vehicle):
        vehicle.update_path()
        self.vehicles.append(vehicle)

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
    passenger_count = 0.0
    arrival_multiplier = 0


    def __init__(self, name, x, y):
        self.id = Station.count + 1
        Station.count += 1
        self.name = name
        self.location = (float(x), float(y))
        self.lines = []
        self.stops = []  # TODO
        self.arrival_multiplier = np.random.uniform(0.005,0.015)

    def __repr__(self):
        return f'<Station {self.id}> {self.name} at {self.location}'

    def simulate_arrivals(self, deltatime):
        self.passenger_count += (deltatime * self.arrival_multiplier)

    def board_passengers(self, vehicle_current_count, vehicle_max_passengers):
        space_available = vehicle_max_passengers - vehicle_current_count
        self.passenger_count = max(0,self.passenger_count - space_available)

    def integrate_line(self, line):
        pass

class Vehicle:
    count = 0

    def __init__(self, capacity, assigned_line, start_x, start_y):
        self.id = Vehicle.count + 1
        Vehicle.count += 1
        self.x = start_x
        self.y = start_y
        self.capacity = capacity
        self.speed = 0.1
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
        next_node = self.path[0]
        if h.get_distance_between(self.x, self.y, next_node.location[0], next_node.location[1]) < 0.2:
            self.path = self.path[1:]
            if len(self.path) == 0:
                self.update_path()
            next_node = self.path[0]
        displacement_vec = (self.path[0].location[0] - self.x, self.path[0].location[1] - self.y)
        normalized_vec = h.normalize_vector(displacement_vec)
        self.x += normalized_vec[0] * self.speed
        self.y += normalized_vec[1] * self.speed



    def load_passengers(self, agents):
        pass

    def unload_passengers(self, agents):
        pass

    def update_manifest(self):
        pass

    def update_path(self):
        # get closest node to current location
        closest_index = None
        closest_distance = 100000000000.0
        for i in range(len(self.assigned_line.stops)):
            distance_to_stop = h.get_distance_between(self.x,
                                                      self.y,
                                                      self.assigned_line.stops[i].location[0],
                                                      self.assigned_line.stops[i].location[1])
            if distance_to_stop < closest_distance:
                closest_distance = distance_to_stop
                closest_index = i

        self.path = self.assigned_line.stops[(closest_index+1):]



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