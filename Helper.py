import pandas as pd
import numpy as np
from Objects import *

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