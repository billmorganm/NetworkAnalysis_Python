import model as m
import network as nw
from scipy.spatial.distance import euclidean
import numpy as np
from pandas import DataFrame

suburbs = nw.get_suburbs()
G = nw.create_graph(suburbs)

engine = m.NetworkAnalysis(G)
engine.add_agents(100)

print(engine.agents)

