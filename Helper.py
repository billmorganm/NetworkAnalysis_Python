import pandas as pd
import numpy as np
from Objects import *
import math

def find_station(stations, name):
    for station in stations:
        if name == station.name:
            return station

def find_line(lines, name):
    for line in lines:
        if f'Line {name}' == line.name:
            return line

def read_stations(dir='Inputs.xlsx'):
    result = []
    data = pd.read_excel(dir, sheet_name='Stations')

    for index, row in data.iterrows():
        name = row['Station Name']
        x = row['x']
        y = row['y']
        station = Station(name, x, y)
        result.append(station)

    return result

def read_lines(stations, dir='Inputs.xlsx'):
    result = []
    data = pd.read_excel(dir, sheet_name='Lines')

    for line in data['Line'].unique():
        stops = list((data[data['Line'] == line]).sort_values(by='Stop', ascending=True)['Station'])
        station_objects = []
        for stop in stops:
            # return the station object
            station_objects.append(find_station(stations, stop))

        result.append(Line(name=f'Line {line}', stops = station_objects))
    return result

def read_vehicles(stations, lines, dir='Inputs.xlsx'):

    data = pd.read_excel(dir, sheet_name='Vehicles')

    for index, row in data.iterrows():
        id = row['Vehicle ID']
        assigned_line = find_line(lines, row['Assigned Line'])
        starting_stop = find_station(stations, row['Starting Stop'])
        capacity = row['Capacity']

        vehicle = Vehicle(capacity, assigned_line, start_x=starting_stop.location[0], start_y=starting_stop.location[1])

        assigned_line.add_vehicle(vehicle)

def get_distance_between(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y1-y2)**2)**0.5


def normalize_vector(vector):
    magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)

    # Avoid division by zero
    if magnitude == 0:
        return (0, 0)

    unit_vector = (vector[0] / magnitude, vector[1] / magnitude)
    return unit_vector